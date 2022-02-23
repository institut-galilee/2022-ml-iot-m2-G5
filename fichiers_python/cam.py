# -*- coding: utf-8 -*-
"""
Created on Sat Jan 22 16:09:40 2022

@author: User
"""

import numpy as np
import cv2
import threading
from tkinter import *


class Camera(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier('C:/Users/User/anaconda3/Lib/site-packages/cv2/cv2/data/haarcascade_frontalface_default.xml')
        self.faces = None
        self.balise = False
        self._kill = threading.Event()
        self.stop_thread = threading.Event()
        

    def run(self):
                
        while True:
            ret, frame = self.cap.read()
        
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in self.faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 5)
               
                
        
                
            cv2.imshow('frame', frame)
        
            if cv2.waitKey(1) == ord('q'):
                break
            if (len(self.faces) > 1 ):
                print("DETECTION D'UN DEUXIEME VISAGE !!\nVous êtes eliminé")
                self.balise = True
                self.stop_thread.set()
                #generation d'une popup d'alerte
                LARGE_FONT= ("Verdana", 12)
                NORM_FONT = ("Helvetica", 10)
                SMALL_FONT = ("Helvetica", 8)
        
                msg = "Nous avons détecté un autre visage, l'examen est fini" 
                popup = Tk()
                popup.wm_title("Alerte !")
                label = Label(popup, text=msg, font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)
                B1 = Button(popup, text="Confirmer", command = popup.destroy)
                B1.pack()
                popup.mainloop()
                break
                
                
            
        self.cap.release()
        cv2.destroyAllWindows()