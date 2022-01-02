from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.factory import Factory
import mysql.connector
from kivy.uix.floatlayout import FloatLayout
from kivy.animation import Animation

Builder.load_file('./libs/kv/login.kv')


class Loading(FloatLayout):
    angle = NumericProperty(0)
    def __init__(self, **kwargs):
        super(Loading, self).__init__(**kwargs)
        anim = Animation(angle = 360, duration=2) 
        anim += Animation(angle = 360, duration=2)
        anim.repeat = True
        anim.start(self)

    def on_angle(self, item, angle):
        if angle == 360:
            item.angle = 0

class Login(Screen):
    pass

class LoginForm(FloatLayout):
    usr_name = ObjectProperty(None)
    usr_pass = ObjectProperty(None)

    def usr_login(self):
        if self.usr_name.text == 'admin' and self.usr_pass.text == 'admin':
            self.usr_name.text = ''
            self.usr_pass.text = ''
            return True
        else: 
            self.usr_name.text = ''
            self.usr_pass.text = ''
            return False
        

    # def create_db(self):
    #     db = mysql.connector.connect(
    #         host='localhost',
    #         user='root',
    #         passwd='1234',
    #         database='storeDB'
    #     )

    #     mycursor = db.cursor()

    #     mycursor.execute("""CREATE TABLE IF NOT EXISTS customers (
    #             id INT NOT NULL AUTO_INCREMENT,
    #             name VARCHAR(250) NOT NULL UNIQUE,
    #             address VARCHAR(250) NOT NULL,
    #             number INT(11) NOT NULL UNIQUE,
    #             timein DATETIME,
    #             timeout DATETIME,
    #             status VARCHAR(11),
    #             PRIMARY KEY (id)
    #         );
    #     """)

    #     mycursor.execute("DESCRIBE customers")

    #     for x in mycursor:
    #         print(x)

    