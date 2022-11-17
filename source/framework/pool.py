from .config import apps
import inspect
from sys import modules


class Pool():

    def __init__(self) -> None:
        pass
    
    @classmethod
    def set(cls, obj, name):
        # if not getattr(cls, name, None):
        setattr(cls, name, obj)
        return getattr(cls, name, None)
        # else:
            # return None
    
    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)



class UiModelPool:
    @classmethod
    def set(cls, name, model_class):
        setattr(cls, name, model_class)

    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)

    @classmethod
    def init(cls):
        cls._active_ui_models = list()
        for app in apps:
            cls._active_ui_models.extend(cls._get_app_active_models(app))
            cls._active_ui_models.extend(cls._get_framework_active_models())

        for model in cls._active_ui_models:
            UiModelPool.set(model[0], model[1])

        return cls

    @classmethod
    def _get_app_active_models(cls, app):
        return inspect.getmembers(
            modules[f'source.apps.{app}.ui'], inspect.isclass)

    @classmethod
    def _get_framework_active_models(cls):
        return inspect.getmembers(
            modules[f'source.framework.framework_models.ui'], inspect.isclass)


class ModelPool:
    @classmethod
    def set(cls, name, model_class):
        setattr(cls, name, model_class)

    @classmethod
    def get(cls, name):
        return getattr(cls, name, None)

