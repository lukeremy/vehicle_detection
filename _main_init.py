import time
import sys
import _capture_init as cap_init
import _capture_alt_ as cap_alt

from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from _help_init import HelpInit

# Interface Load
main_ui = uic.loadUiType("gtk/main.ui")[0]
help_ui = uic.loadUiType("gtk/help.ui")[0]

# Variable
fileLoc = 0

class MainInit(QMainWindow, main_ui):
    def __init__(self, parent=None):
        # Initialization main interface from QT to Python
        QMainWindow.__init__(self, parent)

        # Variable
        self.setupUi(self)
        self.capture = None

        port_cam = ["0", "1", "2"]
        # Menu Bar
        # File
        self.actionExit.triggered.connect(self.file_exit)

        # 1.    Setting
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.setTabEnabled(1, False)
        self.tabWidget.setTabEnabled(2, False)

        # 1.1.  VideoInput
        self.radioButton_choseDevice.setChecked(True)
        self.radioButton_choseFile.setChecked(False)

        self.radioButton_choseFile.toggled.connect(self.radioChoseFile)
        self.radioButton_choseDevice.toggled.connect(self.radioChoseDevice)

        self.comboBox_choseDevice.setEnabled(True)
        self.comboBox_choseDevice.addItems(port_cam)
        self.comboBox_choseDevice.currentIndexChanged.connect(self.selectionDevice)

        self.label_selectFile.setText('')
        self.pushButton_selectFile.setEnabled(False)
        self.pushButton_selectFile.clicked.connect(self.selectFile)

        # 1.2.  VideoMode
        self.radioButton_rgbVM.setChecked(True)
        self.radioButton_binVM.setChecked(False)
        self.checkBox_showboundaryVM.setChecked(False)
        self.checkBox_showroiVM.setChecked(False)

        # 1.3 Background Subtraction
        self.radioButton_BsMA.setChecked(True)
        self.radioButton_BsMOG.setChecked(False)

        # 1.4   Data Input
        # 1.4.1 Camera
        self.setAlt(6)
        self.setElevated(20)
        self.setFps(30)
        self.setFocal(90)

        # 1.4.2 Vehicle Input
        # 1.4.2.1 Light Vehicle
        self.setLengthLV(6)
        self.setWidthLV(2.1)
        self.setHighLV(1.6)
        # 1.4.2.1 Heavy Vehicle
        self.setLengthHV(18)
        self.setWidthHV(2.5)
        self.setHighHV(4.2)

        # 1.4.3 Registration and Detection Line
        # 1.4.3.1 Detection Line
        self.setDetectionLine("500", "450", "840", "450")
        # 1.4.3.2 Registration Line
        self.setRegistrationLine("530", "200", "800", "200")
        # 1.5 Button Help and Set
        self.pushButton_helpSetting.clicked.connect(self.helpSetting)
        self.pushButton_setSetting.clicked.connect(self.setSetting)

        # 2.    Video
        # 2.1   Video Player
        self.pushButton_startVideo.clicked.connect(self.startVideo)
        self.pushButton_showLog.setVisible(False)
        self.pushButton_showLog.clicked.connect(self.showLog)

        # 2.2   Capture
        # self.tableView_Capture()
        self.setLabelLV("0")
        self.setLabelHV("0")
        self.setLabelFPS("0")

        # 3.    Log
        # 3.1   Search
        self.dateEdit_fromDate.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_fromDate.setCalendarPopup(True)

        self.dateEdit_untilDate.setDateTime(QDateTime.currentDateTime())
        self.dateEdit_untilDate.setCalendarPopup(True)

        self.pushButton_searchLog.clicked.connect(self.searchLog)
        self.pushButton_clearLog.clicked.connect(self.clearLog)

        # 3.2   View Log
        # self.tableView_searchLog()
        self.setLogCountLV("10")
        self.setLogCountHV("90")

    # Set Variable
    def setAlt(self, value):
        self.lineEdit_altitudeCam.setText(format(value))

    def getAlt(self):
        return self.lineEdit_altitudeCam.text()

    def setElevated(self, value):
        self.lineEdit_elevatedCam.setText(format(value))

    def getElevated(self):
        return self.lineEdit_elevatedCam.text()

    def setFps(self, value):
        self.lineEdit_fps.setText(format(value))

    def getFps(self):
        return self.lineEdit_fps.text()

    def setFocal(self, value):
        self.lineEdit_focal.setText(format(value))

    def getFocal(self):
        return self.lineEdit_focal.text()

    def setLengthLV(self, value):
        self.lineEdit_pLV.setText(format(value))

    def getLengthLV(self):
        return self.lineEdit_pLV.text()

    def setWidthLV(self, value):
        self.lineEdit_lLV.setText(format(value))

    def getWidthLV(self):
        return self.lineEdit_lLV.text()

    def setHighLV(self, value):
        self.lineEdit_tLV.setText(format(value))

    def getHighLV(self):
        return self.lineEdit_tLV.text()

    def setLengthHV(self, value):
        self.lineEdit_pHV.setText(format(value))

    def getLengthHV(self):
        return self.lineEdit_pHV.text()

    def setWidthHV(self, value):
        self.lineEdit_lHV.setText(format(value))

    def getWidthHV(self):
        return self.lineEdit_lHV.text()

    def setHighHV(self, value):
        self.lineEdit_tHV.setText(format(value))

    def getHighHV(self):
        return self.lineEdit_tHV.text()

    def setDetectionLine(self, x1, y1, x2, y2):
        self.lineEdit_detectX1.setText(format(x1))
        self.lineEdit_detectY1.setText(format(y1))
        self.lineEdit_detectX2.setText(format(x2))
        self.lineEdit_detectY2.setText(format(y2))

    def getDetectLine(self):
        detectX1 = self.lineEdit_detectX1.text()
        detectY1 = self.lineEdit_detectY1.text()
        detectX2 = self.lineEdit_detectX2.text()
        detectY2 = self.lineEdit_detectY2.text()
        return detectX1, detectY1, detectX2, detectY2

    def setRegistrationLine(self, x1, y1, x2, y2):
        self.lineEdit_registX1.setText(format(x1))
        self.lineEdit_registY1.setText(format(y1))
        self.lineEdit_registX2.setText(format(x2))
        self.lineEdit_registY2.setText(format(y2))

    def getRegistrationLine(self):
        registX1 = self.lineEdit_registX1.text()
        registY1 = self.lineEdit_registY1.text()
        registX2 = self.lineEdit_registX2.text()
        registY2 = self.lineEdit_registY2.text()
        return registX1, registY1, registX2, registY2

    def setLabelFPS(self, value):
        self.label_videoFps.setText("frame : {0}".format(value))

    def setLabelLV(self, value):
        self.label_countShortVehicle.setText(value)

    def setLabelHV(self, value):
        self.label_countLongVehicle.setText(value)

    def setLogCountLV(self, value):
        self.label_logcountShortVehicle.setText(value)

    def setLogCountHV(self, value):
        self.label_logcountLongVehicle.setText(value)

    # Get Variable
    def getVideoMode(self):
        if self.radioButton_rgbVM.isChecked():
            video_mode = "RGB"
        elif self.radioButton_binVM.isChecked():
            video_mode = "BIN"
        return video_mode

    def getBoundary(self):
        return self.checkBox_showboundaryVM.isChecked()

    def getRoi(self):
        return self.checkBox_showroiVM.isChecked()

    def getBackgroundSubtraction(self):
        if self.radioButton_BsMOG.isChecked():
            background_subtraction = "MOG"
        elif self.radioButton_BsMA.isChecked():
            background_subtraction = "MA"
        return background_subtraction

    # Function Menu Bar
    # Menu File
    def file_exit(self):
        print "good bye bro.."
        sys.exit()

    # Function Tab 1. Setting
    def cekVideoInput(self):
        if self.radioButton_choseFile.setChecked(True):
            print "Chose file"
        elif self.radioButton_choseDevice.setChecked(True):
            print "Device"

    def selectFile(self):
        global fileLoc

        file_filter = "Movie (*.mp4 *.avi *.mkv)"
        filename = QFileDialog.getOpenFileName(self, "Open File", '', file_filter, None,
                                               QFileDialog.DontUseNativeDialog)

        print "file yg di select {0}".format(filename)
        self.label_selectFile.setText(format(filename))

        fileLoc = format(filename)
        return fileLoc

    def selectionDevice(self):
        global fileLoc

        select = self.comboBox_choseDevice.currentText()
        print "Current index selection ", select

        fileLoc = int(select)
        return fileLoc

    def radioChoseFile(self, enabled):
        if enabled:
            self.pushButton_selectFile.setEnabled(True)
        else:
            self.pushButton_selectFile.setEnabled(False)

    def radioChoseDevice(self, enabled):
        global fileLoc
        if enabled:
            self.comboBox_choseDevice.setEnabled(True)
            fileLoc = 0
        else:
            self.comboBox_choseDevice.setEnabled(False)

    def radioMBO(self, enabled):
        if enabled:
            self.label_initBackground.setEnabled(True)
            self.lineEdit_initBackground.setEnabled(True)
            self.label_initBackgroundSecond.setEnabled(True)
        else:
            self.label_initBackground.setEnabled(False)
            self.lineEdit_initBackground.setEnabled(False)
            self.label_initBackgroundSecond.setEnabled(False)

    def setSetting(self):
        # Get video mode
        video_mode = self.getVideoMode()
        boundary = self.getBoundary()
        roi = self.getRoi()

        # Get background subtraction
        background_subtraction = self.getBackgroundSubtraction()

        # Camera
        alt = float(self.getAlt())
        elevated = float(self.getElevated())
        fps = float(self.getFps())
        focal = float(self.getFocal())

        # Light vehicle dimension
        length_LV = float(self.getLengthLV())
        width_LV = float(self.getWidthLV())
        high_LV = float(self.getHighLV())

        # Heavy vehicle dimension
        length_HV = float(self.getLengthHV())
        width_HV = float(self.getWidthHV())
        high_HV = float(self.getHighHV())

        # Registration and detection line
        detectX1, detectY1, detectX2, detectY2 = self.getDetectLine()
        registX1, registY1, registX2, registY2 = self.getRegistrationLine()

        print "Camera Input"
        print "video input: {0}".format(fileLoc)
        print "video mode: {0}".format(video_mode)
        print "background subtraction: {0}".format(background_subtraction)
        # print "init time bsMBO: {0}".format(initMBO)
        print "boundary: {0}".format(boundary)
        print "roi: {0}".format(roi)
        print "alt: {0} | elevated: {1} | fps: {2} | focal:{3}".format(alt, elevated, fps, focal)
        print "Vehicle Input"
        print "LV >> length: {0} | width: {1} | high: {2}".format(length_LV, width_LV, high_LV)
        print "HV >> length: {0} | width: {1} | high: {2}".format(length_HV, width_HV, high_HV)
        print "Registration and Detection Line"
        print "Detection Line >> ({0},{1}) | ({2},{3})".format(detectX1, detectY1, detectX2, detectY2)
        print "Registration Line >> ({0},{1}) | ({2},{3})".format(registX1, registY1, registX2, registY2)
        time.sleep(1)

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentIndex(1)

    def helpSetting(self):
        title = "Panduan Singkat"
        filename = "conf/help.txt"

        print "Open new popup help"
        self.help_win = HelpInit(title, filename, None)
        self.help_win.show()

    # Function Tab 2. Video
    def startVideo(self):

        # Get video mode
        video_mode = self.getVideoMode()
        boundary = self.getBoundary()
        roi = self.getRoi()

        # Get background subtraction
        background_subtraction = self.getBackgroundSubtraction()

        # Camera
        alt = float(self.getAlt())
        elevated = int(self.getElevated())
        fps = float(self.getFps())
        focal = float(self.getFocal())

        # Light vehicle dimension
        length_LV = float(self.getLengthLV())
        width_LV = float(self.getWidthLV())
        high_LV = float(self.getHighLV())

        # Heavy vehicle dimension
        length_HV = float(self.getLengthHV())
        width_HV = float(self.getWidthHV())
        high_HV = float(self.getHighHV())

        # Registration and detection line
        detectX1, detectY1, detectX2, detectY2 = self.getDetectLine()
        registX1, registY1, registX2, registY2 = self.getRegistrationLine()

        self.tabWidget.setTabEnabled(0, False)

        time.sleep(1)

        self.tabWidget.setTabEnabled(1, True)
        self.tabWidget.setCurrentIndex(1)

        if not self.capture:
            self.capture = cap_init.QtCapture(fileLoc)

            self.pushButton_pauseVideo.clicked.connect(self.capture.stop)
            self.pushButton_stopVideo.clicked.connect(self.stopVideo)

            self.capture.setVideoMode(video_mode)
            self.capture.setBackgroundSubtraction(background_subtraction)
            self.capture.setROI(roi)
            self.capture.setBoundary(boundary)

            self.capture.setFPS(fps)
            self.capture.setAlt(alt)
            self.capture.setElevated(elevated)
            self.capture.setFocal(focal)

            self.capture.setLengthLV(length_LV)
            self.capture.setWidthLV(width_LV)
            self.capture.setHighLV(high_LV)

            self.capture.setLengthHV(length_HV)
            self.capture.setWidthHV(width_HV)
            self.capture.setHighHV(high_HV)

            self.capture.setDetectionLine(detectX1, detectY1, detectX2, detectY2)
            self.capture.setRegistrationLine(registX1, registY1, registX2, registY2)
            self.capture.setParent(self.video_frame)

            # Get Variable
            #fps = self.capture.getLabelFPS()
            self.setLabelFPS(90)

            #labelLV = str(self.getLabel())
            self.setLabelLV("10")

            #labelHV = str(self.capture.getLabelHV())
            self.setLabelHV("90")

        self.capture.start()
        self.capture.show()

    def pauseVideo(self):
        self.videoPlayer.pause()

    def stopVideo(self):
        self.capture.deleteLater()
        self.capture = None

        self.tabWidget.setTabEnabled(0, True)
        self.pushButton_showLog.setVisible(True)

    def showLog(self):

        time.sleep(1)

        self.tabWidget.setTabEnabled(2, True)
        self.tabWidget.setCurrentIndex(2)

    # Function Tab 3. Log
    def searchLog(self):
        hLabel = ["No", "Date", "Time", "Type", "Speed", "Picture"]
        row = 4
        column = 6

        fromDate = self.dateEdit_untilDate.date().toPyDate()
        untilDate = self.dateEdit_untilDate.date().toPyDate()

        self.tableWidget_searchLog.setRowCount(row)
        self.tableWidget_searchLog.setColumnCount(column)
        self.tableWidget_searchLog.setHorizontalHeaderLabels(hLabel)

        self.tableWidget_searchLog.setItem(0, 0, QTableWidgetItem("Item (0,0)"))
        self.tableWidget_searchLog.setItem(0, 1, QTableWidgetItem("Item (3,0)"))
        self.tableWidget_searchLog.setItem(2, 3, QTableWidgetItem("Item (1,0)"))

        print "mulai dari tanggal {0}".format(fromDate)
        print "hingga tanggal {0}".format(untilDate)

        self.label_logcountShortVehicle.setText("20")
        self.label_logcountLongVehicle.setText("100")

    def clearLog(self):
        self.tableWidget_searchLog.clear()
