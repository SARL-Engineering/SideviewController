import constants
import svdevices
from threadworker import Worker
from ui import camdialog_ui, screendialog_ui, viewdialog_ui
from ui import comdialog_ui, rulesdialog_ui
import cv2
import PySpin
from PyQt4 import QtGui, QtCore
import time


class CamDialog(QtGui.QDialog, camdialog_ui.Ui_CamDialog):

    def __init__(self, context, parent=None):
        super(CamDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.context = context

        self._set_labels()
        self._set_default_gui_state()
        self._connect_signals()

        self.refresh_gui()

    def _set_labels(self):
        # Sets text for all labels, buttons, etc.
        self.labelCamName.setText(constants.LABEL_LABEL_CAM_NAME)
        self.labelCamLink.setText(constants.LABEL_LABEL_CAM_LINK)
        self.labelCamRes.setText(constants.LABEL_LABEL_CAM_RES)

    def _set_default_gui_state(self):
        # Sets gui elements based on context (Add or Edit)
        if self.context == constants.STATE_DIALOG_ADD:
            self.setWindowTitle(constants.LABEL_CAM_DIALOG_TITLE_ADD)

        elif self.context == constants.STATE_DIALOG_EDIT:
            self.setWindowTitle(constants.LABEL_CAM_DIALOG_TITLE_EDIT)

        available_cams = self._get_available_cams()
        for cam in available_cams:
            self.cbCamLink.addItem(cam)

        self.cbCamRes.addItem(constants.RES_HIGH_HD)
        self.cbCamRes.addItem(constants.RES_LOW_HD)
        self.cbCamRes.addItem(constants.RES_HQ)

    def _connect_signals(self):
        pass

    def _get_available_cams(self, cam_range=constants.CAM_IDX_RANGE):
        # Queries camera indices in given range, there's apparently
        # no better way to get a list of cameras...
        cam_list = []
        for x in range(cam_range):
            cap = cv2.VideoCapture(x)
            if cap is None or not cap.isOpened():
                continue
            cam_list.append("cam{}".format(x))

        # Add FLIR cams
        system = PySpin.System.GetInstance()
        flir_cam_list = system.GetCameras()

        for cam in flir_cam_list:

            # Retrieve device ID
            nodemap_tldevice = cam.GetTLDeviceNodeMap()
            node_dev_info = PySpin.CCategoryPtr(nodemap_tldevice.GetNode(
                "DeviceInformation"
            ))
            features = node_dev_info.GetFeatures()
            for feature in features:
                node_feature = PySpin.CValuePtr(feature)
                if node_feature.GetName() == "DeviceID":
                    cam_list.append(
                        "FLIR cam {}".format(node_feature.ToString()))

            del cam

        flir_cam_list.Clear()
        system.ReleaseInstance()
        return cam_list

    def refresh_gui(self):
        pass

    def populate(self, cam):
        # Fill gui elements with data from Camera object
        self.leCamName.setText(cam.name)
        self.cbCamLink.setCurrentIndex(self.cbCamLink.findText(cam.link))
        self.cbCamRes.setCurrentIndex(self.cbCamRes.findText(cam.resolution))


class ScreenDialog(QtGui.QDialog, screendialog_ui.Ui_screenDialog):

    def __init__(self, context, parent=None):
        super(ScreenDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.context = context

        self._set_labels()
        self._set_default_gui_state()
        self._connect_signals()

        self.refresh_gui()

    def _set_labels(self):
        # Sets text for all labels, buttons, etc.
        self.labelScreenName.setText(constants.LABEL_LABEL_SCREEN_NAME)
        self.labelMonNum.setText(constants.LABEL_LABEL_MONITOR_NUM)
        self.rbScreenVideo.setText(constants.LABEL_RB_SCREEN_VIDEO)
        self.rbScreenColor.setText(constants.LABEL_RB_SCREEN_COLOR)
        self.pbScreenVideo.setText(constants.LABEL_PB_SCREEN_VIDEO)
        self.pbScreenColor.setText(constants.LABEL_PB_SCREEN_COLOR)

    def _set_default_gui_state(self):
        # Sets gui elements based on context (Add or Edit)
        if self.context == constants.STATE_DIALOG_ADD:
            self.setWindowTitle(constants.LABEL_SCREEN_DIALOG_TITLE_ADD)

        elif self.context == constants.STATE_DIALOG_EDIT:
            self.setWindowTitle(constants.LABEL_SCREEN_DIALOG_TITLE_EDIT)

        # Populate monitor listing
        self.desktop = QtGui.QDesktopWidget()
        self.cbMonNum.addItem(constants.LABEL_CB_MON_NUM_NA)
        for mon_num in range(self.desktop.numScreens()):
            self.cbMonNum.addItem("Monitor {}".format(mon_num))

    def _connect_signals(self):
        # Connects signals to all appropriate gui elements
        self.pbScreenVideo.clicked.connect(self.select_output_folder)
        self.pbScreenColor.clicked.connect(self.select_color)
        self.rbScreenVideo.clicked.connect(self.refresh_gui)
        self.rbScreenColor.clicked.connect(self.refresh_gui)

    def select_output_folder(self):
        # Populate output box with a directory
        directory = QtGui.QFileDialog.getOpenFileName(
            None,
            constants.DIALOG_OPEN_VIDEO_TITLE,
            "",
            constants.FILTER_VIDEO
        )
        self.leScreenVideo.setText(directory)

    def select_color(self):
        # Populate output box with a hex color code
        color = QtGui.QColorDialog.getColor()
        if color.isValid():
            self.leScreenColor.setText(color.name())
            self.leScreenColor.setStyleSheet(
                "QLineEdit { background-color: %s }" % color.name()
            )

    def refresh_gui(self):
        # Update elements to correct values and ability/disability
        #  Update radio buttons
        if self.rbScreenColor.isChecked():
            self.pbScreenVideo.setEnabled(False)
            self.leScreenVideo.setEnabled(False)
            self.pbScreenColor.setEnabled(True)
            self.leScreenColor.setEnabled(True)

        elif self.rbScreenVideo.isChecked():
            self.pbScreenVideo.setEnabled(True)
            self.leScreenVideo.setEnabled(True)
            self.pbScreenColor.setEnabled(False)
            self.leScreenColor.setEnabled(False)

        else:
            self.rbScreenVideo.click()

    def populate(self, screen):
        # Fill gui elements with data from Screen object
        self.leScreenName.setText(screen.name)
        self.cbMonNum.setCurrentIndex(self.cbMonNum.findText(screen.monitor))
        if type(screen) is svdevices.FlatScreen:
            self.rbScreenColor.click()
            self.leScreenColor.setText(screen.color)
            self.leScreenColor.setStyleSheet(
                "QLineEdit { background-color: %s }" % screen.color
            )

        elif type(screen) is svdevices.Video:
            self.rbScreenVideo.click()
            self.leScreenVideo.setText(screen.link)


class COMDialog(QtGui.QDialog, comdialog_ui.Ui_COMDialog):

    def __init__(self, context, parent=None):
        super(COMDialog, self).__init__(parent)
        self.setupUi(self)
        self.context = context
        self.setModal(True)

        self._set_labels()
        self._set_default_gui_state()
        self._connect_signals()

        self.refresh_gui()

    def _set_labels(self):
        self.labelCOMName.setText(constants.LABEL_LABEL_COM_NAME)
        self.labelCOMLink.setText(constants.LABEL_LABEL_COM_LINK)
        self.labelCOMSignal.setText(constants.LABEL_LABEL_COM_SIGNAL)
        self.labelCOMBaudRate.setText(constants.LABEL_LABEL_COM_BAUD_RATE)
        self.labelCOMRules.setText(constants.LABEL_LABEL_COM_RULES)

    def _set_default_gui_state(self):
        if self.context == constants.STATE_DIALOG_ADD:
            self.setWindowTitle(constants.LABEL_COM_DIALOG_TITLE_ADD)

        elif self.context == constants.STATE_DIALOG_EDIT:
            self.setWindowTitle(constants.LABEL_COM_DIALOG_TITLE_EDIT)

    def _connect_signals(self):
        pass

    def refresh_gui(self):
        pass

    def add_rule(self):
        pass

    def edit_rule(self):
        pass

    def remove_rule(self):
        pass

class RulesDialog(QtGui.QDialog, rulesdialog_ui.Ui_rulesDialog):

    def __init__(self, context, parent=None):
        super(RulesDialog, self).__init__(parent)
        self.setupUi(self)
        self.context = context
        self.setModal(True)

        self._set_labels()
        self._set_default_gui_state()
        self._connect_signals()

        self.refresh_gui()

    def _set_labels(self):
        self.labelRuleNum.setText(constants.LABEL_LABEL_RULE_NUM)
        self.rbRuleAt.setText(constants.LABEL_RB_RULE_AT)
        self.rbRuleEvery.setText(constants.LABEL_RB_RULE_EVERY)

    def _set_default_gui_state(self):
        if self.context == constants.STATE_DIALOG_ADD:
            self.setWindowTitle(constants.LABEL_RULE_DIALOG_TITLE_ADD)

        elif self.context == constants.STATE_DIALOG_EDIT:
            self.setWindowTitle(constants.LABEL_RULE_DIALOG_TITLE_EDIT)

    def _connect_signals(self):
        self.rbRuleAt.clicked.connect(self.refresh_gui)
        self.rbRuleEvery.clicked.connect(self.refresh_gui)

    def refresh_gui(self):
        if self.rbRuleAt.isChecked():
            self.teRuleAt.setEnabled(True)
            self.teRuleEvery.setEnabled(False)

        elif self.rbRuleEvery.isChecked():
            self.teRuleAt.setEnabled(False)
            self.teRuleEvery.setEnabled(True)

        else:
            self.rbRuleAt.click()


class ViewDialog(QtGui.QDialog, viewdialog_ui.Ui_Dialog):

    def __init__(self, obj, vd_dict_func, parent=None):
        super(ViewDialog, self).__init__(parent)
        self.setupUi(self)
        self.obj = obj

        # This is a function from MainWindow that updates the dictionary
        # of active ViewDialogs.  closeEvent() is overriden to update the
        # dictionary before actually destroying itself so that the
        # corresponding thread will exit without error.  Sorry for the shit
        # code.
        self.update_vd_dict = vd_dict_func

        self._set_labels()
        self._set_default_gui_state()
        self._connect_signals()

        self.refresh_gui()

    def _set_labels(self):
        # Sets placeholder text
        self.setWindowTitle(self.obj.name)

    def _set_default_gui_state(self):
        # Sets state for screen

        # Ensure window can be maximized
        self.setWindowFlags(
            self.windowFlags() |
            QtCore.Qt.WindowMinMaxButtonsHint
        )

        # Maximize in monitor, if indicated
        if (type(self.obj) is svdevices.FlatScreen or
            type(self.obj) is svdevices.Video):

            if self.obj.monitor != constants.LABEL_CB_MON_NUM_NA:

                mon_num = int(self.obj.monitor[8:])
                desktop = QtGui.QDesktopWidget()
                monitor = desktop.screenGeometry(mon_num)
                self.move(monitor.left(), monitor.height())
                self.setWindowState(QtCore.Qt.WindowFullScreen)

        # Color the window if it's a flat color screen
        if type(self.obj) is svdevices.FlatScreen:
            self.setStyleSheet(
                "QWidget { background-color: %s }" % self.obj.color
            )

    def _connect_signals(self):
        pass

    def keyPressEvent(self, event):
        # Handles fullscreen functionality
        if (event.key() == QtCore.Qt.Key_Escape or
                event.key() == QtCore.Qt.Key_Return or
                event.key() == QtCore.Qt.Key_Enter or
                event.key() == QtCore.Qt.Key_Space):

            if self.isFullScreen():
                self.setWindowState(QtCore.Qt.WindowMaximized)

            else:
                self.setWindowState(QtCore.Qt.WindowFullScreen)

            event.accept()

    def closeEvent(self, event):
        # Update MainWindow dict before closing
        self.update_vd_dict(self.obj.name)
        event.accept()

    def add_label(self):
        self.camFrame = QtGui.QLabel("")
        self.vLayout.addWidget(self.camFrame)

    def refresh_gui(self):
        pass
