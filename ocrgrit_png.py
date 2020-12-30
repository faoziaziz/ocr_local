#!/usr/bin/python2
#
# author      : Aziz Amerul Faozi
# description : This code will use for testing ocr
#
import os
import requests
import mysql.connector
import time
from mysql.connector import errorcode
import base64
#import numpy as np
#import pytesseract
#import cv2

class ocrnanda:

    # Class Variable
    
    conn = None
    DevID = None
    Data = None
    RefSN = None
    init_x = None
    init_y = None
    Image = None
    Teks = None
    idFileTransferStage = None
    path = None
    flagUp = None

    conn = None
    config = {
        'user':'pos_almar',
        'password':'@Alm4r2020',
        'host':'127.0.0.1',
        'port':'3306',
        'database':'trumon'
    }


    def __init__(self, SeqNum, DeviceID, RefSN, ImageBlob):
        # save image
        #
        #
        #
        # Constructor for this class
        self.path = "image/" + str(SeqNUM)+".png"
        self.DevID = DeviceID
        self.Image = ImageBlob
        self.RefSN = SeqNum
        self.idFileTransferStage = RefSN
        self.conn = mysql.connector.connect(**self.config)
        #self.ImageSave()
        self.ImageTranslate()
        print("error")
        

    def ImageSave(self):
        fout = open(self.path, 'wb')
        fout.write(self.Image)
        fout.close()
        

    def ImageTranslate(self):
        global error_count
        # get file from filename

        try:
            #files = {'base': open(self.path, 'rb')}
            #files = {'file': self.Image}
            response = requests.post('http://api.shuhuf.aiseeyou.tech/api/ocrb64p', json={"b64img":self.Image} )
        except:
            error_count = 0
            print("==================")
            print("local OCR >>>")
            time.sleep(3)
            self.LocalOCR()
        else:
            if response.status_code == 200:
                self.Teks=response.json()["OCR"]
                self.flagUp=1
                self.SaveTeksToTable()
                print(str(self.idFileTransferStage) + " converted")
            else:
                if(error_count < 3) :
                    error_count += 1
                    print("==================")
                    print(response)
                    print("reconnect >>>")
                    time.sleep(3)
                    self.ImageTranslate()
                else :
                    error_count = 0
                    print("==================")
                    print(response)
                    print("local OCR >>>")
                    time.sleep(3)
                self.flagUp=99
                self.UpdateFlag()
                    #self.LocalOCR()
            # jika menginginkan local ocr comment flagup dan UpdateFlag
            # dan uncomment localOCR

    def SaveTeksToTable(self):
        # Save to teks
        curr = self.conn.cursor()
        print("SaveTeksToTable")
        query=(""" INSERT INTO `Teks`(`DeviceId`, `RefSN`, `Data`) VALUES (%s, %s, %s)""")
        curr.execute(query, (self.DevID, self.RefSN, self.Teks))
        self.conn.commit()
        self.UpdateFlag()
        curr.close()

    def UpdateFlag(self):
        # update flag
        mycursor = self.conn.cursor()
        query = "UPDATE Ibase SET Flag='%s' WHERE SeqNum = '%s'"
        print("+= da =+")
        mycursor.execute(query, (self.flagUp, self.RefSN, ))
        self.conn.commit()
        #self.UpdateFlag()
        mycursor.close()

        #os.remove("image/temp.png")

    def __del__(self):

        print("Destruktor")
        del self.Image
        del self.idFileTransferStage
        del self.flagUp
        # del self.Teks

# Main program
config = {
    'user':'pos_almar',
    'password':'@Alm4r2020',
    'host':'127.0.0.1',
    'port':3306,
    'database':'trumon'
}

print("start")
error_count = 0
conn = mysql.connector.connect(**config)
sql_get_query = """select * from Ibase where Flag='0'""";
curr = conn.cursor()
curr.execute(sql_get_query)
rows = curr.fetchall()
for row in rows:
    # SeqNUM  ->
    # RefSN ->
    # ImageBlob ->
    SeqNUM = row[0]
    print("SeqNUM "+ str(SeqNUM))
    DeviceID = row[1]
    
    RefSN = row[2]
    ImageBlob =row[3]
    
    ocrnanda(SeqNUM, DeviceID, RefSN, ImageBlob)

print("end")
curr.close()
conn.close()
