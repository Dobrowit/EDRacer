import os
import sys 
import time
import ctypes
import math
import time
from random import seed
from random import randint
from tkinter import *
import winsound

if os.environ['OS'] == 'Windows_NT':
##    EDLOG_PATH = "\Saved Games\Frontier Developments\Elite Dangerous\Status.json"
##    STATUS_FILE = os.environ['HOME'] + EDLOG_PATH
    STATUS_FILE = "C:\\Users\\Radek\\Saved Games\\Frontier Developments\\Elite Dangerous\\Status.json"
else:
    exit()

def makeSound(event):
    filename = [["thunder.wav"],
                ["epic-1.wav"],
                ["epic-2.wav"],
                ["kart-start.wav"],
                ["level-up.wav"],
                ["retro.wav"],
                ["go-go-go.wav"],
                ["blaster-shot.wav"]]

    if event == 0:
        seed(time.time())
        val = randint(0, 2)
        fn = filename[val][0]
    else:
        fn = filename[event][0]

    winsound.PlaySound(fn, winsound.SND_ASYNC)

## GUI

x, y = 0, 0

def startMove(event):
    global x, y
    x = event.x
    y = event.y
def stopMove(event):
    global x, y
    x = None
    y = None
def moving(event):
    global x, y
    x_ = (event.x_root - x)
    y_ = (event.y_root - y)
    root.geometry("+%s+%s" % (x_, y_))
def frame_mapped(e):
    root.update_idletasks()
    root.overrideredirect(True)
    root.state('normal')
def minimize(event):
    root.update_idletasks()
    root.overrideredirect(False)
    #root.state('withdrawn')
    root.state('iconic')
def exitProgram(event):
    os._exit(0)
def hover(event):
    event.widget.config(bg="red")
def unhover(event):
    event.widget.config(bg="black")
def hoverMin(event):
    event.widget.config(bg="grey")
def unHoverMin(event):
    event.widget.config(bg="black")

root = Tk()
root.title("EDRacer - you navigatorand stopwatch")
root.geometry("700x140")
root.iconbitmap('favicon.ico')
root.overrideredirect(True)
root.attributes('-topmost', True)

borderFrame = Frame(root, width=700, height=140, bg="black")
borderFrame.pack_propagate(False)
borderFrame.pack(side=TOP)
borderFrame.bind("<Button-1>", startMove)
borderFrame.bind("<ButtonRelease-1>", stopMove)
borderFrame.bind("<B1-Motion>", moving)
borderFrame.bind("<Map>", frame_mapped)

close = Label(root, font=("Arial", 11), bg="black", fg="orange", anchor=CENTER, text="X", cursor="hand2")
close.place(x=680, y=0, width=20, height=20)
close.bind("<Enter>", hover)
close.bind("<Leave>", unhover)
close.bind("<Button-1>", exitProgram)

holderFrame = Frame(borderFrame, width=700, height=120, bg="black")
holderFrame.pack_propagate(False)
holderFrame.pack(side=BOTTOM)

msg1 = StringVar()
msg1.set("EDRacer")
lab1 = Label(root,
            textvariable = msg1,
            font = ("Courier New", 20),
            bg = "black",
            fg = "orange")
lab1.place(x = 0, y = 20, width = 700, height = 40)

msg2 = StringVar()
msg2.set("Witaj komandorze")
lab2 = Label(root,
            textvariable = msg2,
            font = ("Courier New", 20),
            bg = "black",
            fg = "orange")
lab2.place(x = 0, y = 60, width = 700, height = 40)

msg3 = StringVar()
msg3.set("o7")
lab3 = Label(root,
            textvariable = msg3,
            font = ("Courier New", 20),
            bg = "black",
            fg = "orange")
lab3.place(x = 0, y = 100, width = 700, height = 40)

root.update_idletasks()

def msg(line, text):
    if line == 1:
        msg1.set(text)
    elif line == 2:
        msg2.set(text)
    elif line == 3:
        msg3.set(text)
    root.update()

def guiPause(sec):
    i = 0
    sec = sec * 10
    while i < sec:
        i = i + 1
        root.update()
        time.sleep(0.1)
        
## GUI END

c_uint8 = ctypes.c_uint8
c_uint32 = ctypes.c_uint32

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

def stopWatch(value):
    '''From seconds to Days;Hours:Minutes;Seconds'''
    valueD = (((value/365)/24)/60)
    Days = int (valueD)
    valueH = (valueD - Days)*365
    Hours = int(valueH)
    valueM = (valueH - Hours)*24
    Minutes = int(valueM)
    valueS = (valueM - Minutes)*60
    Seconds = int(valueS)
    time = "{0}:{1}:{2}".format(Hours, Minutes, Seconds)
    return(time)

def radians(degrees):
    return(degrees * math.pi / 180)
    
def degrees(radians):
    return(radians * 180 / math.pi)

