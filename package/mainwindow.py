import constants
import ctypes
import customdialog
import cv2
import flircam
import svdevices
from threadworker import Worker
from ui import mainwindow_ui
from moviepy.video.io.VideoFileClip import VideoFileClip
from PyQt4 import QtGui, QtCore
from PyQt4.phonon import Phonon
import PySpin
import sys
import time


class MainWindow(QtGui.QMainWindow, mainwindow_ui.Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.cams, self.screens, self.devs = [], [], []
        self.view_dialogs = {}
        self.max_video_length = 0

        self._create_icons()
        self._set_labels()
        self._set_default_gui_state()
        self._set_icons()
        self._connect_signals()
        self._start_threadpool()

        self.refresh_gui()
        self.show()

    def _create_icons(self):
        # creates QIcons for open use in other widgets
        self.icon_play = QtGui.QIcon()
        self.icon_play.addPixmap(QtGui.QPixmap(constants.ICON_PLAYBUTTON))
        self.icon_play.addPixmap(
            QtGui.QPixmap(constants.ICON_PLAYBUTTON_LIGHT),
            QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.icon_play.addPixmap(
            QtGui.QPixmap(constants.ICON_PLAYBUTTON_DARK),
            QtGui.QIcon.Active)
        self.icon_play.addPixmap(
            QtGui.QPixmap(constants.ICON_PLAYBUTTON_GRAY),
            QtGui.QIcon.Disabled)

        self.icon_stop = QtGui.QIcon()
        self.icon_stop.addPixmap(QtGui.QPixmap(constants.ICON_STOPBUTTON))
        self.icon_stop.addPixmap(
            QtGui.QPixmap(constants.ICON_STOPBUTTON_LIGHT),
            QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.icon_stop.addPixmap(
            QtGui.QPixmap(constants.ICON_STOPBUTTON_DARK),
            QtGui.QIcon.Active)
        self.icon_stop.addPixmap(
            QtGui.QPixmap(constants.ICON_STOPBUTTON_GRAY),
            QtGui.QIcon.Disabled)

    def _set_labels(self):
        # Sets text for all labels, buttons, etc.
        self.setWindowTitle(constants.APP_TITLE)

        self.labelOutput.setText(constants.LABEL_LABEL_OUTPUT)
        self.labelControls.setText(constants.LABEL_LABEL_CONTROLS)
        self.labelLoops.setText(constants.LABEL_LABEL_LOOPS)

        self.pbOutput.setText(constants.LABEL_PB_OUTPUT)
        self.pbCamAdd.setText(constants.LABEL_PB_ADD)
        self.pbCamEdit.setText(constants.LABEL_PB_EDIT)
        self.pbCamOpen.setText(constants.LABEL_PB_OPEN)
        self.pbCamRemove.setText(constants.LABEL_PB_REMOVE)
        self.pbScreenAdd.setText(constants.LABEL_PB_ADD)
        self.pbScreenEdit.setText(constants.LABEL_PB_EDIT)
        self.pbScreenOpen.setText(constants.LABEL_PB_OPEN)
        self.pbScreenRemove.setText(constants.LABEL_PB_REMOVE)
        self.pbDevicesAdd.setText(constants.LABEL_PB_ADD)
        self.pbDevicesEdit.setText(constants.LABEL_PB_EDIT)
        self.pbDevicesOpen.setText(constants.LABEL_PB_OPEN)
        self.pbDevicesRemove.setText(constants.LABEL_PB_REMOVE)

        self.rbCRLoops.setText(constants.LABEL_RB_LOOP)
        self.rbCRTime.setText(constants.LABEL_RB_TIME)

        self.tabGroup.setTabText(constants.IDX_TAB_CAM,
                                 constants.LABEL_TAB_CAM)
        self.tabGroup.setTabText(constants.IDX_TAB_SCREEN,
                                 constants.LABEL_TAB_SCREEN)
        self.tabGroup.setTabText(constants.IDX_TAB_DEVICES,
                                 constants.LABEL_TAB_DEV)

    # TODO: Implement configuration saving and opening
    def _set_default_gui_state(self):
        # Sets default states of all gui elements
        self.tbControls.setIcon(self.icon_play)
        self.actionStop.setEnabled(False)
        self.lcdControls.display("00:00:00.000")

        self.progressBar.setValue(0)
        self.teCSDuration.setMinimumTime(QtCore.QTime(0, 0, 1))
        self.max_video_length = 0
        self.state = constants.STATE_MW_IDLE

    def _set_icons(self):
        # Sets icons in window and taskbar
        self.appid = constants.APP_TITLE
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(self.appid)

    def _connect_signals(self):
        # Connects signals to all appropriate gui elements
        self.destroyed.connect(self._destroy_dialogs)

        self.pbOutput.clicked.connect(self.select_output_folder)
        self.rbCRTime.clicked.connect(self.refresh_gui)
        self.rbCRLoops.clicked.connect(self.refresh_gui)
        self.tbControls.clicked.connect(self.toggle_run)

        self.tabGroup.currentChanged.connect(self.refresh_gui)
        self.pbCamAdd.clicked.connect(self.add_cam)
        self.pbCamEdit.clicked.connect(self.edit_cam)
        self.pbCamRemove.clicked.connect(self.remove_gen_obj)
        self.pbCamOpen.clicked.connect(self.open_cam)
        self.pbScreenAdd.clicked.connect(self.add_screen)
        self.pbScreenEdit.clicked.connect(self.edit_screen)
        self.pbScreenOpen.clicked.connect(self.open_screen)
        self.pbScreenRemove.clicked.connect(self.remove_gen_obj)
        self.pbDevicesRemove.clicked.connect(self.remove_gen_obj)
        self.lwCam.clicked.connect(self.refresh_tab_buts)
        self.lwScreen.clicked.connect(self.refresh_tab_buts)
        self.lwDevices.clicked.connect(self.refresh_tab_buts)

        self.actionStart.triggered.connect(self.toggle_run)
        self.actionStop.triggered.connect(self.toggle_run)
        self.actionCamera.triggered.connect(self.add_cam)
        self.actionVideo.triggered.connect(self.add_screen)

    def _start_threadpool(self):
        # Start handler for future threads
        self.threadpool = QtCore.QThreadPool()

    def _run_disable(self):
        # Disables all elements that shouldn't be used while recording
        self.pbOutput.setEnabled(False)
        self.rbCRTime.setEnabled(False)
        self.rbCRLoops.setEnabled(False)
        self.leOutput.setEnabled(False)
        self.teCSDuration.setEnabled(False)
        self.spinLoops.setEnabled(False)
        self.progressBar.setEnabled(True)

        self.pbCamAdd.setEnabled(False)
        self.pbCamEdit.setEnabled(False)
        self.pbCamRemove.setEnabled(False)
        self.pbScreenAdd.setEnabled(False)
        self.pbScreenEdit.setEnabled(False)
        self.pbScreenRemove.setEnabled(False)
        self.pbDevicesAdd.setEnabled(False)
        self.pbDevicesEdit.setEnabled(False)
        self.pbDevicesRemove.setEnabled(False)

        self.actionNew_Config.setEnabled(False)
        self.actionOpen_Config.setEnabled(False)
        self.actionSave_Config.setEnabled(False)
        self.actionSave_Config_As.setEnabled(False)
        self.actionStart.setEnabled(False)
        self.actionStop.setEnabled(True)
        self.actionCamera.setEnabled(False)
        self.actionVideo.setEnabled(False)

    def _idle_enable(self):
        # Enables all elements after recording ends
        self.pbOutput.setEnabled(True)
        self.rbCRTime.setEnabled(True)
        self.rbCRLoops.setEnabled(True)
        self.leOutput.setEnabled(True)
        self.teCSDuration.setEnabled(True)
        self.spinLoops.setEnabled(True)
        self.progressBar.setEnabled(False)

        self.pbCamAdd.setEnabled(True)
        self.pbCamEdit.setEnabled(True)
        self.pbCamRemove.setEnabled(True)
        self.pbScreenAdd.setEnabled(True)
        self.pbScreenEdit.setEnabled(True)
        self.pbScreenRemove.setEnabled(True)
        self.pbDevicesAdd.setEnabled(True)
        self.pbDevicesEdit.setEnabled(True)
        self.pbDevicesRemove.setEnabled(True)

        self.actionNew_Config.setEnabled(True)
        self.actionOpen_Config.setEnabled(True)
        self.actionSave_Config.setEnabled(True)
        self.actionSave_Config_As.setEnabled(True)
        self.actionStart.setEnabled(True)
        self.actionStop.setEnabled(False)
        self.actionCamera.setEnabled(True)
        self.actionVideo.setEnabled(True)

    def _is_prerun_error(self):
        # Returns True if there exists some missing information before a run
        if len(self.leOutput.text()) == 0:
            self.show_dialog_no_output()
            self.pbOutput.setFocus()
            return True

        elif self.rbCRLoops.isChecked() and self.max_video_length == 0:
            self.show_dialog_no_video()
            self.tabGroup.setCurrentIndex(constants.IDX_TAB_SCREEN)
            self.pbScreenAdd.setFocus()
            return True

        elif svdevices.Camera not in \
                [type(viewd.obj) for key, viewd in self.view_dialogs.items()]:
            self.show_dialog_no_cam()
            self.tabGroup.setCurrentIndex(constants.IDX_TAB_CAM)
            return True

        return False

    def _valid_add(self, new_obj):
        # Checks that a new device object has a unique name and all fields
        # filled out
        if new_obj.name in [cam.name for cam in self.cams] \
            or new_obj.name in [screen.name for screen in self.screens] \
            or new_obj.name in [dev.name for dev in self.devs]:
                self.show_dialog_dup_name()
                return False

        if type(new_obj) is svdevices.Camera:
            for cam in self.cams:
                if cam.link == new_obj.link:
                    self.show_dialog_cam_taken(cam.name)
                    return False

        if type(new_obj) is svdevices.Camera and \
            (new_obj.name == "" or
             new_obj.link == "" or
             new_obj.resolution == ""):
            self.show_dialog_blank_fields()
            return False

        elif type(new_obj) is svdevices.Video and \
                (new_obj.name == "" or
                 new_obj.link == "" or
                new_obj.monitor == ""):
            self.show_dialog_blank_fields()
            return False

        elif type(new_obj) is svdevices.FlatScreen and \
                (new_obj.name == "" or
                 new_obj.color == "" or
                new_obj.monitor == ""):
            self.show_dialog_blank_fields()
            return False

        return True

    def _run_timer(self, **kwargs):
        kwargs["cb_str_passback"].emit("00:00:00.000")
        start_time = time.time()
        while True:
            time.sleep(0.05)
            current_time = time.time()
            d_time = current_time - start_time
            kwargs["cb_str_passback"].emit(time.strftime(
                "%H:%M:%S.{0:03d}".format(
                    int(round(d_time % 1000, 3) * 1000) % 1000),
                time.gmtime(d_time)))

            if self._end_timer(d_time, kwargs["cb_int_passback"]):
                break

    def _update_progbar(self, cent_val):
        # Mid-thread slot to write progress to progress bar
        self.progressBar.setValue(cent_val)

    def _update_timer(self, new_time):
        # Mid-thread slot to write time to lcd display
        self.lcdControls.display(new_time)

    def _end_timer(self, d_time, passback):
        # Checks for condition to end timer thread
        end_time = sum(x * int(t) for x, t in zip(
            [3600, 60, 1],
            self.teCSDuration.text().split(":")
        ))
        loop_time = int(self.spinLoops.value()) * self.max_video_length

        # Update progress
        if self.rbCRTime.isChecked():
            passback.emit((d_time / end_time)*100)

        elif self.rbCRLoops.isChecked():
            passback.emit((d_time / loop_time)*100)

        # Check if recording is ended
        if self.state == constants.STATE_MW_IDLE \
                or (self.rbCRTime.isChecked() and d_time >= end_time) \
                or (self.rbCRLoops.isChecked() and d_time >= loop_time):

            self.state = constants.STATE_MW_IDLE
            self.tbControls.setIcon(self.icon_play)
            self._idle_enable()
            return True

        return False

    def _destroy_dialogs(self):
        # Closes all open view dialog windows
        for name, dialog in self.view_dialogs.items():
            dialog.close()

    def _del_view_dialog(self, name):
        # Helper function to connect to dialog.finished() signals
        del self.view_dialogs[name]
        if self.state == constants.STATE_MW_RUN:
            self.toggle_run()
        self._update_max_dur()
        self.refresh_tab_buts()

    def _paint_cam_frame(self, cam, frame):
        # Slot takes a frame, turns it into a pixmap, and sets it
        if cam.name in self.view_dialogs:
            dialog = self.view_dialogs[cam.name]

        else:
            return

        # Convert array to pixmap
        if len(frame.shape) == 3:
            image = QtGui.QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                QtGui.QImage.Format_RGB888
            ).rgbSwapped()
            pixmap = QtGui.QPixmap.fromImage(image)

        elif len(frame.shape) == 2:
            image = QtGui.QImage(
                frame,
                frame.shape[1],
                frame.shape[0],
                QtGui.QImage.Format_Indexed8
            )
            pixmap = QtGui.QPixmap.fromImage(image)

        # set in dialog
        dialog.camFrame.setPixmap(pixmap)

    # TODO: Cam freezes when running multiple cameras simultaneously
    def _handle_cam(self, cam, **kwargs):
        # Opens camera feed processing to be used in separate thread
        cap = cv2.VideoCapture(int(cam.link[3:]))
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, int(cam.resolution.split("x")[0]))
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, int(cam.resolution.split("x")[1]))
        cap.set(cv2.CAP_PROP_FPS, constants.CAM_FPS)

        recording = False   # Flag indicating when to use VideoWriter
        output = None
        images = []
        start_time = 0

        while cap.isOpened() and cam.name in self.view_dialogs.keys():
            ret, frame = cap.read()

            if ret:

                time.sleep(0.01)

                # Create copy to avoid saving overlaid frame
                save_frame = frame.copy()

                # Initialize VideoWriter if recording starts
                if self.state == constants.STATE_MW_RUN \
                        and recording is False:
                    recording = True
                    # output = self._get_video_writer(cam)
                    start_time = time.time()

                # Add frames if recording
                if self.state == constants.STATE_MW_RUN :#and output != None:
                    images.append(save_frame)
                    # output.write(frame)

                # Add text overlay
                if recording:
                    cv2.putText(frame, constants.OVERLAY_REC,
                                constants.OVERLAY_FONT_POINT,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                constants.OVERLAY_FONT_SCALE,
                                constants.OVERLAY_FONT_REC_COLOR,
                                constants.OVERLAY_FONT_THICKNESS
                                )
                else:
                    cv2.putText(frame, constants.OVERLAY_IDLE,
                                constants.OVERLAY_FONT_POINT,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                constants.OVERLAY_FONT_SCALE,
                                constants.OVERLAY_FONT_IDLE_COLOR,
                                constants.OVERLAY_FONT_THICKNESS
                                )

                # Release file if recording ends
                if recording and self.state == constants.STATE_MW_IDLE:#\
                        #and output != None:
                    recording = False
                    end_time = time.time()
                    output = self._get_video_writer(
                        cam,
                        fps=float(len(images) / (end_time - start_time))
                    )
                    for image in images:
                        time.sleep(0.01)
                        output.write(image)

                    output.release()

                kwargs["cb_obj_passback"].emit(cam, frame)

        cap.release()
        if output is not None:
            output.release()

    def _handle_flir_cam(self, cam, **kwargs):
        # Opens FLIR camera feed processing to be used in separate thread

        # Get FLIR Camera object
        flir_cam, cam_list, system = self._get_flir_cam(cam)

        # Initialize camera
        flir_cam.Init()

        # Retrieve GenICam nodemap
        nodemap = flir_cam.GetNodeMap()

        # Set FPS
        # flir_cam.AcquisitionFrameRate.SetValue(constants.CAM_FPS)

        # Configure image events
        image_event_handler = flircam.ImageEventHandler(
            flir_cam,
            cam,
            self.leOutput.text(),
            kwargs["cb_obj_passback"]
        )
        flir_cam.RegisterEvent(image_event_handler)

        # Set acquisition mode to continuous
        node_acq_mode = PySpin.CEnumerationPtr(nodemap.GetNode(
            "AcquisitionMode"))
        node_acq_mode_cont = node_acq_mode.GetEntryByName("Continuous")
        acq_mode_cont = node_acq_mode_cont.GetValue()
        node_acq_mode.SetIntValue(acq_mode_cont)

        # Begin collecting images
        flir_cam.BeginAcquisition()

        # Collect images as long as dialog is open
        while cam.name in self.view_dialogs.keys():

            time.sleep(0.01)
            # Initialize VideoWriter if recording starts
            image_event_handler.rec_state = self.state

        # End collection and reset image events
        """if image_event_handler.output is not None:
            image_event_handler.output.release()"""
        flir_cam.EndAcquisition()
        flir_cam.UnregisterEvent(image_event_handler)

        # De-initialize camera
        flir_cam.DeInit()

        # Clean up other objects that don't auto garbage-collect
        del flir_cam
        cam_list.Clear()
        system.ReleaseInstance()

    def _get_flir_cam(self, cam_obj):
        # Takes data from Camera object to get a PySpin.Camera object
        # Retrieve singleton reference to system object
        system = PySpin.System.GetInstance()

        # Retrieve list of cameras from the system
        cam_list = system.GetCameras()

        for i, flir_cam in enumerate(cam_list):

            nodemap_tldevice = flir_cam.GetTLDeviceNodeMap()
            node_device_information = PySpin.CCategoryPtr(
                nodemap_tldevice.GetNode('DeviceInformation'))
            features = node_device_information.GetFeatures()

            for feature in features:

                node_feature = PySpin.CValuePtr(feature)
                if node_feature.GetName() == "DeviceID":

                    match_str = "FLIR cam {}".format(node_feature.ToString())
                    if match_str == cam_obj.link:
                        return flir_cam, cam_list, system

    def _get_video_writer(self, cam, fps=constants.CAM_FPS):
        # Generates VideoWriter object for saving camera feed frames
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        output_loc = self.leOutput.text()
        output_fn = "{}_SIDEVIEW_CAM_{}".format(
            int(time.time()),
            cam.name
        )
        output = cv2.VideoWriter(
            "{}\{}{}".format(
                output_loc,
                output_fn,
                constants.OUTPUT_FILE_EXT
            ),
            fourcc,
            fps,
            (int(cam.resolution.split("x")[0]),
             int(cam.resolution.split("x")[1])),
            isColor=True
        )
        return output

    def _handle_video(self, media_obj, **kwargs):
        # Updates video ViewDialog when recording begins
        # Update max video length
        """fn = str(media_obj.currentSource().fileName())
        clip = VideoFileClip(fn)
        self.max_video_length = clip.duration"""
        self._update_max_dur()

        playing = True  # Flag indicating when the video is playing

        while kwargs["video_name"] in self.view_dialogs.keys():

            time.sleep(0.01)

            # Stop playing if currently playing and state goes to idle
            if self.state == constants.STATE_MW_IDLE and playing:
                playing = False
                media_obj.stop()

                # Scoot over the first frame-ish
                media_obj.play()
                media_obj.pause()

            # Start playing if idle and state goes to run
            if self.state == constants.STATE_MW_RUN and not playing:
                playing = True
                media_obj.play()

    def _update_max_dur(self):
        # Updates maximum duration video based on open ViewDialogs
        self.max_video_length = 0
        for _, dialog in self.view_dialogs.items():

            if type(dialog.obj) == svdevices.Video:

                clip = VideoFileClip(str(dialog.obj.link))

                if self.max_video_length < clip.duration:
                    self.max_video_length = clip.duration

    def closeEvent(self, event):
        self._destroy_dialogs()
        event.accept()

    def select_output_folder(self):
        # Populate output box with a directory
        directory = QtGui.QFileDialog.getExistingDirectory(
            None,
            constants.PROMPT_FOLDER_SELECT,
            "",
            QtGui.QFileDialog.ShowDirsOnly
        )
        self.leOutput.setText(directory)

    def refresh_gui(self):
        # Update elements to correct values and ability/disability
        if self.state == constants.STATE_MW_RUN:
            self._run_disable()
            return

        #  Update radio buttons
        if self.rbCRLoops.isChecked():
            self.spinLoops.setEnabled(True)
            self.teCSDuration.setEnabled(False)

        elif self.rbCRTime.isChecked():
            self.spinLoops.setEnabled(False)
            self.teCSDuration.setEnabled(True)

        else:
            self.rbCRTime.click()

        # Manage tabbed button availability based on listwidget selection
        if self.tabGroup.currentIndex() == constants.IDX_TAB_CAM:
            if len(self.lwCam.selectedItems()) < 1:
                self.lwCam.setCurrentRow(-1)
                self.pbCamEdit.setEnabled(False)
                self.pbCamOpen.setEnabled(False)
                self.pbCamRemove.setEnabled(False)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_SCREEN:
            if len(self.lwScreen.selectedItems()) < 1:
                self.lwCam.setCurrentRow(-1)
                self.pbScreenEdit.setEnabled(False)
                self.pbScreenOpen.setEnabled(False)
                self.pbScreenRemove.setEnabled(False)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_DEVICES:
            if len(self.lwDevices.selectedItems()) < 1:
                self.lwCam.setCurrentRow(-1)
                self.pbDevicesEdit.setEnabled(False)
                self.pbDevicesOpen.setEnabled(False)
                self.pbDevicesRemove.setEnabled(False)

        # Populate device lists
        self.lwCam.clear()
        self.lwScreen.clear()
        self.lwDevices.clear()
        for cam in self.cams:
            self.lwCam.addItem(cam.name)

        for screen in self.screens:
            self.lwScreen.addItem(screen.name)

        for dev in self.devs:
            self.lwDevices.addItem(dev.name)

    def refresh_tab_buts(self):
        # Duplicate code from refresh_gui() for simplified button ability
        # Manage tabbed button availability based on listwidget selection
        if self.tabGroup.currentIndex() == constants.IDX_TAB_CAM:
            selected_item = self.lwCam.item(self.lwCam.currentRow())
            if selected_item is not None \
                    and str(selected_item.text()) in self.view_dialogs.keys():
                self.pbCamEdit.setEnabled(False)
                self.pbCamOpen.setEnabled(False)
                self.pbCamRemove.setEnabled(False)

            else:
                self.pbCamEdit.setEnabled(True)
                self.pbCamOpen.setEnabled(True)
                self.pbCamRemove.setEnabled(True)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_SCREEN:
            selected_item = self.lwScreen.item(
                self.lwScreen.currentRow()
            )

            if selected_item is not None \
                    and str(selected_item.text()) in self.view_dialogs.keys():
                self.pbScreenEdit.setEnabled(False)
                self.pbScreenOpen.setEnabled(False)
                self.pbScreenRemove.setEnabled(False)

            else:
                self.pbScreenEdit.setEnabled(True)
                self.pbScreenOpen.setEnabled(True)
                self.pbScreenRemove.setEnabled(True)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_DEVICES:
            self.pbDevicesEdit.setEnabled(True)
            self.pbDevicesOpen.setEnabled(True)
            self.pbDevicesRemove.setEnabled(True)

    # TODO: Move static dialog functions to new file
    def show_dialog_no_output(self):
        # Shows dialog when user tries to run w/o output directory
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_NO_OUTPUT)
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def show_dialog_no_video(self):
        # Shows dialog when user tries to run w/loop termination and no video
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_NO_VIDEO)
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def show_dialog_no_cam(self):
        # Shows dialog when user tries to run w/o a camera open
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_NO_CAM)
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def show_dialog_dup_name(self):
        # Shows dialog when user tries to create a device with an already
        # existing name
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_DUP_NAME)
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def show_dialog_blank_fields(self):
        # Shows a dialog when a user tries to create a device without filling
        # out all of the fields
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_BLANK_FIELDS)
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def show_dialog_cam_taken(self, cam_name):
        # Shows a dialog when a user tries to create a camera with a link
        # already being used
        dialog = QtGui.QMessageBox()
        dialog.setIcon(QtGui.QMessageBox.Critical)
        dialog.setText(constants.DIALOG_MESSAGE_CAM_TAKEN.format(cam_name))
        dialog.setWindowTitle(constants.DIALOG_TITLE_ERROR)
        dialog.setStandardButtons(QtGui.QMessageBox.Ok)
        dialog.exec_()

    def toggle_run(self):
        # Switches between recording and ending the recording
        if self.state == constants.STATE_MW_RUN:
            self.state = constants.STATE_MW_IDLE
            self.tbControls.setIcon(self.icon_play)
            self._idle_enable()

        elif self.state == constants.STATE_MW_IDLE:
            if self._is_prerun_error():
                return
            self.state = constants.STATE_MW_RUN
            self.tbControls.setIcon(self.icon_stop)
            self._run_disable()
            self.start_timer()

        self.refresh_gui()

    def start_timer(self):
        # Starts new thread updating runtime
        worker = Worker(self._run_timer)
        worker.signals.int_passback.connect(self._update_progbar)
        worker.signals.str_passback.connect(self._update_timer)
        self.threadpool.start(worker)

    # TODO: Add framerate as a field
    # TODO: Poll for resolutions that are actually available
    def add_cam(self):
        dialog = customdialog.CamDialog(constants.STATE_DIALOG_ADD)
        if dialog.exec_():
            # Create a new Camera object
            new_cam = svdevices.Camera(
                dialog.leCamName.text(),
                dialog.cbCamLink.currentText(),
                dialog.cbCamRes.currentText(),
            )
            # Check that given data is valid
            if self._valid_add(new_cam):
                self.cams.append(new_cam)

            else:
                self.add_cam()

        self.refresh_gui()

    def edit_cam(self):
        dialog = customdialog.CamDialog(constants.STATE_DIALOG_EDIT)
        cam_pos = self.lwCam.currentRow()
        cam = self.cams[cam_pos]
        self.cams.pop(cam_pos)
        dialog.populate(cam)
        if dialog.exec_():
            new_cam = svdevices.Camera(
                dialog.leCamName.text(),
                dialog.cbCamLink.currentText(),
                dialog.cbCamRes.currentText()
            )

            if self._valid_add(new_cam):
                self.cams.insert(cam_pos, new_cam)

            else:
                self.cams.insert(cam_pos, cam)
                self.edit_cam()

        self.refresh_gui()

    def open_cam(self):
        # Initializes screen with selected cam object, opens thread when run
        cam = self.cams[self.lwCam.currentRow()]
        dialog = customdialog.ViewDialog(cam, self._del_view_dialog)
        dialog.add_label()
        self.view_dialogs[cam.name] = dialog
        dialog.show()
        self.refresh_tab_buts()

        # Start new thread
        if "FLIR" in cam.link:
            worker = Worker(self._handle_flir_cam, cam)

        else:
            worker = Worker(self._handle_cam, cam)

        worker.signals.obj_passback.connect(self._paint_cam_frame)
        self.threadpool.start(worker)

    def add_screen(self):
        dialog = customdialog.ScreenDialog(constants.STATE_DIALOG_ADD)
        if dialog.exec_():
            if dialog.rbScreenColor.isChecked():
                new_screen = svdevices.FlatScreen(
                    dialog.leScreenName.text(),
                    dialog.leScreenColor.text(),
                    monitor=dialog.cbMonNum.currentText()
                )

            elif dialog.rbScreenVideo.isChecked():
                new_screen = svdevices.Video(
                    dialog.leScreenName.text(),
                    dialog.leScreenVideo.text(),
                    monitor=dialog.cbMonNum.currentText()
                )

            if self._valid_add(new_screen):
                self.screens.append(new_screen)

            else:
                self.add_screen()

        self.refresh_gui()

    def edit_screen(self):
        dialog = customdialog.ScreenDialog(constants.STATE_DIALOG_EDIT)
        screen_pos = self.lwScreen.currentRow()
        screen = self.screens[screen_pos]
        self.screens.pop(screen_pos)
        dialog.populate(screen)
        if dialog.exec_():
            if dialog.rbScreenColor.isChecked():
                new_screen = \
                    svdevices.FlatScreen(
                        dialog.leScreenName.text(),
                        dialog.leScreenColor.text(),
                        monitor=dialog.cbMonNum.currentText()
                    )

            elif dialog.rbScreenVideo.isChecked():
                new_screen = svdevices.Video(
                        dialog.leScreenName.text(),
                        dialog.leScreenVideo.text(),
                    monitor=dialog.cbMonNum.currentText()
                    )

            if self._valid_add(new_screen):
                self.screens.insert(screen_pos, new_screen)

            else:
                self.screens.insert(screen_pos, screen)
                self.edit_screen()

        self.refresh_gui()

    # Add setting to maximize and assign to monitor
    def open_screen(self):
        # Initializes screen with selected screen object, opens thread
        # when run
        screen = self.screens[self.lwScreen.currentRow()]
        dialog = customdialog.ViewDialog(screen, self._del_view_dialog)
        self.view_dialogs[screen.name] = dialog
        dialog.show()
        self.refresh_tab_buts()

        # Create new thread if screen is a Video object
        if type(screen) is svdevices.Video:

            # Initialize Phonon multimedia objects
            media_src = Phonon.MediaSource(screen.link)
            media_obj = Phonon.MediaObject(dialog)
            media_obj.setCurrentSource(media_src)
            video_widget = Phonon.VideoWidget(dialog)
            video_widget.setMinimumSize(640, 480)
            dialog.vLayout.addWidget(video_widget)
            Phonon.createPath(media_obj, video_widget)
            video_widget.show()

            worker = Worker(self._handle_video, media_obj,
                            video_name=screen.name)
            self.threadpool.start(worker)

    def remove_gen_obj(self):
        # Removes cam, screen, or device that is selected
        if self.tabGroup.currentIndex() == constants.IDX_TAB_CAM:
            self.cams.pop(self.lwCam.currentRow())
            for item in self.lwCam.selectedItems():
                self.lwCam.setItemSelected(item, False)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_SCREEN:
            self.screens.pop(self.lwScreen.currentRow())
            for item in self.lwScreen.selectedItems():
                self.lwScreen.setItemSelected(item, False)

        elif self.tabGroup.currentIndex() == constants.IDX_TAB_DEVICES:
            self.devices.pop(self.lwDevices.currentRow())
            for item in self.lwDevices.selectedItems():
                self.lwDevices.setItemSelected(item, False)

        self.refresh_gui()
