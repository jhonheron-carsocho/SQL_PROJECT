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
import mysql

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
                    try:
                        int(read_data[1])
                        int(read_data[-1])
                    except (TypeError, ValueError):
                        self.qr_reading = 'Invalid QR Code'
                    else:
                        self.qr_reading = 'Valid QR Code'
                        self.data_base(read_data)
                    time.sleep(3)

                else:
                    self.qr_reading = 'Invalid Qr Code'
                    time.sleep(3)

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

    def data_base(self, data):
        conn = mysql.connector.connect(
                    host = '127.0.0.1',
                    user = 'root',
                    passwd = '',
                    database = 'trial'
                    )
        
        cur = conn.cursor()
        
        # creates table and columns inside database
        cur.execute("""CREATE TABLE IF NOT EXISTS customers (
                            id MEDIUMINT NOT NULL AUTO_INCREMENT,
                            PRIMARY KEY (id),
                            name varchar(255),
                            age int,
                            address varchar (255),
                            number text,
                            time_in datetime,
                            time_out datetime,
                            status text)
                            """)
        
        dt = time.strftime("%Y-%m-%d %H:%M:%S")
        
        cur.execute(f"SELECT name FROM customers WHERE name = '{data[0]}' AND status = 'In'")
        res = cur.fetchall()
        
        if len(res) == 1:
            cur.execute(f"UPDATE customers SET time_out = '{dt}', status = 'Out'")
            
        else:
            cur.execute(f"""INSERT INTO customers (name, age, address, number,
                                 time_in, time_out, status) VALUES 
                                 (%s, %s, %s, %s, '{dt}', NULL, 'In')
                                 """, data)

        conn.commit()
        conn.close()