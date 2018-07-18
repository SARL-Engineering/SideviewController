import cv2


class FrameWriter(object):

    def __init__(self, height, width, fps, fn, images, color=True):
        super(FrameWriter, self).__init__()
        self.height = height
        self.width = width
        self.fps = fps
        self.fn = fn
        self.images = images

        self.output = None
