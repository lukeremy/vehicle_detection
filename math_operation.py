import math

def centeroidPinHoleMode(height, focal, altitude, theta, yCoordinate):
    # height : jumlah baris (piksel)
    # focal -> |A'O| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # yCoordinate : indeks piksel Y object
    height = float(height)
    focal = float(focal)
    theta = float(theta)
    yCoordinate = float(yCoordinate)

    delta = math.degrees(math.atan(math.fabs(yCoordinate - (height / 2)) / focal))

    if yCoordinate <= height / 2:
        lCentroid = altitude * math.tan(math.radians(theta + delta))
    else:
        lCentroid = altitude * math.tan(math.radians(theta - delta))

    lCentroid = round(lCentroid, 4)
    delta = round(delta, 4)

    if (theta + delta) > 90.0:
        Lcenteroid = "unknown length"

    # print "delta: {0} | lCentroid: {1}".format(delta, lCentroid)
    return lCentroid

def vertikalPinHoleModel(height, focal, altitude, theta, y1, y2, maxHighLV, maxHighHV, maxLengthLV):
    # height : jumlah baris (piksel)
    # focal -> |A'O| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # y1' : indeks piksel terdepan kendaraan (kordinat y)
    # y2' : indeks piksel terbelakang kendaraan (kordinat y)
    # Lx1 -> |O'X1| : jarak titik terdepan kendaraan dengan kamera (m)
    # Lx2 -> |O'X2| : jarak titik blindspot belakang kendaraan (m)
    # X2G -> |X2G| : jarak belakang kendaraan dengan titik blindspot belakang kendaraan (m)

    delta1 = math.degrees(math.atan(math.fabs(y1 - (height / 2)) / focal))
    delta2 = math.degrees(math.atan(math.fabs(y2 - (height / 2)) / focal))

    if y1 <= height / 2:
        Lx1 = altitude * math.tan(math.radians(theta + delta1))
    else:
        Lx1 = altitude * math.tan(math.radians(theta - delta1))

    if y2 <= height / 2:
        Lx2 = altitude * math.tan(math.radians(theta + delta2))
    else:
        Lx2 = altitude * math.tan(math.radians(theta - delta2))

    Lv = math.fabs(Lx1 - Lx2)

    if Lv <= maxLengthLV:
        estimationVehicleHigh = maxHighLV
    else:
        estimationVehicleHigh = maxHighHV

    if y2 >= height / 2:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta + delta2))
    else:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta - delta2))

    Lv = math.fabs(Lx1 - (Lx2 + X2G))

    delta1 = round(delta1, 3)
    delta2 = round(delta2, 3)
    Lx1 = round(Lx1, 4)
    Lx2 = round(Lx2, 4)
    X2G = round(X2G, 4)
    Lv = round(Lv, 3)

    # print "delta1: {0} | delta2: {1} | Lx1: {2} | Lx2: {3} | X2G: {4} | Lv: {5}".format(delta1, delta2, Lx1, Lx2, X2G, Lv)
    return Lv

def horizontalPinHoleModel(width, focal, altitude, x1, x2, lengthObject):
    # width : jumlah kolom (piksel)
    # focal -> |A'O| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # lengthObject : jarak objek dengan kamera (m)
    # x1' : indeks piksel kanan kendaraan (kordinat x)
    # x2' : indeks piksel kiri kendaraan (kordinat x)
    # Lw1 -> |O'X1| : jarak titik kanan kendaraan dengan titik tengah kamera (m)
    # Lw2 -> |O'X2| : jarak titik kiri kendaraan dengan titik tengah kamera (m)
    # X2G -> |X2G| : jarak belakang kendaraan dengan titik blindspot belakang kendaraan (m)

    delta1 = math.degrees(math.atan(math.fabs(x1 - (width / 2)) / focal))
    delta2 = math.degrees(math.atan(math.fabs(x2 - (width / 2)) / focal))

    OX = math.sqrt(math.pow(lengthObject, 2) + math.pow(altitude, 2))

    Lw1 = math.tan(math.radians(delta1)) * OX
    Lw2 = math.tan(math.radians(delta2)) * OX

    if (x1 <= width / 2) and (x2 >= width / 2):
        widthObject = round((Lw2 + Lw1), 3)
    else:
        widthObject = round(math.fabs(Lw2 - Lw1), 3)

    delta1 = round(delta1, 3)
    delta2 = round(delta2, 3)
    lengthObject = round(lengthObject, 2)
    OX = round(OX, 4)
    Lw1 = round(Lw1, 4)
    Lw2 = round(Lw2, 4)

    # print "delta1: {0} | delta2: {1} | Length: {2} | OX: {3} | Lw1: {4} | Lw2: {5} | widthObject: {6}".format(delta1, delta2, lengthObject, OX, Lw1, Lw2, widthObject)
    return widthObject

def funcY_line(x1, y1, x2, y2, X):
    # m : line gradient
    # y - y1 = m (x -x1)
    # y = m (x - x1) + y

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    X = float(X)

    m = (y1 - y2) / (x1 - x2)
    Y = ((m * X) - (m * x1)) + y1
    Y = int(round(Y))
    return Y

def funcX_line(x1, y1, x2, y2, Y):
    # m : line gradient
    # y - y1 = m (x -x1)
    # x = ((y - y1) + (m * x1)) /m

    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    Y = float(Y)

    m = (y1 - y2) / (x1 - x2)
    X = ((Y - y1) + (m * x1)) / m
    X = int(round(X))
    return X

def getFocalfromFOV(width, fov):
    focal = (width / 2) / math.tan(math.radians(fov / 2))
    return focal

def transformDiagonalFOV(fov):
    if fov == 90.0:
        horizontalFOV = 78.4
        verticalFOV = 44.1
    elif fov == 127.0:
        horizontalFOV = 113.3
        verticalFOV = 63.7
    elif fov == 160.0:
        horizontalFOV = 139.5
        verticalFOV = 78.4
    else:
        horizontalFOV, verticalFOV = fov

    return horizontalFOV, verticalFOV

def distancetwoPoint(x1, y1, x2, y2):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)

    distance = math.sqrt((math.pow(math.fabs(x1 - x2), 2) + (math.pow(math.fabs(y1 - y2), 2))))
    distance = int(distance)

    return distance

