from source.framework.api import Api

api = Api()


def login(*args, **kwargs):
    res = api.api_gate('authenticate', *args, **kwargs)
    return res


def get_ui_model_access(*args, **kwargs):
    res = api.api_gate('get_ui_model_access', *args, **kwargs)
    return res


def get_model_fields(*args, **kwargs):
    res = api.api_gate('get_model_fields', *args, **kwargs)
    return res


def get_model_field(*args, **kwargs):
    res = api.api_gate('get_model_field', *args, **kwargs)
    return res


def get_model_parameter(*args, **kwargs):
    res = api.api_gate('get_model_parameter', *args, **kwargs)
    return res


def exec(*args, **kwargs):
    res = api.api_gate('exec', *args, **kwargs)
    return res


def get_visible_fields(*args, **kwargs):
    res = api.api_gate('get_visible_fields', *args, **kwargs)
    return res


def get_init_setting(*args, **kwargs):
    res = api.api_gate('get_init_setting', *args, **kwargs)
    return res


def translate(*args, **kwargs):
    res = api.api_gate('translate', *args, **kwargs)
    return res


def get_relations(*args, **kwargs):
    res = api.api_gate('get_relations', *args, **kwargs)
    return res

