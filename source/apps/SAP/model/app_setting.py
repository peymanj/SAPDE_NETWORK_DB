from PyQt5.QtMultimedia import QCameraInfo
from source.framework.base_model import Model
from source.framework.fields import Fields


class AppSetting(Model):
    def __init__(self) -> None:
        super().__init__()

    _name = 'app_setting'
    _table = 'app_setting'
    _id_column = 'id'
    _init = True
    _get_name_string = '{id}'

    def _camera_selection(self, id=None):
        available_cameras = QCameraInfo.availableCameras()
        data = list()
        for i, cam in enumerate(available_cameras):
            data.append((i + 1, cam.description()))
        return self.search_in_tuple_list(data, id)

    _fields = {
        'id': Fields.integer('id'),
        'camera': Fields.selection('Default camera', func=_camera_selection, required=False, local_data='get_camera'),
        # 'master_password': Fields.char('Master password', length=100, required=True),
    }

    def create(self, context=None):
        if self.read():
            return None
        return super().create(context=context)

    def delete(self, context=None):
        return None

    def get_setting(self):
        context = {'return_object': False, 'post_proc': False}
        setting = self.read(context=context)
        return setting[0] if setting else setting

    def master_pass_check(self, context=None):
        password = context.get('password')
        return True if password == self.get_setting()['master_password'] else False
