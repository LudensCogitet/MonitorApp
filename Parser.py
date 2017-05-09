class Parser:
    command = {}

    def __init__(self, mainWidget):
        self.mainWidget = mainWidget

    def execute(self,func,*args):
        func = func.lower()
        if func not in Parser.command:
            return "\nUnrecognized command " + func
        else:
            return Parser.command[func](self.mainWidget,*args)

    def _addFunc(name,function):
        name = name.lower()
        if name in Parser.command:
            print('\nWarning. Overwriting previously existing command function: \"'+ name +\
                  '\" in Parser.')
        Parser.command[name] = function

def _addMonitor(mainWidget, type, name, *args):
    type = type.lower()

    if type not in mainWidget.monitorTypes:
        return "\nCannot add monitor of type \"" + type + "\". Type is unknown."
    elif name in mainWidget.monitors:
        return "\nCannot add monitor named \"" + name + "\". Name already in use."
    else:
        mainWidget.addMonitor(type,name,*args)

    return "\nAdded monitor of type "+ type + " named \"" + name +"\""

Parser._addFunc("add", _addMonitor)

def _removeMonitor(mainWidget, name, *args):
        if name not in mainWidget.monitors:
            return "\nCannot remove monitor \"" + name + "\". No such monitor."
        else:
            mainWidget.removeMonitor(name,*args)
            return "\nRemoved monitor \"" + name + "\""

Parser._addFunc("remove",_removeMonitor)

if __name__ == '__main__':
    print(Parser.execute("add","Bob","bob1"))
    print(Parser.execute("remove","bob1"))
    print(Parser.execute("Steve","Bob","bob1"))
