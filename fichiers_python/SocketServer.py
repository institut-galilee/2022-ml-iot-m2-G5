# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 13:02:46 2022

@author: User
"""

#Imports Modules
import socket
import cv2
import time
import os
import threading
from tkinter import *
#Definition classe Serveur 
class Serveur(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.listensocket = socket.socket()
        self.Port = 8000
        self.maxConnections = 999
        self.IP = socket.gethostname() #Gets Hostname Of Current Macheine
        self.local_ip = socket.gethostbyname(self.IP)
        self.file_name = "C:/Users/User/AndroidStudioProjects/logLabel.txt" #get file of predict label in the app
        self.label = ""
        #self.labelInterdits = ["cellular telephone", "cellular phone", "cellphone", "cell", "mobile phone", "dial telephone", "dial phone", "file", "file cabinet", " iPod"]
        self.ipod = " iPod"
        self.phone = " cellular telephone, cellular phone, cellphone, cell, mobile phone"
        self.dialphone = " dial telephone, dial phone"
        self.file = " file, file cabinet, filing cabinet"
        self.message = ""
        self.balise = False
        self.stop_thread = threading.Event()
        



    def openserver(self):
        print(self.local_ip)
        self.listensocket.bind(('',self.Port))
        
        #Opens Server
        self.listensocket.listen(self.maxConnections)
        print("Server started at " + self.IP + " on port " + str(self.Port))


   
    
    def delete_file(self):
        if os.path.exists(self.file_name):
          os.remove(self.file_name)
          print("logLabel.txt is deleted successfully !")
        else:
          print("The file does not exist")
    

    def run(self):
        running = True
        
        while running:
            #Accepts Incomming Connection
            
            (clientsocket, address) = self.listensocket.accept()
            
            self.message = clientsocket.recv(4096).decode() #Receives Message
            
            if self.message != '':
                            
                if(float(self.message) > 5):
                    print(self.message)
                    print("mouvement brusque, fin de l'exam !")
                    self.balise = True
                    self.stop_thread.set()
                    
                     #generation d'une popup d'alerte
                    LARGE_FONT= ("Verdana", 12)
                    NORM_FONT = ("Helvetica", 10)
                    SMALL_FONT = ("Helvetica", 8)
            
                    msg = "Mouvement brusque, fin de l'examen"
                    popup = Tk()
                    popup.wm_title("Alerte !")
                    label = Label(popup, text=msg, font=NORM_FONT)
                    label.pack(side="top", fill="x", pady=10)
                    B1 = Button(popup, text="Confirmer", command = popup.destroy)
                    B1.pack()
                    popup.mainloop()
                    exit(1)
    
               
            #lit le fichier log contenant les labels enregistré par notre application
            with open(os.path.join(os.path.dirname(__file__), self.file_name), 'r') as read_label:
                # Read all lines in the file one by one
                for line in read_label:
                    # prend le mot apres "getPredictedLabel:" afin de recuperer le label
                    if 'getPredictedLabel:' in line:
                        self.label = line.split('getPredictedLabel:')[1]
                        self.label = self.label.lower().replace(" ", "").strip()
                        #self.label = self.label.replace("\n", "")
                        
                        #si le client est toujours en execution
                        if self.message != '':
                        
                            if self.label in self.ipod.lower().replace(" ", "") or self.label in self.phone.lower().replace(" ", "") or self.label in self.dialphone.lower().replace(" ", "") or self.label in self.file.lower().replace(" ", ""):
                                print("Nous avons détecté :", self.label, "\nVous êtes éliminé")
                                self.balise = True
                                self.stop_thread.set()
                                
                                #generation d'une popup d'alerte
                                LARGE_FONT= ("Verdana", 12)
                                NORM_FONT = ("Helvetica", 10)
                                SMALL_FONT = ("Helvetica", 8)
                        
                                msg = "Nous avons détecté :" + self.label + "\nVous êtes éliminé"
                                popup = Tk()
                                popup.wm_title("Alerte !")
                                label = Label(popup, text=msg, font=NORM_FONT)
                                label.pack(side="top", fill="x", pady=10)
                                B1 = Button(popup, text="Confirmer", command = popup.destroy)
                                B1.pack()
                                popup.mainloop()
                                exit(1)
                                
                        else:
                            print('Au revoir !')
                        
                            running = False
                            
                            self.listensocket.close()
                            break
                    
    
    

          
                           
            
        
            
 