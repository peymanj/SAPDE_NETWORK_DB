from PyQt5.QtCore import QEventLoop, QObject, QRunnable, QThread, QThreadPool, QTimer, Qt, pyqtSignal, pyqtSlot
from source.framework.ui.qt_ui import UiBaseClassWizard
import importlib
from source.framework.config import current_app
from source.framework.ui.qt_ui.extended_widgets import ExtendedMessageBox
from source.framework.ui.qt_ui.qt_ui_pool import QtUiPool
from source.framework.utilities import run_in_thread, tr, log
from .ui_base_frame_layout import UiBaseFrameLayout
from source.framework.framework_models.ui.loading import Loading
from source.framework.request_handler import RequestHandler
from source.framework.base import Base
from source.framework.utilities import return_exception


class Signal(QObject):
    new_form =      pyqtSignal(object, object, object, object, object)
    open_search =   pyqtSignal(object, object)
    setting_view =  pyqtSignal()
    exit_view =     pyqtSignal()
    refresh =       pyqtSignal()
    close_form =    pyqtSignal()
    delete =        pyqtSignal(object)


class UiConnector(QObject, Base):
    
    def __init__(self) -> None:
        super().__init__()
        self.form_obj = None
        self.base_signals = self.connect_signals(None, Signal())
        self.stacked_form = UiBaseFrameLayout(self.base_signals)
        self.base_signals.exit_view.connect(self.stacked_form.close)
        self.loading = Loading(self.stacked_form.statusBar)
        self.threadpool = QThreadPool()
        self.threadpool.setExpiryTimeout(60000)
        self.loading = Loading(self.stacked_form) 
        self.loading_delay_start_timer = QTimer()
        self.loading_delay_start_timer.timeout.connect(self.loading.start)
        self.loading_delay_stop_timer = QTimer()
        self.loading_delay_stop_timer.timeout.connect(self.loading.stop)

    def connect_signals(self, form_obj, signal):
        signal.new_form.connect\
            (lambda parent, model, mode, id, base_menu: self.generate_form_from_model(
                parent, model, mode, id=id, base_menu=base_menu))
        signal.close_form.connect(self.close_form)

        if form_obj:
            signal.refresh.connect(form_obj.refresh) 
            signal.delete.connect(form_obj.delete)      
        return signal

    def generate_form_from_model(self, parent, ui_model, mode, id=None, add_nav=True, base_menu=False):  
        if not isinstance(ui_model, str):
            ui_model = type(ui_model).__name__
        access = self.api_get('get_ui_model_access', {'ui_model': ui_model, 'mode': mode})
        action_class = self.pool.get('ui_models').get(ui_model)
        try:
            if issubclass(action_class, UiBaseClassWizard):
                self.form = action_class()
                return self.form
        except Exception:
            raise Exception('Ui model is not defined properly.')
        model = action_class._model
        msg = ExtendedMessageBox()
        if id == False:
            msg.show(msg.Error, tr('No item selected.'))
        action_form = action_class(
            stacked_form=self.stacked_form, 
            mode=mode, 
            model=model,
            id=id, 
            parent=parent,
            set_form_stat=add_nav,  
        )
        action_form.set_signals(self.connect_signals(action_form, Signal()))
        if base_menu:
            self.stacked_form.reset_navigation()
        if add_nav:
            self.form_obj = QtUiPool.set(action_form, ui_model)
            action_form.init()
            self.stacked_form.stackedWidget.addWidget(self.form_obj)
            self.stacked_form.stackedWidget.setCurrentIndex(self.stack_index)
            self.stacked_form.add_nav_button(self.stack_index, action_class, id, mode)
            if len(self.open_models) > self.stack_index:
                self.open_models = self.open_models[:self.stack_index] + [{model:self.form_obj}]
            else:
                self.open_models += [{model:self.form_obj}]
            self.stack_index += 1

        return action_form

    def initiate_app(self):
        self.app_module = importlib.import_module(f'source.apps.{current_app}')
        init_action = self.app_module.qt.base_action
        ui_shared_name = self.app_module.qt.shared_ui_class
        self.stacked_form.set_elements(getattr(self.app_module, ui_shared_name))
        self.stacked_form.showMaximized()
        self.stack_index = 0
        self.open_models = list()
        self.form = self.generate_form_from_model(None, init_action, 3) # 3: list view



    def api(self, method, params):
        if self.pool.get('current_user'):
            params.update({'uid': self.pool.get('current_user')['id']})

        result = None
        if self.loading:
            self.loading_delay_start_timer.start(500)
            self.loading_delay_stop_timer.stop()
            method = return_exception(method)
            self.run_in_thread(
                method, params=params)

        if self.loading:
            self.loading_delay_stop_timer.start(300)
            self.loading_delay_start_timer.stop()

        self.msg = ExtendedMessageBox()
        if isinstance(self.result, Exception):
            log(str(self.result))
            raise self.result
            self.msg.show(self.msg.Error, str(self.result))
        elif self.result and self.result.get('easys_error'):
            log(self.result.get('easys_error'))
            self.msg.show(self.msg.Error, self.result.get('easys_error'))
        else:
            return self.result

    def api_get(self, endpoint, params):
        import source.framework.server_api as server_api
        res = self.api(getattr(server_api, endpoint), params)
        return res

    def api_post(self, endpoint, params):
        import source.framework.server_api as server_api
        res = self.api(getattr(server_api, endpoint), params)
        return res
    
    def close_form(self):
        curr_index = self.stacked_form.stackedWidget.count() - 1
        getattr(self.stacked_form, 'nav_pushbutton_' + str(curr_index -1)).clicked.emit()
    
    def set_result(self, result):
        self.result = result

    def thread_complete(self):
        # print(self.threadpool.activeThreadCount())
        pass

    def run_in_thread(self, func, *args, **kwargs):

        worker = Worker(func, *args, **kwargs) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.set_result)
        worker.signals.finished.connect(self.thread_complete)
        ev = QEventLoop()
        worker.signals.finished.connect(ev.quit)

        self.threadpool.start(worker)
        ev.exec()       


class Worker(QRunnable):

    def __init__(self, func, *args, **kwargs):
        super(Worker, self).__init__()
        self.func =  func
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()
        self.setAutoDelete(True)

    @pyqtSlot()
    def run(self):
        res = self.func(*self.args, **self.kwargs)
        self.signals.result.emit(res)
        self.signals.finished.emit()


class WorkerSignals(QObject):

    finished = pyqtSignal()
    error = pyqtSignal(list)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)
