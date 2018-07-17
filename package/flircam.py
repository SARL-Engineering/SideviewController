# Handler for FLIR cameras using their proprietary PySpin wrapper
# Look into their PySpin API for implementation details, much of this code
# is copy-pasted in :)
import constants
import cv2
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
        self.im_passback = im_passback
        self.start_time = 0
        self.mutex = QtCore.QMutex()
        self.im_toggle = True

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

    def _to_np(self, image):
        # Converts an ImagePtr to a NumPy array
        try:
            data = image.GetData()

        except Exception as ex:
            print(ex)
        np_image = data.reshape((
            self.height,
            self.width
        ))
        return np_image

    def _init_spinvideo(self):
        # FLIR API video writer, kinda sucks tbh
        self.avi_recorder = PySpin.SpinVideo()

        # Set options
        option = PySpin.H264Option()
        option.frameRate = self.fps
        option.bitrate = 1000000
        option.height = self.images[0].GetHeight()
        option.width = self.images[0].GetWidth()
        output_fn = "{}_SIDEVIEW_CAM_{}".format(
            int(time.time()),
            self.cam.name
        )

        self.avi_recorder.Open("{}\{}{}".format(
            self.output_loc,
            output_fn,
            constants.OUTPUT_FILE_EXT
        ), option)

    # TODO: Freeze GUI while writing
    def _write_vid(self, **kwargs):
        print("Writing video...")
        try:
            for image in self.images:
                self.output.write(image)

        except Exception, error:
            print(str(error))
        print("Writing complete.")
        del self.images[:]
        self.output.release()

    def _append_image(self, **kwargs):
        self.images.append(kwargs["fr"])

    # TODO: Clean function and get rid of useless code
    def OnImageEvent(self, image):
        """This method defines an image event. In it, the image that triggered
        the event is converted and saved before incrementing the count. Please
        see Acquisition example for more in-depth comments on the acquisition
        of images.

        :param image: Image from event.
        :type image: ImagePtr
        :rtype: None
        """
        self.mutex.lock()
        frame = self._to_np(image)
        save_frame = frame.copy()  # frame to save that won't be overlaid

        # Initialize VideoWriter if recording starts
        if self.rec_state == constants.STATE_MW_RUN \
                and self.recording is False:
            self.recording = True
            self.start_time = time.time()

        if self.im_toggle:
            self.im_toggle = False

        else:
            self.im_toggle = True

        # Add frames if recording
        if self.rec_state == constants.STATE_MW_RUN and self.im_toggle:
            """im_worker = Worker(self._append_image, fr=save_frame)
            self.threadpool.start(im_worker)"""
            pass

        # Add text overlay
        if self.recording:
            cv2.putText(frame, constants.OVERLAY_REC,
                        constants.OVERLAY_FONT_POINT_LARGE,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        constants.OVERLAY_FONT_SCALE_LARGE,
                        constants.OVERLAY_FONT_REC_COLOR,
                        constants.OVERLAY_FONT_THICKNESS
                        )
        else:
            cv2.putText(frame, constants.OVERLAY_IDLE,
                        constants.OVERLAY_FONT_POINT_LARGE,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        constants.OVERLAY_FONT_SCALE_LARGE,
                        constants.OVERLAY_FONT_IDLE_COLOR,
                        constants.OVERLAY_FONT_THICKNESS
                        )

        # Release file if recording ends
        if self.recording and self.rec_state == constants.STATE_MW_IDLE:
            self.recording = False
            self._init_videowriter(
                fps=float(len(self.images) /
                          ((time.time() - self.start_time)))
            )
            worker = Worker(self._write_vid)
            self.threadpool.start(worker)

        image.Release()

        if (time.time() - self.timer)*1000 >= (1000/constants.CAM_FPS):
            frame = cv2.resize(frame, None, fx=0.5, fy=0.5,
                               interpolation=cv2.INTER_AREA)
            self.timer = time.time()
            self.im_passback.emit(self.cam, frame)

        self.mutex.unlock()

    def save_video(self):
        # Saves current list of images to file
        self.avi_recorder = PySpin.SpinVideo()

        # Set options
        option = PySpin.H264Option()
        option.frameRate = self.fps
        option.bitrate = 1000000
        option.height = self.images[0].GetHeight()
        option.width = self.images[0].GetWidth()
        output_fn = "{}_SIDEVIEW_CAM_{}".format(
            int(time.time()),
            self.cam.name
        )

        self.avi_recorder.Open("{}\{}".format(
                self.output_loc,
                output_fn,
            ), option)

        for i in range(len(self.images)):
            self.avi_recorder.Append(self.images[i])

        self.avi_recorder.Close()
