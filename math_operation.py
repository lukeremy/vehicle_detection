import math

def centeroidPinHoleMode(height, focal, altitude, theta, yCoordinate):
    # height : jumlah baris (piksel)
    # focal -> |A'O| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # yCoordinate : indeks piksel Y object

    delta = math.degrees(math.atan(math.fabs(yCoordinate - (height / 2)) / focal))

    if yCoordinate > height / 2:
        Lcenteroid = altitude * math.tan(math.radians(theta + delta))
    else:
        Lcenteroid = altitude * math.tan(math.radians(theta - delta))

    Lcenteroid = round(Lcenteroid, 2)
    return Lcenteroid

def vertikalPinHoleModel(height, focal, altitude, theta, x1, x2, maxHighLV, maxHighHV, maxLengthLV):
    # height : jumlah baris (piksel)
    # focal -> |A'O| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # x1' : indeks piksel terdepan kendaraan (kordinat y)
    # x2' : indeks piksel terbelakang kendaraan (kordinat y)
    # Lx1 -> |O'X1| : jarak titik terdepan kendaraan dengan kamera (m)
    # Lx2 -> |O'X2| : jarak titik blindspot belakang kendaraan (m)
    # X2G -> |X2G| : jarak belakang kendaraan dengan titik blindspot belakang kendaraan (m)

    delta1 = math.degrees(math.atan(math.fabs(x1 - (height / 2)) / focal))
    delta2 = math.degrees(math.atan(math.fabs(x2 - (height / 2)) / focal))

    if x1 >= height / 2:
        Lx1 = altitude * math.tan(math.radians(theta + delta1))
    else:
        Lx1 = altitude * math.tan(math.radians(theta - delta1))

    if x2 >= height / 2:
        Lx2 = altitude * math.tan(math.radians(theta + delta2))
    else:
        Lx2 = altitude * math.tan(math.radians(theta - delta2))

    Lv = Lx1 - Lx2

    if Lv <= maxLengthLV:
        estimationVehicleHigh = maxHighLV
    else:
        estimationVehicleHigh = maxHighHV

    if x2 >= height / 2:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta + delta2))
    else:
        X2G = estimationVehicleHigh * math.tan(math.radians(theta - delta2))

    Lv = Lx1 - (Lx2 + X2G)

    delta1 = round(delta1, 3)
    delta2 = round(delta2, 3)
    Lx1 = round(Lx1, 4)
    Lx2 = round(Lx2, 4)
    X2G = round(X2G, 4)
    Lv = round(Lv, 2)

    #print "delta1: {0} | delta2: {1} | Lx1: {2} | Lx2: {3} | X2G: {4} | Lv: {5}".format(delta1, delta2, Lx1, Lx2, X2G, Lv)
    return Lv

def horizontalPinHoleModel(width, height, focal, altitude, theta, x1, x2, yCoordinate):

    widthY = math.fabs(x1 - x2)
    delta1 = math.degrees(math.atan(math.fabs(x1 - (width / 2)) / focal))
    delta2 = math.degrees(math.atan(math.fabs(x2 - (width / 2)) / focal))

    lengthObject = centeroidPinHoleMode(height, focal, altitude, theta, yCoordinate)
    OX = math.sqrt(math.exp(lengthObject) + math.exp(altitude))
    widthObject = (widthY * OX) / focal
    widthObject = round(widthObject, 2)
    print widthObject

def funcY_line(x1, y1, x2, y2, X):
    # m : gradien garis
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
    # m : gradien garis
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
