from datetime import datetime
from tabulate import tabulate
from PyQt5.QtCore import dec
import concurrent.futures
from .pool import Pool
from os import path, getenv
import sys

# returns translation of a given string

translation_cache = {}


def tr(phrase, model=None, model_id=None, cache=True):
    from source.framework.pool import Pool
    cached = translation_cache.get(phrase, None)
    if cached is not None:
        return cached
    t = Pool.get('ui_connector') \
        .api_get('translate', {'phrase': phrase,
                               'model': model,
                               'model_id': model_id})
    translation = t and t.get('translation') or phrase

    if cache:
        translation_cache[phrase] = translation
    return translation


def get_error_details(type, value, tback):
    msg = '\n' \
          + 'Exception Type: ' + (str(type.__name__) if type else '-') \
          + '\n' \
          + 'Exception Message: ' + (str(value.message) if hasattr(value, 'message') \
                                         else str(value) if value else '-') \
          + '\n'
    headers = ['File Name', 'Line', 'Method']
    data = list()
    while True:
        data.append([
            str(tback.tb_frame.f_code.co_filename),
            str(tback.tb_lineno),
            str(tback.tb_frame.f_code.co_name)
        ])
        if tback.tb_next:
            tback = tback.tb_next
        else:
            print(data)
            print(headers)
            msg += tabulate(data, headers=headers)
            return msg


def _write_to_log_file(msg: str, file_path: str) -> None:
    date_str = str(datetime.now().date())
    with open(' '.join([file_path, date_str]), "a+") as f:
        f.write(msg)


def log(message, sql=False, print_msg=False):
    if isinstance(message, Exception) and Pool.get('debug'):
        type, value, tback = sys.exc_info()
        message = get_error_details(type, value, tback)
        print(message)
    else:
        message = str(message)
    lad = getenv('LOCALAPPDATA')
    if sql:
        log_path = Pool.get('config').directories.sql_log.replace('(localappdata)', lad) + 'sql_log.txt'
    else:
        log_path = Pool.get('config').directories.log.replace('(localappdata)', lad) + 'EasysERP_log.txt'
    now = str(datetime.now())

    long_message = '\n' + '-' * 30 + '\n' + now + '\n' + message
    if sql == 'error':
        print(long_message)
    _write_to_log_file(long_message, log_path)
    if print_msg: print(long_message)
    return message


def exception_handler(type, value, tback):
    from .ui.qt_ui.extended_widgets.extended_messagebox import MsgBoxError, ExtendedMessageBox

    if type != MsgBoxError:
        msg = ExtendedMessageBox()
        if Pool.get('debug'):
            msg.show(msg.Error, log(get_error_details(type, value, tback)))
        else:
            msg.show(msg.Error, log(str(value.message)
                                    if hasattr(value, 'message') else str(value) if value else '-'))
    sys.__excepthook__(type, value, tback)


def return_exception(func):
    def except_handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return e

    return except_handler


def _eval(val):
    try:
        return eval(val)
    except:
        return val


def run_in_thread(func):
    def run(*args, **kwargs):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(func, *args, **kwargs)
            res = future.result()
            return res

    return run
