from PyQt5.QtWidgets import *
from .searchForm import searchFrom
from .ui_shared_methods import get_data_from_db

f_index_mapped = {
    'char':        0,
    'datetime':    1,
    'date':        2,
    'integer':     3,
    'boolean':     4,
    'selection':   0,
    'many2one':    0,
    'many2many':   0,
}

class operator:
    Like = 'Like'
    NotLike = 'Not Like'
    Contains = 'Like'
    StartsWith = 'Like'
    EndsWith = 'Like' 
    In = 'In'
    ET = '='
    NET = '!='
    GT = '>'
    ST = '<'
    GET = '>='
    SET = '<='

class UiSearch(QWidget):
    
    def __init__(self, *args, parent_form=None, table_widget=None, **kwargs):
        super(UiSearch, self).__init__(*args, **kwargs)
        self.parent = parent_form
        self.twidget = table_widget
        self.search_form = searchFrom()
        self.search_form.setupUi()
        self.set_connections()
        self.set_init_field_data()

    def show(self, field_name=None):
        self.f_name = field_name
        self.f_obj = self.twidget.model_fields.get(field_name)
        field_type = self.f_obj['display'] or self.f_obj['type']
        self.search_form.stackedWidget.setCurrentIndex(f_index_mapped.get(field_type))
        self.set_layout()
        self.search_form.show()

    def set_connections(self):
        self.conditions = list()
        self.search_form.searchPushButton.clicked.connect(self.search)
        self.search_form.cancelPushButton.clicked.connect(self.search_form.hide)
        self.search_form.clearPushButton.clicked.connect(self.clear_search)


    def set_layout(self):
        # ----------------------------------------------------------
        if self.f_obj['relation']:
            data = self.parent.api('exec', self.f_obj['relation'], 'read', {'as_relational': True})
            if not self.f_obj['display']:
                self.relative_search = True
                self.search_form.relationalComboBox.setValue(data)
            else:
                if self.f_obj['display'].lower() == 'char':
                    self.relative_search = False
        elif self.f_obj['type'] == 'selection':
            self.relative_search = True
            context = {'order_id': self.get_current_parent('order')}
            selections = self.parent.api('exec', self.parent.model, self.f_obj['func'], context=context)
            self.search_form.relationalComboBox.setValue(selections)
        else:
            self.relative_search = False

        if not self.relative_search:
            self.search_form.relationalMainWidget.setHidden(True)
            self.search_form.stackedWidget.setHidden(False)
        else:
            self.search_form.relationalMainWidget.setHidden(False)
            self.search_form.stackedWidget.setHidden(True)
    
    def set_init_field_data(self):
        str_operators = [
            (0, 'Equal to'),
            (1, 'Not like'),
            (2, 'Contains'),    # wildcards needed
            (3, 'Starts with'), # wildcards needed
            (4, 'Ends with'),   # wildcards needed
        ]
        self.search_form.charFieldComboBox.setValue(str_operators)
        self.search_form.charFieldComboBox.setCurrentIndex(0)
        
        #-----------------------------------------------------------
        self.search_form.dateFieldFromDateEdit.setValue('today')
        self.search_form.dateFieldToDateEdit.setValue('today')
        #-----------------------------------------------------------
        self.search_form.dateTimeFieldFromDateTimeEdit.setValue('today')
        self.search_form.dateTimeFieldToDateTimeEdit.setValue('today')
        #-----------------------------------------------------------
        int_operators = [
            (operator.ET, 'Equal to'),
            (operator.NET, 'Not equal to'),
            (operator.GET, 'Greater than or equal to'),   
            (operator.SET, 'Smaller than or equal to'), 
            (operator.GT, 'Greater than'),  
            (operator.ST, 'Smaller than'),
        ]
        self.search_form.integerFieldComboBox.setValue(int_operators)
        self.search_form.integerFieldComboBox.setCurrentIndex(0)

        self.search_form.booleanFieldComboBox.setValue([(True, 'Checked'), (False, 'Not checked')])

    def search(self):
        model = self.twidget.source_model
        self.twidget.search_args[self.f_name] = list()
        index = self.search_form.stackedWidget.currentIndex()
        
        if self.relative_search:
            selected_index = self.search_form.relationalComboBox.getValue()
            if selected_index:
                criteria = operator.In
                search_str = selected_index
                self.twidget.search_args[self.f_name].append((self.f_name, criteria, search_str))
        
        elif index == 0:
            search_str = self.search_form.charFieldLineEdit.text()
            criteria = self.search_form.charFieldComboBox.getValue()

            if criteria == 0:
                criteria = operator.Like
            elif criteria == 1:
                criteria = operator.NotLike
            elif criteria == 2:
                criteria = operator.Contains
                search_str = '%' + search_str + '%'
            elif criteria == 3:
                criteria = operator.StartsWith
                search_str = search_str + '%'
            elif criteria == 4:
                criteria = operator.EndsWith
                search_str = '%' + search_str 

            self.twidget.search_args[self.f_name].append((self.f_name, criteria, search_str))

        elif index == 1:
            s_date = self.search_form.dateTimeFieldFromDateTimeEdit.getValue()
            e_date = self.search_form.dateTimeFieldToDateTimeEdit.getValue()
            self.twidget.search_args[self.f_name].append((self.f_name, '>=', s_date))
            self.twidget.search_args[self.f_name].append((self.f_name, '<=', e_date))

        elif index == 2:
            s_date = self.search_form.dateFieldFromDateEdit.getValue()
            e_date = self.search_form.dateFieldToDateEdit.getValue()
            self.twidget.search_args[self.f_name].append((self.f_name, '>=', s_date))
            self.twidget.search_args[self.f_name].append((self.f_name, '<=', e_date))

        elif index == 3:
            search_val = self.search_form.integerFieldDoubleSpinBox.value()
            criteria = self.search_form.integerFieldComboBox.getValue()
            self.twidget.search_args[self.f_name].append((self.f_name, criteria, search_val))

        elif index == 4:
            search_val = self.search_form.booleanFieldComboBox.getValue()
            self.twidget.search_args[self.f_name].append((self.f_name, '=', search_val))

        data = get_data_from_db(self.parent, model=model, condition=self.generate_condition())
        self.twidget.load_data_to_table(data)
        self.search_form.hide()

    def clear_search(self):
        if self.f_name in self.twidget.search_args:
            self.twidget.search_args.pop(self.f_name)
        data = get_data_from_db(self.parent, model=self.parent._model, condition=self.generate_condition())
        self.twidget.load_data_to_table(data)
        self.search_form.hide()

    def generate_condition(self):
        conditions = list()
        for key, val in self.twidget.search_args.items():
            if val:
                conditions.extend(val)
        return (len(conditions) - 1) * ['and'] + conditions

