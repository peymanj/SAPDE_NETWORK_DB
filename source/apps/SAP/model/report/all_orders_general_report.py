from source.framework import fields
from source.framework.base_model import Model
from source.framework.fields import Fields


class AllOrdersGeneralReport(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'all_orders_general_report'
    _id_column = 'id'
    _init = True
    _get_name_string = '{id}'
    _order = '[order] DESC, pallet, box, item_set, side'

    def _side_selection(self, params={}):
        id = params.get('id')
        data = [
            (1, 'Front'),
            (2, 'Back'),
        ]
        return self.search_in_tuple_list(data, id)

    _fields = {
        'id': Fields.integer('id'),
        'order': Fields.many2one('Order', relation='order'),
        'order_item': Fields.many2one('Order item', relation='order_item'),
        'pallet': Fields.many2one('Pallet', relation='pallet'),
        'box': Fields.many2one('Box', relation='box', search=False),
        'size': Fields.many2one('Size', relation='size'),
        'model': Fields.many2one('Model', relation='model'),
        'item_set': Fields.many2one('Set', relation='item_set', display='char', search=False),
        'side': Fields.selection('Side', func=_side_selection),  # 1: front  ,    2: back
        'weight': Fields.integer('Weight'),
        'sn1': Fields.char('Serial number 1', length=100, required=True),
        'sn2': Fields.char('Serial number 2', length=100),
        'sn3': Fields.char('Serial number 3', length=100),
        'sn4': Fields.char('Serial number 4', length=100),
        'sn5': Fields.char('Serial number 5', length=100),
        'sn6': Fields.char('Serial number 6', length=100),
        'sn7': Fields.char('Serial number 7', length=100),
        'sn8': Fields.char('Serial number 8', length=100),
        'check1': Fields.boolean('Final check 1'),
        'check2': Fields.boolean('Final check 2'),
        'check3': Fields.boolean('Final check 3'),
        'check4': Fields.boolean('Final check 4'),
        'check5': Fields.boolean('Final check 5'),
        'check6': Fields.boolean('Final check 6'),
        'check7': Fields.boolean('Final check 7'),
        'check8': Fields.boolean('Final check 8'),
        'check_user': Fields.many2one('Last checker user', relation='user'),
        'create_user': Fields.many2one('Creator user', relation='user'),
        'create_date': Fields.datetime('Create date'),
        'update_user': Fields.many2one('Editor user', relation='user'),
        'update_date': Fields.datetime('Edit date'),
        # 'image':            Fields.binary('Image'),
    }

    def load_stored_function(self, context=None):
        query = f"""
            all_orders_general_report()
        """
        return query

    def init(self):
        self.drop_function_if_exists('all_orders_general_report')
        query = """
            CREATE FUNCTION [all_orders_general_report] ()
            RETURNS 
            TABLE 
            AS	
            RETURN 
            Select top 10000
                p.id as id,
                oi.order_id as [order],
                oi.id as order_item,
                oi.pallet_no as pallet,
                b.id as box,
                oi.size as size,
                oi.model as model,
                iset.id as item_set,
                p.side as side,
                p.[weight] as [weight],
                p.sn1,
                p.sn2,
                p.sn3,
                p.sn4,
                p.sn5,
                p.sn6,
                p.sn7,
                p.sn8,
                p.check1,
                p.check2,
                p.check3,
                p.check4,
                p.check5,
                p.check6,
                p.check7,
                p.check8,
                p.check_user,
                p.create_user,
                p.create_date,
                p.update_date,
                p.update_user
            From part p
            Left Join item_set iset on iset.id = p.item_set
            Left Join box b on b.id = iset.box
            Left Join order_item oi on oi.id = b.order_item
            Order By oi.id DESC, oi.pallet_no, b.code, iset.code
        """
        self.orm_exec(query)
