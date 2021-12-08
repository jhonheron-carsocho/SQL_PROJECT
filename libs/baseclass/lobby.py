from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
import requests
from kivy.uix.relativelayout import RelativeLayout                  
from kivy.uix.carousel import Carousel
from kivymd_extensions.akivymd import *
from kivy.clock import Clock

Builder.load_file('./libs/kv/lobby.kv')

class Lobby(Screen):
    def on_enter(self):
        Clock.schedule_once(self.callback_function, 3)
        print('hiiiiii')

    def callback_function(self, dt):
        self.ids.board.load_next(mode='next')
        #time.sleep(3)
        Clock.schedule_once(self.callback_function, 3)


class OnBoarding(Screen):
    def on_enter(self):
        Clock.schedule_once(self.callback_function, 3)
        print('hiiiiii')

    def callback_function(self, dt):
        self.root.ids.board.load_next(mode='next')
        #time.sleep(3)
        Clock.schedule_once(self.callback_function, 3)

    def finish_callback(self):
        pass
