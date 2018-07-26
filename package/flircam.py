# Handler for FLIR cameras using their proprietary PySpin wrapper
# Look into their PySpin API for implementation details, much of this code
# is copy-pasted in :)
import constants
import cv2
import frameprocessor
from PyQt4 import QtCore
import PySpin
from threadworker import Worker
import time
import numpy as np


class ImageEventHandler(PySpin.ImageEvent):

    def __init__(self, flir_cam, cam, output_loc, im_passback):

        super(ImageEventHandler, self).__init__()

        nodemap = flir_cam.GetTLDeviceNodeMap()

        # Set internal state
        self.rec_state = constants.STATE_MW_IDLE
        self.recording = False
        self.cam = cam
        self.output_loc = output_loc
        self.output = None
        self.parent_queue = None
        self.im_passback = im_passback
        self.start_time = 0
        self.mutex = QtCore.QMutex()
        self.im_toggle = True
        self.im_callback = None

        # Save dimensions
        self.height = flir_cam.Height()
        self.width = flir_cam.Width()
        self.fps = flir_cam.AcquisitionFrameRate.GetValue()

        self.threadpool = QtCore.QThreadPool()
        self.timer = time.time()

        # Images that will become a saved video
        self.images = []

        # Retrieve device serial number
        node_device_serial_number = PySpin.CStringPtr(
            nodemap.GetNode('DeviceSerialNumber'))

        if PySpin.IsAvailable(node_device_serial_number) and PySpin.IsReadable(
                node_device_serial_number):
            self._device_serial_number = node_device_serial_number.GetValue()

        del flir_cam

    def _init_videowriter(self, fps=constants.CAM_FPS):
        # OpenCV implementation
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        output_fn = "{}_SIDEVIEW_CAM_{}".format(
            int(time.time()),
            self.cam.name
        )
        self.output = cv2.VideoWriter(
            "{}\{}{}".format(
                self.output_loc,
                output_fn,
                constants.OUTPUT_FILE_EXT
            ),
            fourcc,
            fps,
            (self.width,
             self.height),
            isColor=False
        )

    def _to_np(self, image, height, width):
        # Converts an ImagePtr to a NumPy array
        data = image.GetData()

        if len(data) != height*width:
            return np.ones((height, width))

        np_image = data.reshape((
            height,
            width
        ))
        return np_image
