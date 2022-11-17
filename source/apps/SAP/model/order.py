import os
from datetime import datetime
from os import getenv, path
from base64 import urlsafe_b64decode
from googleapiclient.errors import HttpError

from source.framework.base_model import Model
from source.framework.fields import Fields
from source.framework.intergration.gdrive.gdrive_api import GoogleSheetsAPI
from source.framework.utilities import log
from source.framework.utilities import tr
from .gsheet_cell_format import *


class Order(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'order'
    _table = 'order'
    _id_column = 'id'
    _init = True
    _get_name_string = '{code}'
    _log = True

    def _current_user(self, context=None):
        return context.get('uid')

    def update_status(self, ids):
        for id in ids:

            order_items = self.pool.get('api').internal_exec('order_item', 'search',
                                                    {'fields': ['status'], 'condition': [('order_id', '=', id)]})
            n_order_items = len(order_items)
            n_order_items_ok = 0
            for rec in order_items:
                if rec.get('status'):
                    n_order_items_ok += 1
            if n_order_items_ok == n_order_items != 0:
                status = True
            else:
                status = False
            self.update({'id': id, 'field_values': {'status': status}})

    _fields = {
        'id': Fields.integer('id'),
        'code': Fields.char('Order number', length=120, required=True),
        'delivery_date': Fields.datetime('Delivery Date'),
        'total_items': Fields.integer('Delivery Date'),
        'order_items': Fields.one2many('Order items', relation='order_item', field='order_id'),
        'g_sheet': Fields.char('Google sheets URL', length=500, required=False),
        'client_gmail': Fields.char('Client Gmail', length=100, required=False),
        'status': Fields.boolean('Status', default=False),
        'caption_set': Fields.many2one('Caption Set', relation='caption_set'),
    }

    _sql_constraints = [
        ('unique_order_code', 'unique', ['code']),
    ]

    _default_values = {
        'user': _current_user,
        'delivery_date': 'today',
    }

    def upload_order_to_gdrive(self, context=None):

        def create_new_sheet(order):
            try:
                sheet_id = gapi.create(order.code)
            except Exception as e:
                log(e)
                return {'message': 'Unable to create new Google Sheet'}
            sheet_url = 'https://docs.google.com/spreadsheets/d/' + sheet_id
            self.update({'id': order.id, 'field_values': {'g_sheet': sheet_url}})
            return sheet_id

        order_id = context.get('id')
        order = self.pool.get('api').internal_exec('order', 'read', {'ids': [order_id], 'return_object': True})[0]
        data = self.get_report_data(order_id, order)
        try:
            gapi = GoogleSheetsAPI()
            init_data = gapi.check_creds()
            if init_data == FileNotFoundError:
                return {'message': 'cred_file_not_found'}

        except Exception as e:
            log(e)
            return {'message': 'Unable to connect to Google Sheet API'}
        if not order.g_sheet:
            sheet_id = create_new_sheet(order)
        try:
            spreadsheet_id = order.g_sheet.replace('https://docs.google.com/spreadsheets/d/', '') \
                if order.g_sheet else sheet_id
            gapi.batch_update_values(spreadsheet_id,
                                     'A1', 'USER_ENTERED', data)
        except HttpError as e:
            log(e)
            if e.status_code == 404:
                spreadsheet_id = create_new_sheet(order)
                gapi.batch_update_values(spreadsheet_id,
                                         'A1', 'USER_ENTERED', data)
            else:
                return {'message': 'Unable send data Google Sheet'}
        except Exception as e:
            log(e)
            return {'message': 'Unable send data Google Sheet'}

        try:
            gapi.grant_access(spreadsheet_id, order.client_gmail)
        except Exception as e:
            log(e)
            return {'message': 'Unable to grant access for client Gmail'}

        for f in format_list:
            gapi.format_cells(spreadsheet_id, f)
        return {'message': 'Upload successful.'}

    def copy_cred_file(self, params={}):
        file = params.get('file')
        if file:
            cred_path = path.join(self.pool.get('config').directories.gdrive_token, 'google_sheet.json')
            if not cred_path:
                cred_path = path.join(getenv('LOCALAPPDATA'), r"sap\credentials\google_sheet.json")
            with open(cred_path, "wb") as f:
                f.write(bytes(file, 'utf-8'))

    def get_report_data(self, order_id, order_obj):
        def get(data_dict, key):
            val = data_dict.get(key)

            if isinstance(val, tuple):
                    val = val[1]
            if val is None:
                val = '--'
            if isinstance(val, bool):
                val = '✔' if val else 'x'
            return val


        class IncompleteSetExists(Exception):
            def __init__(self) -> None:
                super().__init__('There is at least one set with incomplete data. Unable to upload to GDrive.')

        sn_count = 8
        chk_count = 8
        data = self.pool.get('api').internal_exec('parts_per_order_report', 'read', context={'order_id': order_id})
        header = list()
        header.append([tr('SAP Data Entry Log File')])
        header.append([tr('Order'), order_obj.code])
        header.append([tr('Delivery Date'), str(order_obj.delivery_date.date())])
        header.append([tr('Report update Date'), str(datetime.now().date())])
        header.append([''] * 6 + [tr('Front')] + [''] * (sn_count + chk_count) + [tr('Back')])
        columns = [tr('Row'), tr('Pallet'), tr('Box'), tr('Set'), tr('Model'), tr('Size')]
        def _tr(phrase):
            return  self.pool.get('api').internal_exec('parts_per_order_report', 'translate', {'phrase': phrase, 'model_id':order_id})
        columns += [_tr(f'Serial Number {i}') for i in range(1, sn_count + 1)] \
                   + [_tr(f'Final Check {i}') for i in range(1, chk_count + 1)] + [tr('Weight')]
        columns += [_tr(f'Serial Number {i}') for i in range(1, sn_count + 1)] \
                   + [_tr(f'Final Check {i}') for i in range(1, chk_count + 1)] + [tr('Weight')]
        columns += [tr('Set weight'), tr('Create User'), tr('Editor user'), tr('Edit date')]
        header.append(columns)

        struct = list()
        for i in range(0, len(data), 2):
            recf = data[i]
            try:
                recb = data[i + 1]
            except Exception as e:
                raise IncompleteSetExists
            struct.append(
                [(i + 2) / 2, get(recf, 'pallet'), get(recf, 'box'), get(recf, 'item_set'), get(recf, 'model'),
                 get(recf, 'size'),
                 get(recf, 'sn1'), get(recf, 'sn2'), get(recf, 'sn3'), get(recf, 'sn4'),
                 get(recf, 'sn5'), get(recf, 'sn6'), get(recf, 'sn7'), get(recf, 'sn8'),

                 get(recf, 'check1'), get(recf, 'check2'), get(recf, 'check3'), get(recf, 'check4'),
                 get(recf, 'check5'), get(recf, 'check6'), get(recf, 'check7'), get(recf, 'check8'),
                 get(recf, 'weight'),

                 get(recb, 'sn1'), get(recb, 'sn2'), get(recb, 'sn3'), get(recb, 'sn4'),
                 get(recb, 'sn5'), get(recb, 'sn6'), get(recb, 'sn7'), get(recb, 'sn8'),

                 get(recb, 'check1'), get(recb, 'check2'), get(recb, 'check3'), get(recb, 'check4'),
                 get(recb, 'check5'), get(recb, 'check6'), get(recb, 'check7'), get(recb, 'check8'),
                 get(recb, 'weight'),

                 get(recf, 'weight') + get(recb, 'weight'), get(recf, 'create_user'), get(recf, 'check_user'),
                 str(get(recf, 'update_date').date())
                 ])
        return header + struct
