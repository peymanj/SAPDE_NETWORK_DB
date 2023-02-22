from datetime import datetime
from os import getenv, path, remove
from shutil import rmtree
from base64 import urlsafe_b64decode
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
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
            context.update({'id': order.id, 'field_values': {'g_sheet': sheet_url}})
            self.update(context)
            return sheet_id

        order_id = context.get('id')
        order = self.pool.get('api').internal_exec('order', 'read', {'ids': [order_id], 'return_object': True})[0]
        data = self.get_report_data(order_id, order)
        try:
            cred_path = path.join(getenv('LOCALAPPDATA'), r"sap\credentials")
            # gapi = GoogleSheetsAPI(cred_path=cred_path)
            # init_data = gapi.check_creds()
            raise RefreshError
            if init_data == FileNotFoundError:
                return {'message': 'cred_file_not_found'}
        except RefreshError as e:
            remove(cred_path)
            # log(e)
            return {'message': e.args[0]}
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
        start = 0
        headers = data[4]
        color = 0
        colors = {
            0: {'r':0.4, 'g':0.6, 'b':1.0},
            1: {'r':0.0, 'g':0.8, 'b':0.4},
            2: {'r':1.0, 'g':1.0, 'b':0.6},
            3: {'r':0.8, 'g':0.6, 'b':1.0},
            4: {'r':0.0, 'g':1.0, 'b':1.0},
        }
        for i in range(len(headers)-1):
            end = 0
            if headers[i]:
                start = i
            if headers[i+1] and start:
                end = i + 1
            if i == len(headers)-2:
                end = i + 2
            if start and end:
                c = colors[color]
                f = get_part_header_format(start, end, c['r'], c['g'], c['b'])
                gapi.format_cells(spreadsheet_id, f)
                color += 1

        f = get_end_header_format(end, end + 4, **colors[4])
        gapi.format_cells(spreadsheet_id, f)
        return {'message': 'Upload successful.'}

    def copy_cred_file(self, params={}):
        file = params.get('file')
        if file:
            # cred_path = path.join(self.pool.get('config').directories.gdrive_token, 'google_sheet.json')
            # if not cred_path:
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

        data = self.pool.get('api').internal_exec('parts_per_order_report', 'read', context={'order_id': order_id})

        n_data = len(data)
        order_item_data = {}
        ordered_data = {}
        for i in range(n_data):
            set_no = data[i]['item_set'][0]
            order_item_no = data[i]['order_item'][0]

            if order_item_no not in ordered_data:
                ordered_data[order_item_no] = {}
            if set_no not in ordered_data[order_item_no]:
                ordered_data[order_item_no][set_no] = {
                    'parts': [False] * 4,
                    'weight': 0,
                    'create_user': None,
                    'update_user': None,
                    'update_date': None,
                }
            ordered_data[order_item_no][set_no]['parts'][data[i]['side'][0] - 1] = (data[i])
            if order_item_no not in order_item_data:
                order_item_data[order_item_no] = data[i]

        max_part_column = 0
        update_date = datetime(1900, 1, 1)

        for o_i in ordered_data:
            for i_s in ordered_data[o_i]:
                parts = ordered_data[o_i][i_s]['parts']
                max_part = 0
                for i in range(len(parts), 0, -1):
                    if parts[i - 1]:
                        max_part = i
                        break

                if max_part > max_part_column:
                    max_part_column = max_part

                sum_weight = 0
                for part in ordered_data[o_i][i_s]['parts']:
                    sum_weight += part.get('weight', 0) if part else 0
                    if part and update_date < part["update_date"]:
                        update_date = part["update_date"]
                ordered_data[o_i][i_s]['weight'] = sum_weight
                ordered_data[o_i][i_s]['update_date'] = update_date

        wmax = 0
        wmin = 100000
        for o_i in ordered_data:
            for n in ordered_data[o_i]:
                i_s = ordered_data[o_i][n]
                if i_s.get('weight') > wmax:
                    wmax = i_s.get('weight')
            if i_s.get('weight') < wmin:
                wmin = i_s.get('weight')

        max_part_count = {
            1: {'sn': 0, 'check': 0},
            2: {'sn': 0, 'check': 0},
            3: {'sn': 0, 'check': 0},
            4: {'sn': 0, 'check': 0},
        }
        for o_i in ordered_data:
            for i_s in ordered_data[o_i]:
                for i in range(1, len(ordered_data[o_i][i_s]['parts']) + 1):
                    part = ordered_data[o_i][i_s]['parts'][i - 1]
                    sn = 0
                    check = 0
                    for c in range(1, 9):
                        if part and part.get('sn%s' % c) is not None:
                            sn += 1
                        if part and part.get('check%s' % c) is not None:
                            check += 1
                    if max_part_count[i]['sn'] < sn:
                        max_part_count[i]['sn'] = sn
                    if max_part_count[i]['check'] < check:
                        max_part_count[i]['check'] = check
                break

        visible_parts = {}
        for i in range(1, 5):
            visible_parts[i] = {}
            if i <= max_part_column:
                visible_parts[i]['visible'] = True
                sn = max_part_count[i]['sn']
                check = max_part_count[i]['check']
            else:
                visible_parts[i]['visible'] = False
                sn = 0
                check = 0

            visible_parts[i]['visible_sn_count'] = [True] * sn + [False] * (8 - sn)
            visible_parts[i]['visible_check_count'] = [True] * check + [False] * (8 - check)

        def _tr(phrase):
            return  self.pool.get('api').internal_exec('part', 'translate', {'phrase': phrase, 'model_id':order_id})
        headers = list()
        headers.append([_tr('SAP Data Entry Log File')])
        headers.append([_tr('Order'), order_obj.code])
        headers.append([_tr('Delivery Date'), str(order_obj.delivery_date.date())])
        headers.append([_tr('Report update Date'), str(datetime.now().date())])
        h = [''] * 6
        for i in range(4):
            if visible_parts.get(i+1)['visible']:
                h += [_tr('Part ' + str(i+1))] + (max_part_count.get(i + 1)['sn'] + max_part_count.get(i + 1)['check'] + 3) * ['']
        headers.append(h)
        columns = [_tr('Row'), _tr('Pallet'), _tr('Box'), _tr('Set'), _tr('Model'), _tr('Size')]
        for p in range(1, 5):
            for i in range(8):
                if visible_parts.get(p)['visible_sn_count'][i]:
                    columns += [_tr(f'Serial Number {i+1}')]
            for i in range(8):
                if visible_parts.get(p)['visible_check_count'][i]:
                    columns += [_tr(f'Final Check {i+1}')]
            if visible_parts.get(p)['visible']:
                columns += [_tr('Weight'), _tr('length'), _tr('width'), _tr('thickness')]

        columns += [_tr('Set weight'), _tr('Create User'), _tr('Editor user'), _tr('Edit date')]
        headers.append(columns)

        index = 0
        struct = []
        for o_i in ordered_data:
            for i_s in ordered_data[o_i]:
                index += 1
                struct.append([])
                order_item = order_item_data[o_i]
                struct[-1] += [index, get(order_item, 'pallet'), get(order_item, 'box'), get(order_item, 'item_set'), get(order_item, 'model'),
                        get(order_item, 'size'),]
                for p in range(1, 5):
                    if p - 1 < len(ordered_data[o_i][i_s]['parts']):
                        part = ordered_data[o_i][i_s]['parts'][p-1]
                    else:
                        part = False
                    for j in range(8):
                        if visible_parts.get(p)['visible_sn_count'][j]:
                            if part and get(part, 'sn' + str(j + 1)):
                                struct[-1] += [get(part, 'sn' + str(j + 1))]
                            else:
                                struct[-1] += ['---']
                    for j in range(8):
                        if visible_parts.get(p)['visible_check_count'][j]:
                            if part and get(part, 'check' + str(j + 1)):
                                struct[-1] += [get(part, 'check' + str(j + 1))]
                            else:
                                struct[-1] += ['---']
                    other_fields = ['weight', 'length', 'width', 'thickness']
                    for f in other_fields:
                        if visible_parts.get(p)['visible']:
                            if part:
                                struct[-1] += [get(part, f)]
                            else:
                                struct[-1] += ['---']
                struct[-1].append(ordered_data[o_i][i_s]['weight'])
                struct[-1].append('N/A')
                struct[-1].append('N/A')
                struct[-1].append(str(ordered_data[o_i][i_s]['update_date']))

        return headers + struct
