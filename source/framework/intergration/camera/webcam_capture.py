# importing required libraries
from PyQt5.QtCore import pyqtSignal, QByteArray, QBuffer, QIODevice, Qt, QSettings
from PyQt5.QtWidgets import *
from PyQt5.QtMultimedia import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtGui import QImage
import os
import sys
import time


class CameraCapture(QMainWindow):
    save_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__()
        self.setGeometry(100, 100, 600, 600)
        self.setWindowModality(Qt.ApplicationModal)
        # self.setStyleSheet("background : black;")
        self.available_cameras = QCameraInfo.availableCameras()
        self.camera_index = QSettings('sapde', 'sapde').value('camera')-1 or 0

        self.save_path = ""
        self.viewfinder = QCameraViewfinder()
        self.setCentralWidget(self.viewfinder)
        self.select_camera(self.camera_index)

        toolbar = QToolBar("Camera Tool Bar")
        self.addToolBar(toolbar)
        save_action = QAction("Save", self)
        save_action.setToolTip("Save current image (press Enter)")
        save_action.triggered.connect(self.capture_img)
        toolbar.addAction(save_action)
        self.capture.imageCaptured.connect(self.save)
        self.setWindowTitle("Camera view")


    def show(self):
        self.viewfinder.show()
        return super().show()

    def select_camera(self, camera_index):
        self.camera = QCamera(self.available_cameras[camera_index])
        self.camera.setViewfinder(self.viewfinder)
        self.camera.setCaptureMode(QCamera.CaptureStillImage)
        self.camera.start()
        self.capture = QCameraImageCapture(self.camera)
        self.current_camera_name = self.available_cameras[camera_index].description()

        self.save_seq = 0

    def capture_img(self):
        timestamp = time.strftime("%d-%b-%Y-%H_%M_%S")
        self.capture.capture(os.path.join(self.save_path,
                                          "%s-%04d-%s.jpg" % (
                                              self.current_camera_name,
                                              self.save_seq,
                                              timestamp
                                          )))

    def save(self, i, img):
        byteArray = QByteArray()
        buffer = QBuffer(byteArray)
        buffer.open(QIODevice.ReadWrite)
        img.save(buffer, "PNG")  # // writes the image in PNG format inside the buffer
        iconBase64 = byteArray.toBase64().data()
        self.save_signal.emit(repr(iconBase64))
        self.close()




    def change_folder(self):
        path = QFileDialog.getExistingDirectory(self,
                                                "Picture Location", "")
        if path:
            self.save_path = path
            self.save_seq = 0

    def keyPressEvent(self, qKeyEvent):
        if qKeyEvent.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.capture_img()
        else:
            return super().keyPressEvent(qKeyEvent)

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()


if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = CameraCapture()
    sys.exit(App.exec())
