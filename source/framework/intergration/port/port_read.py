from PyQt5.QtCore import QObject, pyqtSignal
from serial import Serial, PARITY_NONE, STOPBITS_ONE, EIGHTBITS
from time import sleep
import threading
from source.framework.pool import Pool


class PortRead(QObject):
    data_signal = pyqtSignal(str)

    def start(self):
        thread = threading.Thread(target=self.listen, args=())
        global exit_flag
        exit_flag = False
        thread.start()

    def stop(self):
        global exit_flag
        exit_flag = True
    
    def listen(self):
        with Serial(
                port=Pool.get('config').general.serial_port or 'COM3',
                baudrate=9600,
                parity=PARITY_NONE,
                stopbits=STOPBITS_ONE,
                bytesize=EIGHTBITS,
                timeout=0) as ser:
            print("connected to: " + ser.portstr)
            while True:
                sleep (1)
                x = str()
                for line in ser:
                    x += line.decode("utf-8")
                if x:
                    x = x.split('\x1b')[0].strip()
                    self.data_signal.emit(x)

                global exit_flag
                if exit_flag:
                    return str()
        
        
          
