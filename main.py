from kivy.config import Config
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.uix.behaviors import DragBehavior, ButtonBehavior
from kivy.properties import ObjectProperty
from kivy.core.window import Window

import re
from Parser import Parser

class SliderMonitor(BoxLayout):
    pass

class NumberMonitor(BoxLayout):
    pass

class ConsoleWidget(DragBehavior, BoxLayout):
    def __init__(self):
        super(ConsoleWidget,self).__init__()
        self.active = False

    def handleInput(self):
        console = self.ids.readout.children[0]
        commandline = self.ids.commandline
        text = commandline.text

        commands = text.split(' ')
        parseReturn = app.parser.execute(commands[0],*commands[1:])
        console.text = console.text + parseReturn

        self.ids.commandline.text = ""
        self.ids.commandline.focus = True

class MainWidget(FloatLayout):
    def __init__(self):
        super(MainWidget,self).__init__()
        self._keyboard = Window.request_keyboard(None,self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.console = ConsoleWidget()
        self.monitorTypes = ['number','slider']
        self.monitors = {}

    def addMonitor(self,type,name,*args):
        if type == 'number':
            self.monitors[name] = NumberMonitor()
        elif type == 'slider':
            self.monitors[name] = SliderMonitor()

        self.monitors[name].ids.name.text = name
        self.ids.monitorSpace.add_widget(self.monitors[name])

    def removeMonitor(self,name,*args):
        self.ids.monitorSpace.remove_widget(self.monitors[name])
        del self.monitors[name]

    def _on_keyboard_down(self,keyboard,keycode,text,modifiers):
        if self.console.active == True:
            if keycode[1] == 'tab' :
                self._close_console()
            elif keycode[1] == 'enter':
                self.console.handleInput()
        elif self.console.active == False:
            if keycode[1] == 'tab':
                self._open_console()

    def _open_console(self):
        self.console.active = True
        self.add_widget(self.console)
        self.console.ids.commandline.focus = True

    def _close_console(self):
        self.console.active = False
        self.console.ids.commandline.text = ""
        self.remove_widget(self.console)

class MainApp(App):
    def __init__(self):
        super(MainApp,self).__init__()
        self.mainWidget = None
        self.parser = None

    def build(self):
        self.mainWidget = MainWidget()
        self.parser = Parser(self.mainWidget)
        return self.mainWidget

if __name__ == '__main__':
    app = MainApp()
    app.run()
