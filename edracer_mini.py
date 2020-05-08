import os
import sys 
import time
import ctypes
import math
import time

if os.environ['OS'] == 'Windows_NT':
##    EDLOG_PATH = "\Saved Games\Frontier Developments\Elite Dangerous\Status.json"
##    STATUS_FILE = os.environ['HOME'] + EDLOG_PATH
    STATUS_FILE = "C:\\Users\\Radek\\Saved Games\\Frontier Developments\\Elite Dangerous\\Status.json"
else:
    exit()

c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32

altlista = [0]

class StatusFlagsBits(ctypes.LittleEndianStructure):
# How to define a bit-field structure in Python:
# https://wiki.python.org/moin/BitManipulation
# Definitions of bits 
# https://forums.frontier.co.uk/threads/journal-docs-for-v3-7-fleet-carriers-beta.540745/
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
##    Velocity = 17
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
##        DistDEG = degrees(Zeta)
##        Time = 1000 * Zeta * Radius / Velocity
        Delta = CurrentHeading - Heading
    if math.fabs(Delta) < 15:
        Wskaz = "==<>=="
    else:
        if Delta < 0:
            Wskaz = "--->>>"
        else:
            Wskaz = "<<<---"
#    print(str(Delta) + " " + wskaz + " Heading: {:.4f}".format(Heading) + " | Dist: {:.0f}".format(Dist))
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

def printstatus():
    edstatus = readedstat()
    if edstatus != 0:
        status_flags.as_integer = edstatus['Flags']
        print("timestamp: " + str(edstatus['timestamp']))
        if edstatus['Flags'] > 0:
            print("Flags:")
            print("  alt_ar " + str(status_flags.alt_ar))
            print("  cargo_scoop: " + str(status_flags.cargo_scoop))
            print("  fa_off: " + str(status_flags.fa_off))
            print("  fsd_charge: " + str(status_flags.fsd_charge))
            print("  fsd_cool: " + str(status_flags.fsd_cool))
            print("  fsd_jump: " + str(status_flags.fsd_jump))
            print("  fsd_masslock: " + str(status_flags.fsd_masslock))
            print("  fuel_scoop: " + str(status_flags.fuel_scoop))
            print("  hardpoints: " + str(status_flags.hardpoints))
            print("  has_lat_long: " + str(status_flags.has_lat_long)) ## jstem na planecie i mam współrzędne
            print("  in_danger: " + str(status_flags.in_danger)) ## jestem pod ostrzałem
            print("  in_fighter: " + str(status_flags.in_fighter))
            print("  in_ship: " + str(status_flags.in_ship))
            print("  in_srv: " + str(status_flags.in_srv)) ## jestes w srv
            print("  interdiction: " + str(status_flags.interdiction))
            print("  landed: " + str(status_flags.landed))
            print("  landing_gear: " + str(status_flags.landing_gear))
            print("  lights: " + str(status_flags.lights))
            print("  low_fuel: " + str(status_flags.low_fuel))
            print("  night_vision " + str(status_flags.night_vision))
            print("  overheat: " + str(status_flags.overheat))
            print("  shields_up: " + str(status_flags.shields_up))
            print("  silent_run: " + str(status_flags.silent_run))
            print("  srv_board: " + str(status_flags.srv_board))
            print("  srv_brake: " + str(status_flags.srv_brake))
            print("  srv_da: " + str(status_flags.srv_da))
            print("  srv_hb: " + str(status_flags.srv_hb))
            print("  srv_turret: " + str(status_flags.srv_turret))
            print("  supercruise: " + str(status_flags.supercruise))
            print("  wing: " + str(status_flags.wing))
            print("Pips: ")
            print("  SYS: " + str(edstatus['Pips'][0]))
            print("  ENG: " + str(edstatus['Pips'][1]))
            print("  WEP: " + str(edstatus['Pips'][2]))
            print("Fuel: ")
            print("  FuelMain: " + str(edstatus['Fuel']['FuelMain']))
            print("  FuelReservoir: " + str(edstatus['Fuel']['FuelReservoir']))
            print("FireGroup: " + str(edstatus['FireGroup']))
            print("GuiFocus: " + str(edstatus['GuiFocus']))
            print("Cargo: " + str(edstatus['Cargo']))
            print("LegalState: " + edstatus['LegalState'])
            if status_flags.has_lat_long == 1:
                print("GEO:")
                print("  Altitude: " + str(edstatus['Altitude']))
                print("  BodyName: " + edstatus['BodyName'])
                print("  Heading: " + str(edstatus['Heading']))
                print("  Latitude: " + str(edstatus['Latitude']))
                print("  Longitude: " + str(edstatus['Longitude']))
                print("  PlanetRadius: " + str(edstatus['PlanetRadius']))


## Lat | Long | Radius | Opis
##wpc = 14
##wp = [  [26.7968, -116.2396, 60, "(START) - między dużymi landing padami"],
##        [26.8008, -116.2684, 90, "(1) - plac za Wieżą-1"],
##        [26.7972, -116.2864, 90, "(2) - panele słoneczne"],
##        [26.8059, -116.2872, 25, "(3) - wjazd na duży landing pad i w lewo"],
##        [26.8158, -116.2884, 25, "(4) - tuż za skrętem w prawo"],
##        [26.8172, -116.2745, 25, "(5) - prosto do końca, skręt w prawo i pierwszy zjazd po lewej "],
##        [26.8425, -116.2447, 90, "(6) - objechać działo jonowe"],
##        [26.8145, -116.2507, 25, "(7) - miń najbliższy panel słoneczny z lewej i dalej prosto"],
##        [26.8029, -116.2571, 25, "(8) - to będzie ostro w prawo"],
##        [26.8042, -116.2611, 25, "(9) - koniec gładkiej drogi"],
##        [26.7960, -116.2665, 25, "(10) - za Wieżą-1 szybka droga"],
##        [26.7921, -116.2683, 25, "(11) - ostro w lewo"],
##        [26.7876, -116.2580, 25, "(12) - uwaga na kamienie"],
##        [26.8214, -116.2618, 50, "(META) - do końca jeszcze 1000 metrów"]]

wpc = 5
wp = [  [26.8145, -116.2507, 25, "(START) - zajmij pozycję!"],
        [26.8029, -116.2571, 25, "(1) - będzie ostro w prawo"],
        [26.8042, -116.2611, 25, "(2) - zawracasz!"],
        [26.8029, -116.2571, 25, "(1) - to będzie ostro w lewo"],
        [26.8145, -116.2507, 25, "(META)"]]

##exit()
##printstatus()

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
