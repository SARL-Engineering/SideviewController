class Camera(object):
    
    def __init__(self, name, link, resolution):
        super(Camera, self).__init__()
        self.name = name
        self.link = link
        self.resolution = resolution


class Screen(object):
    
    def __init__(self, name, monitor=None):
        super(Screen, self).__init__()
        self.name = name
        self.monitor = monitor


class Video(Screen):

    def __init__(self, name, link, monitor=None):
        super(Video, self).__init__(name, monitor)
        self.link = link


class FlatScreen(Screen):

    def __init__(self, name, color, monitor=None):
        super(FlatScreen, self).__init__(name, monitor)
        self.color = color


class COMDevice(object):

    def __init__(self, name, link, signal, baud_rate, rules):
        super(COMDevice, self).__init__()
        self.name = name
        self.link = link
        self.signal = signal
        self.baud_rate = baud_rate
        self.rules = rules


class Rule(object):

    def __init__(self, num, time_intv, isAt=True):
        super(Rule, self).__init__()
        self.num = num
        self.time_intv = time_intv
        if isAt:
            self.isAt = True
            self.isEvery = False

        else:
            self.isAt = False
            self.isEvery = True
