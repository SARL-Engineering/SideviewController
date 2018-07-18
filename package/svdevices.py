# TODO: Implement generic serial comm device object
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


class SerialDevice(object):

    def __init__(self, name, link, action):
        super(SerialDevice, self).__init__()
        self.name = name
        self.link = link
        self.action = action
