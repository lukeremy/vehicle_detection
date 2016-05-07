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
        filename = None
        video_mode = None
        boundary = None
        roi = None
        alt = None
        elevated = None
        fps = None

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
        self.radioButton_BsMOG.setChecked(True)
        self.radioButton_BsMA.setChecked(False)

        # 1.4   Data Input
        # 1.4.1 Camera
        self.lineEdit_altitudeCam.setText(format("100"))
        self.lineEdit_elevatedCam.setText(format("20"))
        self.lineEdit_fps.setText(format("10"))
        self.lineEdit_focal.setText(format("5"))

        # 1.4.2 Vehicle Input
        # 1.4.2.1 Light Vehicle
        self.lineEdit_pLV.setText(format("6"))
        self.lineEdit_lLV.setText(format("2.1"))
        self.lineEdit_tLV.setText(format("1.6"))

        # 1.4.2.1 Heavy Vehicle
        self.lineEdit_pHV.setText(format("18"))
        self.lineEdit_lHV.setText(format("2.5"))
        self.lineEdit_tHV.setText(format("4.2"))

        # 1.4.3 Registration and Detection Line
        # 1.4.3.1 Registration Line
        self.lineEdit_detectX1.setText(format("10"))
        self.lineEdit_detectY1.setText(format("20"))
        self.lineEdit_detectX2.setText(format("30"))
        self.lineEdit_detectY2.setText(format("40"))
        # 1.4.3.2 Detection Line
        self.lineEdit_registX1.setText(format("50"))
        self.lineEdit_registY1.setText(format("60"))
        self.lineEdit_registX2.setText(format("70"))
        self.lineEdit_registY2.setText(format("80"))

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
        self.label_countShortVehicle.setText("140")
        self.label_countLongVehicle.setText("130")
        self.label_videoFps.setText("frame : {0}".format("0"))

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
        self.label_logcountShortVehicle.setText("20")
        self.label_logcountLongVehicle.setText("100")

    # Get variabel
    def getAlt(self):
        return self.lineEdit_altitudeCam.text()

    def getElevated(self):
        return self.lineEdit_elevatedCam.text()

    def getFps(self):
        return self.lineEdit_fps.text()

    def getFocal(self):
        return self.lineEdit_focal.text()

    def getLengthLV(self):
        return self.lineEdit_pLV.text()

    def getWidthLV(self):
        return self.lineEdit_lLV.text()

    def getHighLV(self):
        return self.lineEdit_tLV.text()

    def getLengthHV(self):
        return self.lineEdit_pHV.text()

    def getWidthHV(self):
        return self.lineEdit_lHV.text()

    def getHighHV(self):
        return self.lineEdit_tHV.text()

    def getVideoMode(self):
        if self.radioButton_rgbVM.isChecked():
            video_mode = "rgb"
        elif self.radioButton_binVM.isChecked():
            video_mode = "binary"
        return video_mode

    def getBoundary(self):
        return self.checkBox_showboundaryVM.isChecked()

    def getRoi(self):
        return self.checkBox_showroiVM.isChecked()

    def getBackgroundSubtraction(self):
        if self.radioButton_BsMOG.isChecked():
            background_subtraction = "mog"
        elif self.radioButton_BsMA.isChecked():
            background_subtraction = "ma"
        return background_subtraction

    def getDetectLine(self):
        detectX1 = self.lineEdit_detectX1.text()
        detectY1 = self.lineEdit_detectY1.text()
        detectX2 = self.lineEdit_detectX2.text()
        detectY2 = self.lineEdit_detectY2.text()
        return detectX1, detectY1, detectX2, detectY2

    def getRegistrationLine(self):
        registX1 = self.lineEdit_registX1.text()
        registY1 = self.lineEdit_registY1.text()
        registX2 = self.lineEdit_registX2.text()
        registY2 = self.lineEdit_registY2.text()
        return registX1, registY1, registX2, registY2

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
        # Variable
        initMBO = None

        # Get video mode
        video_mode = self.getVideoMode()

        # Get video mode
        boundary = self.getBoundary()
        roi = self.getRoi()

        # Get background subtraction
        background_subtraction = self.getBackgroundSubtraction()

        # Get camera setting
        alt = self.getAlt()
        elevated = self.getElevated()
        fps = self.getFps()
        focal = self.getFocal()

        # Get vehicle dimension
        # Light vehicle dimension
        length_LV = self.getLengthLV()
        width_LV = self.getWidthLV()
        high_LV = self.getHighLV()

        # Heavy vehicle dimension
        length_HV = self.getLengthHV()
        width_HV = self.getWidthHV()
        high_HV = self.getHighHV()

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
        fps = 30

        self.tabWidget.setTabEnabled(0, False)

        if not self.capture:
            self.capture = cap_init.QtCapture(fps, fileLoc)
            self.pushButton_pauseVideo.clicked.connect(self.capture.stop)
            self.pushButton_stopVideo.clicked.connect(self.stopVideo)
            # self.capture.setFPS(1)
            self.capture.setParent(self.video_frame)

        self.capture.start()
        self.capture.show()

    def startVideoAlt(self):
        if not self.capture:
            self.capture = cap_alt.QtCaptureAlt(fileLoc)
        self.capture.startCapture()
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

        self.lcdNumber_logShortVehicle.display("50")
        self.lcdNumber_logLongVehicle.display("10")

    def clearLog(self):
        self.tableWidget_searchLog.clear()

    def ujicoba(self):
        print "Open new popup"