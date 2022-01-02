# -*- coding:UTF-8 -*-

#-------------Import Settings-----------------#
import yaml
yamlfile = open("settings.yaml")
yamlsettings = yaml.load(yamlfile, Loader=yaml.FullLoader)

#--------------Driver Library-----------------#
import RPi.GPIO as GPIO
import OLED_Driver as OLED
import time
from datetime import datetime
from datetime import timedelta
import pymysql
import board
import neopixel
import socket

#---------------Image Library-----------------#
from PIL  import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor

#-------------Other Libraries-----------------#
from getmac import get_mac_address as gma
import requests
import sys
import os
import json

#--------------Define Settings----------------#
pixel_pin = board.D21
num_pixels = 7
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

#-------------Display Functions---------------#
def Start_Splash():
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    logohw = Image.open("ryg-splash.png")
    image.paste(logohw,(0,0))
    image.save("web/oled.png")
    OLED.Display_Image(image)
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((255, 165, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(1)
    pixels.fill((0, 0, 0))
    pixels.show()

def Display_Activation(activationcode):
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    draw = ImageDraw.Draw(image)
    headfont = ImageFont.truetype('cambriab.ttf',16)
    codefont = ImageFont.truetype('cambriab.ttf',36)
    draw.text((5, 5), "Activation Code:", fill = "WHITE", font = headfont)
    draw.text((5, 45), activationcode, fill = "WHITE",font = codefont)
    image.save("web/oled.png")
    OLED.Display_Image(image)

def Display_Avatar(wbxstatus):
    global lenscol
    if wbxstatus == "active":
        pixels.fill((0, 255, 0))
        pixels.show()
        statusimg = "overlays/active.png"
        lenscol = "229954"
    elif wbxstatus == "call":
        pixels.fill((255, 165, 0))
        pixels.show()
        statusimg = "overlays/call.png"
        lenscol = "ffa500"
    elif wbxstatus == "DoNotDisturb":
        pixels.fill((255, 0, 0))
        pixels.show()
        statusimg = "overlays/dnd.png"
        lenscol = "a93226"
    elif wbxstatus == "meeting":
        pixels.fill((255, 165, 0))
        pixels.show()
        statusimg = "overlays/meeting.png"
        lenscol = "ffa500"
    elif wbxstatus == "OutOfOffice":
        pixels.fill((0, 0, 0))
        pixels.show()
        statusimg = "overlays/ooo.png"
        lenscol = "ecf0f1"
    elif wbxstatus == "pending":
        statusimg = "overlays/inactive.png"
        lenscol = "ecf0f1"
    elif wbxstatus == "presenting":
        pixels.fill((255, 0, 0))
        pixels.show()
        statusimg = "overlays/presenting.png"
        lenscol = "a93226"
    elif wbxstatus == "inactive":
        pixels.fill((0, 0, 0))
        pixels.show()
        statusimg = "overlays/inactive.png"
        lenscol = "ecf0f1"
    else:
        pixels.fill((0, 0, 0))
        pixels.show()
        statusimg = "overlays/inactive.png"
        lenscol = "ecf0f1"
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    avpng = Image.open("avatar.png")
    statpng = Image.open(statusimg)
    image.paste(avpng,(0,0))
    image.paste(statpng,(0,0),statpng)
    image.save("web/oled.png")
    OLED.Display_Image(image)


#-----------Connect Database-------------#
#  DB settings pulled from settings.yaml #
#         (see settings.example)         #
#----------------------------------------#
dbServerName    = yamlsettings["Database"]["ServerName"]
dbUser          = yamlsettings["Database"]["Username"]
dbPassword      = yamlsettings["Database"]["Password"]
dbName          = yamlsettings["Database"]["DBName"]
charSet         = "utf8mb4"
cusrorType      = pymysql.cursors.DictCursor

#-----------Import Parameters------------#
interval        = yamlsettings["Parameters"]["Interval"]
displayname     = "User"
lenscol         = "ECF0F1"

#-----------Set Device Name--------------#
devname = gma()

try:
    #---------Display Startup----------#
    pixels.fill((0, 0, 0))
    pixels.show()
    OLED.Device_Init()
    Start_Splash()

    #------Retrieve Settings-------#
    DBConn = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=cusrorType)
    objsettings = DBConn.cursor()
    objsettings.execute("SELECT * FROM settings")
    rssettings = objsettings.fetchone()
    oldavatar = rssettings["avatar"]
    rssettings.clear
    objsettings.close
    DBConn.close
    avsize = (128,128)

    #-------Check Device API-------#
    devurl = 'https://redyellowgreen.net/api/device/'
    hostname = socket.gethostname() + ".local"
    localipaddress = socket.gethostbyname(hostname)
    devpost = {'devname': devname,'localipaddress': localipaddress}
    devresp = requests.post(devurl, data = devpost)
    devdict = json.loads(devresp.text)
    deverror = devdict['error']
    if deverror == "200":
       accesstoken = devdict['accesstoken']
       accessexpires = devdict['accessexpires']
       authstring = "Bearer " + accesstoken
    elif deverror == "404":
       activationcode = devdict['activationcode']
       Display_Activation(activationcode)
       DBConn = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=cusrorType)
       objupdatesettings = DBConn.cursor()
       objupdatesettings.execute("UPDATE settings SET displayname = 'Activation Code: " + activationcode + "', lenscol = 'ecf0f1'")
       DBConn.commit()
       objupdatesettings.close
       DBConn.close
       time.sleep(10)
       while (True):
             devresp = requests.post(devurl, data = devpost)
             devdict = json.loads(devresp.text)
             deverror = devdict['error']
             if deverror == "200":
                accesstoken = devdict['accesstoken']
                accessexpires = devdict['accessexpires']
                authstring = "Bearer " + accesstoken
                OLED.Clear_Screen()
                break
             time.sleep(20)
    else:
       print("Unable to reach web services. Exiting.")
       sys.exit()

    while (True):
        #---Retrieve Webex API Data---#
        wbxurl = "https://webexapis.com/v1/people/me"
        wbxheaders = {'Authorization': authstring}
        wbxresp = requests.get(wbxurl, headers = wbxheaders)
        try:
            wbxdict = json.loads(wbxresp.text)
            avatar = wbxdict['avatar']
            wbxstatus = wbxdict['status']
            displayname = wbxdict['displayName']
            if avatar != oldavatar:
                oldavatar = avatar
                avimg = Image.open(requests.get(avatar, stream=True).raw)
                avimg = avimg.resize(avsize)
                avimg.save("avatar.png", format="png")
            Display_Avatar(wbxstatus)
            time.sleep(interval)
            DBConn = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=cusrorType)
            objupdatesettings = DBConn.cursor()
            objupdatesettings.execute("UPDATE settings SET avatar = '" + avatar + "', displayname = '" + displayname + "', lenscol = '" + lenscol + "'")
            DBConn.commit()
            objupdatesettings.close
            DBConn.close
        except:
            validjson = False
            time.sleep(interval)

except Exception as e:
    print("Exeception occured:{}".format(e))
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
finally:
    print("\r\nShutting down RedYellowGreen")
    pixels.fill((0, 0, 0))
    pixels.show()
    OLED.Clear_Screen()
    GPIO.cleanup()
    image = Image.new("RGB", (OLED.SSD1351_WIDTH, OLED.SSD1351_HEIGHT), "BLACK")
    image.save("web/oled.png")
    DBConn = pymysql.connect(host=dbServerName, user=dbUser, password=dbPassword, db=dbName, charset=charSet,cursorclass=cusrorType)
    objupdatesettings = DBConn.cursor()
    objupdatesettings.execute("UPDATE settings SET displayname = '', lenscol = 'ecf0f1'")
    DBConn.commit()
    objupdatesettings.close
    DBConn.close
