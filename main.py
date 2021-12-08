from kivy.config import Config
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.properties import StringProperty, NumericProperty
from libs.baseclass import login, scanner, lobby
from kivy.core.window import Window



class MyApp(MDApp):
    product_category = StringProperty()
    log_usr = StringProperty()
    product_index = NumericProperty()
    selected = StringProperty('')
    selected2 = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'You Trace Me'
        self.theme_cls.primary_palette = "Green"

    def build(self):
        kv_run = Builder.load_file("main.kv")
        return kv_run


    def colors(self, color_code):
        if color_code == 0:
            color_rgba = '#f3cdc0'
        elif color_code == 1:
            color_rgba = '#00539CFF'
        elif color_code == 2:
            color_rgba = '#4a2c27'

        return color_rgba

    def show_screen(self, name):
        self.root.current = 'lobby'
        self.root.get_screen('lobby').ids.manage.current = name
        return True


if __name__ == "__main__":

    MyApp().run()


#from kivy.config import Config
#from kivymd.app import MDApp
#from kivy.lang.builder import Builder
#from kivy.properties import StringProperty, NumericProperty
#from libs.baseclass import login, scanner
#from kivy.core.window import Window

#Window.fullscreen = True

#class MyApp(MDApp):
#    product_category = StringProperty()
#    log_usr = StringProperty()
#    product_index = NumericProperty()
#    selected = StringProperty('')
#    selected2 = StringProperty('')

#    def __init__(self, **kwargs):
#        super().__init__(**kwargs)
#        self.title = 'BASTA'
        
#    def build(self):
#        kv_run = Builder.load_file("main.kv")
#        return kv_run

#    # def on_start(self):
#    #     if self.get_account() is not None and self.get_account() != []:
#    #         print(self.get_account())
#    #         self.root.current = 'nav_screen'
#    #     else:
#    #         self.root.current = 'login'

#    # def get_account(self):
#    #     try:
#    #         conn = sqlite3.connect('./assets/data/app_data.db')
#    #         cursor = conn.cursor()
#    #         cursor.execute('SELECT * FROM accounts WHERE status = "active"')
#    #         data = cursor.fetchone()
#    #     except (AttributeError, sqlite3.OperationalError):
#    #         data = None
#    #     return data

#    def colors(self, color_code):
#        if color_code == 0:
#            color_rgba = '#f3cdc0'
#        elif color_code == 1:
#            color_rgba = '#00539CFF'
#        elif color_code == 2:
#            color_rgba = '#4a2c27'

#        return color_rgba

#    def show_screen(self, name):
#        self.root.current = 'login'
#        self.root.get_screen('login').ids.manage.current = name
#        return True


#if __name__ == "__main__":
#    Config.set("graphics", "width", "1920")
#    Config.set("graphics", "height", "1080")
#    Config.write()
#    MyApp().run()
