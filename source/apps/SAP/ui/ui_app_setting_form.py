from source.framework.ui.qt_ui.ui_base_class import UiBaseClass
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import QCameraInfo


class UiAppSettingForm(UiBaseClass):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_camera(self, id=None):

        def search_in_tuple_list(tup_list, id, index=0):
            if not id:
                return tup_list
            res = None
            for tup in tup_list:
                if tup[index] == id:
                    res = tup[1]
            return res

        available_cameras = QCameraInfo.availableCameras()
        data = list()
        for i, cam in enumerate(available_cameras):
            data.append((i + 1, cam.description()))
        return search_in_tuple_list(data, id)


    _model = 'app_setting'
    _menu_bar = False
    _list_view = {
        'first_list': {'source': 'UiAppSettingForm'}
    }

    _form_view = {
        'fields': [
            'camera',
        ],

    }

    