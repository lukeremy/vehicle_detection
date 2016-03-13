import cv2


def resize(frame, width, height):
    frame = cv2.resize(frame, (width, height))
    return frame

def addText(frame, text, x, y):
    font = cv2.FONT_HERSHEY_PLAIN
    cv2.putText(frame, "{0}".format(text), (x, y), font, 0.9, (255, 255, 0), 1)

def convBGR2RGB(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

def convRGB2GRAY(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    return frame

def convRGB2HSV(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    return frame

def initBackgrounSubtraction(real_time, start_time, alpha):
    if real_time < start_time + alpha:
        print "initiation background subtraction"
        return False
    else:
        print "background subtraction found"
        return True