def namiar(CurrentLat, CurrentLong, CurrentHeading, TargetLat, TargetLong, Radius):
    Zeta = 0
    Alpha = 0
    Brng = 0
    BrngFinal = 0
    Velocity = 17 # dodać bieżące wyliczanie prędkości
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
        DistDEG = degrees(Zeta)
        Time = 1000 * Zeta * Radius / Velocity
        Delta = CurrentHeading - Heading
    return(Heading, Dist, Delta)

def readedstat():
    try:
        plik = open(STATUS_FILE, 'r')
        if os.stat(STATUS_FILE).st_size > 0: ## czasmi stastus może być pusty
            edstatus = eval(plik.read())
            plik.close()
        else:
            edstatus = 0
    except:
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
wp = [  [26.8145, -116.2507, 25, "START"],
        [26.8029, -116.2571, 25, "zakręt w prawo"],
        [26.8042, -116.2611, 25, "zawrotka do tyłu"],
        [26.8029, -116.2571, 25, "zakręt w lewo"],
        [26.8145, -116.2507, 30, "META"]]
    
##printstatus()
##exit()

##makeSound(0)
guiPause(5)

c0 = 0
while c0 == 0:
    timerstart = 0
    czas0 = 0
    hbtrig = 0
    start = 0
    c = 0
    
    edstatus = readedstat() ## Odczytanie statusu
    status_flags.as_integer = edstatus['Flags']
    while c < wpc and status_flags.in_srv == 1:
        edstatus = readedstat() ## Odczytanie statusu
        if edstatus != 0:
            status_flags.as_integer = edstatus['Flags']
##            timestamp = edstatus['timestamp']
            if edstatus['Flags'] > 0:
                if status_flags.has_lat_long == 1:
                    TargetLat = wp[c][0]
                    TargetLong = wp[c][1]
                    Radius = wp[c][2]
                    WPname = wp[c][3]
                    n = namiar(edstatus['Latitude'], edstatus['Longitude'], edstatus['Heading'], TargetLat, TargetLong, edstatus['PlanetRadius'])
                    Heading = n[0]
                    Dist = n[1]
                    Delta = n[2]

                    if math.fabs(Delta) < 15:
                        Wskaz = "||||> {:3.0f} <||||".format(Heading)
                    else:
                        if Delta < 0:
                            Wskaz = "----- {:3.0f} >>>>>".format(Heading)
                        else:
                            Wskaz = "<<<<< {:3.0f} -----".format(Heading)

                    if Dist < Radius:
                        Wskaz = ">>>>> VVV <<<<<".format(Heading)
                  
                    if czas0 < 1:
                        czastxt = ""
                    else:
                        czastxt = " S: {:.0f} sek.".format(czas0)
                    
                    if hbtrig == 0 and status_flags.srv_brake == 1 and start == 0 and Dist < Radius:
                        ## Przełącznik od hamulca
                        print('Przełącznik od hamulca')
                        lab1.configure(fg="red")
                        hbtrig = 1
                        ## makeSound(3)
                        
                    if start == 1 and Dist <= Radius:
                        ## Następny punkt
                        print('Następny punkt')
                        c = c + 1
                        if c - 1 == 0:
                            makeSound(6) # START
                            print("START")
                        elif c == wpc:
                            makeSound(5) # META
                            print("META")
                        else:
                            makeSound(4) # KOLEJNY PKT.
                            print("KOLEJNY PKT.")

                    if c == 0 and hbtrig == 1 and status_flags.srv_brake == 0 and start == 0 and Dist < Radius:    
                        ## Stoper startuje
                        print('Stoper startuje')
                        lab1.configure(fg="green")
                        timerstart = time.time()
                        start=1
                        hbtrig=0
                        
                    if start == 1:
                        czas0 = time.time() - timerstart
                        
                    if status_flags.srv_brake == 1 and status_flags.cargo_scoop == 1:
                        ## Restart - zaciągnąć hamulec, otworzyć cargo
                        print('Restart')
                        msg(1, "##############################")
                        msg(2, "##############################")
                        msg(3, "##############################")
                        lab1.configure(fg="orange")
                        timerstart = 0
                        czas0 = 0
                        hbtrig = 0
                        start = 0
                        c = 0
                        while status_flags.cargo_scoop == 1:
                            edstatus = readedstat() ## Odczytanie statusu
                            status_flags.as_integer = edstatus['Flags']
                            print("WAIT")
                            guiPause(1)

                    msg(1, Wskaz)
                    msg(2, " D:{:.0f}m".format(Dist) + " P:{:.0f}/{}".format(c+1, wpc) + " R:{:.0f} ".format(Radius) + czastxt)
                    msg(3, WPname)
                          
    czas = time.time() - timerstart
    lab1.configure(fg="orange")
    msg(1, "Twój czas to {:.0f} sek.".format(czas))
    msg(2, stopWatch(czas))
    msg(3, "Aby kontynuować przełącz cargo scoop")
    state = status_flags.cargo_scoop
    while status_flags.cargo_scoop == state:
        edstatus = readedstat() ## Odczytanie statusu
        status_flags.as_integer = edstatus['Flags']
        print("WAIT")
        guiPause(1)

##    else:
##        print("FIGHTER | ", end='')


