from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.clock import Clock
from source import RandSource
import re

class Parser:
    def __init__(self,mainWidget):
        self.mainWidget = mainWidget

    def parseCom(self, args):
        command = args[0].lower()
        if command == 'add':
            if args[1].lower() == 'label':
                if len(args) > 2:
                    self.mainWidget.addWidget('Label',args[2])
            elif args[1].lower() == 'slider':
                if len(args) > 2:
                    self.mainWidget.addWidget('Slider',args[2])
        if command == 'remove':
            if args[1].lower() == 'widget':
                self.mainWidget.removeWidget(args[2])

class SliderNode(BoxLayout):
    def changeVal(self, value):
        self.ids['slider'].value = value

class LabelNode(BoxLayout):
    def changeVal(self, value):
        self.ids['value'].text = str(value)

class CommandPrompt(BoxLayout):
    def __init__(self,parser):
        super(CommandPrompt,self).__init__()
        self.parser = parser

    def checkCom(self):
        textinput = self.ids['textinput']
        if textinput.focus == False:
            self.parser.parseCom(re.split(" ",textinput.text))
            print(textinput.text)
            textinput.text = ''
            textinput.focus = True

class MainWidget(BoxLayout):
    def __init__(self):
        super(MainWidget,self).__init__()
        self.widgets = {}
        self.commandPrompt = CommandPrompt(Parser(self))
        self.ids.commandSpace.add_widget(self.commandPrompt)

    def addWidget(self, wType, name):
        if wType == 'Label':
            self.widgets[name] = LabelNode(id=name)
        elif wType == 'Slider':
            self.widgets[name] = SliderNode(id=name)

        app.sources[len(self.widgets)%2][1].append(name)

        self.ids.workSpace.add_widget(self.widgets[name])
        print(self.commandPrompt)

    def removeWidget(self, name):
        widget = self.widgets.pop(name,None)
        self.remove_widget(widget)

class MainApp(App):
    def __init__(self):
        super(MainApp,self).__init__()
        self.sources = [[RandSource('rand1'),[]],[RandSource('rand2',5),[]]]
        self.mainWidget = None

    def build(self):
        self.mainWidget = MainWidget()

        return self.mainWidget

    def checkSources(self,dt):
        for source in self.sources:
            retVal = source[0].checkVal()
            for bound in source[1]:
                self.mainWidget.widgets[bound].changeVal(retVal[2])


    def on_start(self):
        Clock.schedule_interval(self.checkSources,0.1)

if __name__ == '__main__':
    app = MainApp()
    app.run()
