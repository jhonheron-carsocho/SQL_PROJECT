import threading
import numpy as np
from pyzbar.pyzbar import decode
from functools import partial
import cv2
from kivy.app import App
from kivy.clock import Clock
import time
from kivy.graphics.texture import Texture
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty

Builder.load_file('./libs/kv/scanner.kv')


class Scanner(Screen):
    qr_reading = StringProperty('')

    def __init__(self, **kwargs):
        super(Scanner, self).__init__(**kwargs)
        self.record_scene = True
        
    def on_enter(self, *args):
        threading.Thread(target=self.start_cam, daemon=True).start()

    def start_cam(self):
        cam = cv2.VideoCapture(0)

        while (self.record_scene):
            ret, img = cam.read()
            img_flip = cv2.flip(img,1)
            if decode(img) == []:
                self.qr_reading = ''

            for barcode in decode(img_flip):
                data_ret = barcode.data.decode('utf-8')
                read_data = data_ret.split(';')

                find_array = np.array([barcode.polygon],np.int32)
                find_array = find_array.reshape((-1,1,2))
                cv2.polylines(img_flip, [find_array], True, (255,0,255),5)
                find_array2 = barcode.rect
                cv2.putText(img_flip, read_data[0], (find_array2[0], find_array2[1]),
                            cv2.FONT_HERSHEY_SIMPLEX, 2,(255,0,255),2)
                
                print(read_data)
                if len(read_data) == 4:
                    self.qr_reading = 'Valid QR Code'
                    time.sleep(5)
                else:
                    self.qr_reading = 'Invalid Qr Code'

            Clock.schedule_once(partial(self.display_frame, img_flip))
            
            cv2.waitKey(1)

        cam.release()

    def stop_respo(self):
        self.record_scene = False

    def display_frame(self, frame, dt):
        texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture.blit_buffer(frame.tobytes(order=None), colorfmt='bgr', bufferfmt='ubyte')
        texture.flip_vertical()
        self.ids.cam_respo.texture = texture
