import os
import sys 
import time
import ctypes
import math
import time

if os.environ['OS'] == 'Windows_NT':
    STATUS_FILE = "C:\\Users\\NAZWA_KAT\\Saved Games\\Frontier Developments\\Elite Dangerous\\Status.json"
else:
    exit()

c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32

altlista = [0]

class StatusFlagsBits(ctypes.LittleEndianStructure):
    _fields_ = [("docked",          c_uint8, 1),
                ("landed",          c_uint8, 1),
                ("landing_gear",    c_uint8, 1),
                ("shields_up",      c_uint8, 1),
                ("supercruise",     c_uint8, 1),
                ("fa_off",          c_uint8, 1),
                ("hardpoints",      c_uint8, 1),
                ("wing",            c_uint8, 1),
                ("lights",          c_uint8, 1),
                ("cargo_scoop",     c_uint8, 1),
                ("silent_run",      c_uint8, 1),
                ("fuel_scoop",      c_uint8, 1),
                ("srv_brake",       c_uint8, 1),
                ("srv_turret",      c_uint8, 1),
                ("srv_board",       c_uint8, 1),
                ("srv_da",          c_uint8, 1),
                ("fsd_masslock",    c_uint8, 1),
                ("fsd_charge",      c_uint8, 1),
                ("fsd_cool",        c_uint8, 1),
                ("low_fuel",        c_uint8, 1),
                ("overheat",        c_uint8, 1),
                ("has_lat_long",    c_uint8, 1),
                ("in_danger",       c_uint8, 1),
                ("interdiction",    c_uint8, 1),
                ("in_ship",         c_uint8, 1),
                ("in_fighter",      c_uint8, 1),
                ("in_srv",          c_uint8, 1),
                ("alt_ar",          c_uint8, 1),
                ("night_vision",    c_uint8, 1),
                ("fsd_jump",        c_uint8, 1),
                ("srv_hb",          c_uint8, 1)]

class StatusFlags(ctypes.Union):
    _anonymous_ = ("bits",)
    _fields_ = [("bits",        StatusFlagsBits),
                ("as_integer",  c_uint32)]

status_flags = StatusFlags()

def radians(degrees):
    return(degrees * math.pi / 180)
    
def degrees(radians):
    return(radians * 180 / math.pi)

def namiar(CurrentLat, CurrentLong, CurrentHeading, TargetLat, TargetLong, Radius):
    Zeta = 0
    Alpha = 0
    Brng = 0
    BrngFinal = 0
    if (CurrentLat <= 90 and CurrentLat >= -90 and CurrentLong <= 180 and CurrentLong >= -180 and TargetLat <= 90 and TargetLat >= -90 and TargetLong <= 180 and TargetLong >= -180):
        PhiA = radians(CurrentLat)
        LambdaA = radians(CurrentLong)
        PhiB = radians(TargetLat)
        LambdaB = radians(TargetLong)
        Zeta = math.acos(math.sin(PhiA) * math.sin(PhiB) + math.cos(PhiA) * math.cos(PhiB) * math.cos(LambdaB - LambdaA))
        Alpha = math.acos((math.sin(PhiB) - math.sin(PhiA) * math.cos(Zeta)) / math.cos(PhiA) * math.sin(Zeta))
        Brng = math.atan2(math.sin(LambdaB - LambdaA) * math.cos(PhiB), math.cos(PhiA) * math.sin(PhiB) - math.sin(PhiA) * math.cos(PhiB) * math.cos(LambdaB - LambdaA))
        BrngFinal = math.atan2(math.sin(LambdaA - LambdaB) * math.cos(PhiA), math.cos(PhiB) * math.sin(PhiA) - math.sin(PhiB) * math.cos(PhiA) * math.cos(LambdaA - LambdaB))
        BrngFinal = degrees(BrngFinal)
        BrngFinal = (BrngFinal + 180) % 360
        Heading = (degrees(Brng) + 360) % 360
        Dist = Zeta * Radius
        Delta = CurrentHeading - Heading
    if math.fabs(Delta) < 15:
        Wskaz = "==<>=="
    else:
        if Delta < 0:
            Wskaz = "--->>>"
        else:
            Wskaz = "<<<---"
    return(Heading, Dist, Wskaz)

def readedstat():
    time.sleep(1) ## mniej nie ma sensu, ED aktualizuje najszybciej status mniej więcej co 1 sek.
    plik = open(STATUS_FILE, 'r')
    if os.stat(STATUS_FILE).st_size > 0: ## czasmi stastus może być pusty
        edstatus = eval(plik.read())
        plik.close()
    else:
        edstatus = 0
    return(edstatus)

wpc = 5
wp = [  [26.8145, -116.2507, 25, "(START) - zajmij pozycję!"],
        [26.8029, -116.2571, 25, "(1) - będzie ostro w prawo"],
        [26.8042, -116.2611, 25, "(2) - zawracasz!"],
        [26.8029, -116.2571, 25, "(1) - to będzie ostro w lewo"],
        [26.8145, -116.2507, 25, "(META)"]]

start=0
c = 0
while c < wpc:
    edstatus = readedstat()
    if edstatus != 0:
        status_flags.as_integer = edstatus['Flags']
        timestamp = edstatus['timestamp']
        if edstatus['Flags'] > 0:
            if status_flags.has_lat_long == 1:
                TargetLat = wp[c][0]
                TargetLong = wp[c][1]
                Radius = wp[c][2]
                WPname = wp[c][3]
                n0 = namiar(edstatus['Latitude'], edstatus['Longitude'], edstatus['Heading'], wp[0][0], wp[0][1], edstatus['PlanetRadius'])
                Dist0 = n0[1]
                n = namiar(edstatus['Latitude'], edstatus['Longitude'], edstatus['Heading'], TargetLat, TargetLong, edstatus['PlanetRadius'])
                Haeding = n[0]
                Dist = n[1]
                Wskaz = n[2]
                print(Wskaz + " | Dist: {:.0f}".format(Dist) + "m | " + WPname)
                if Dist <= Radius:
                    c = c + 1
                if c == 1 and Dist0 >= wp[0][2] and start == 0:
                    timerstart = time.time()
                    print("Stoper wystartował!")
                    start=1
czas = time.time() - timerstart
print("Twój czas to {:.0f} sek.".format(czas)) 
