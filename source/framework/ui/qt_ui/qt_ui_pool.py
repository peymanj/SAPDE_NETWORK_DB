from os import error


class QtUiPool():

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
        
        