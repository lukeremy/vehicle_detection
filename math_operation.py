import math

def pinholeModel(height, focal, altitude, theta, x1, x2, maxHighLV, maxHighHV, maxLengthLV):
    # W : jumlah baris (piksel)
    # focal -> |A'B| : focal length (piksel)
    # altitude -> |O'O| : tinggi kamera (m)
    # theta : sudut kemiringan kamera (derajat)
    # x1' : indeks piksel terdepan kendaraan
    # x2' : indeks piksel terbelakang kendaraan
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

def funcY_line(x1, y1, x2, y2, centeroidX):
    # m : gradien garis
    m = (y1 -y2) / (x1 - x2)
    y = ((m * centeroidX) - (m * x1)) + y1
    y = round(y)
    return y