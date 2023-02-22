from source.framework.ui.qt_ui.ui_base_class import UiBaseClass

class UiCaptionSetForm(UiBaseClass):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    _menu_bar = False
    _model = 'caption_set'

    _list_view = {
        'first_list': {'source': 'UiCaptionSetForm'}
    }

    _form_view = {
        'fields': [
            'name',
            'part1_tr',
            'part2_tr',
            'part3_tr',
            'part4_tr',
            'sn1_tr',
            'sn2_tr',
            'sn3_tr',
            'sn4_tr',
            'sn5_tr',
            'sn6_tr',
            'sn7_tr',
            'sn8_tr',
            'check1_tr',
            'check2_tr',
            'check3_tr',
            'check4_tr',
            'check5_tr',
            'check6_tr',
            'check7_tr',
            'check8_tr',
        ],
    }
