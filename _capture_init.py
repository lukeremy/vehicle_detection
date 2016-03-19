import cv2
import numpy as np
import vehicle_tracking as proc
import time

from PyQt4 import QtGui, QtCore
from PyQt4 import uic

# Global variable
main_ui = uic.loadUiType("gtk/video_frame.ui")[0]

# init variable
start_time = None
width = 960     # pixel
height = 540    # pixel
alpha = 8       # second
mask_status = False
mask_frame = None
frame = 0

# background subtraction
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mog_bs = cv2.createBackgroundSubtractorMOG2()
knn_bs = cv2.createBackgroundSubtractorKNN()


class QtCapture(QtGui.QFrame, main_ui):
    def __init__(self, fps, filename):
        global avg
        super(QtGui.QFrame, self).__init__()

        self.fps = fps
        self.setupUi(self)

        # Start Capture Video
        self.cap = cv2.VideoCapture(filename)

        # Initiation to moving average
        _, frame = self.cap.read()
        frame = proc.convBGR2RGB(frame)
        frame = cv2.resize(frame, (width, height))
        avg = np.float32(frame)

    def setFPS(self, fps):
        self.fps = fps

    def start(self):
        global start_time
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.nextFrame)
        self.timer.start(1000. / self.fps)
        start_time = time.time()
        print format(start_time)
        return start_time

    def stop(self):
        self.timer.stop()

    def deleteLater(self):
        global frame
        frame = 0

        self.cap.release()
        super(QtGui.QFrame, self).deleteLater()

    def nextFrame(self):
        global mask_status, mask_frame, frame, mog_bs, kernel
        real_time = time.time()
        ret, frame_ori = self.cap.read()
        frame += 1

        # ---------- Do not disturb this source code ---------- #
        # Default color model is BGR format
        frame_resize = cv2.resize(frame_ori, (width, height))
        rgb_frame = proc.convBGR2RGB(frame_resize)                 # convert from BGR color model to RGB color model
        # ----------------------------------------------------- #

        # Initiation background subtraction
        # ------------------------------------------------------#

        # Moving Average subtraction
        acuWeight = cv2.accumulateWeighted(rgb_frame, avg, 0.01)
        initSubtrack = cv2.convertScaleAbs(acuWeight)               # return rgb color for background subtraction
        initBackground = proc.initBackgrounSubtraction(real_time, start_time, alpha)
        if not mask_status:
            if not initBackground:
                print "initiation background subtraction"
            else:
                print "mask found"
                mask_frame = initSubtrack
                mask_status = True
            subtract_frame = initSubtrack
        else:
            print "mask frame"
            subtract_frame = mask_frame

        # Mixture of Gaussian subtraction
        mog_frame = mog_bs.apply(frame_ori)

        # Kernel Nearest Neighbour subtraction
        kkn_frame = knn_bs.apply(frame_ori)

        # Mask
        bs_mask = cv2.morphologyEx(mog_frame, cv2.MORPH_OPEN, proc.kernel())

        # ------------------------------------------------------#

        # Image processing
        gray_frame = proc.convRGB2GRAY(initSubtrack)

        # Add frame rate text
        proc.addText(gray_frame, "frame: {0}".format(frame), 1, 850, 525)

        # Last variable to show must 'show_frame'
        show_frame = bs_mask

        # ---------- Do not disturb this source code ----------- #
        # Gray scale, binary image - Format_Indexed8
        # RGB image - Format_RGB888
        img = QtGui.QImage(show_frame, show_frame.shape[1], show_frame.shape[0], QtGui.QImage.Format_Indexed8)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        # ------------------------------------------------------ #
