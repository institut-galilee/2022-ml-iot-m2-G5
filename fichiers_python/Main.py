# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 14:07:53 2022

@author: User


from SocketServer import Serveur"""
from cam import Camera
from Voice_recognition import Voice_recognizer
#Import the required Libraries
from tkinter import *

import threading

from SocketServer import Serveur




class Main:
    def stop_code(serv, camera, voice):
        
        while (True):
            if serv.balise == True or camera.balise == True or voice.balise ==True:
               
              
               if serv.stop_thread.isSet():
                   camera.stop_thread.set()
                   voice.stop_thread.set()
                   
                   print("Fin des processus1")
                   exit(1)
               if camera.stop_thread.isSet():
                   serv.stop_thread.set()
                   voice.stop_thread.set()
                   serv.join()
              
                   camera.join()
             
                   voice.join()
                   print("Fin des processus2")
                   exit(1)
               if voice.stop_thread.isSet():
                   camera.stop_thread.set()
                   serv.stop_thread.set()
                   serv.join()
              
                   camera.join()
             
                   voice.join()
                   
                   print("Fin des processus3")
                   exit(1)
                           
               
              
           

           
                
            
     
        
    if __name__ == '__main__':
        
        
        #generation d'une popup consigne
        LARGE_FONT= ("Verdana", 12)
        NORM_FONT = ("Helvetica", 10)
        SMALL_FONT = ("Helvetica", 8)

        msg = "1) Personne n'est autorisé à s'approcher de votre écran d'ordinateur pour quelque raison que ce soit \n\n2) Vous ne devez quitter la zone d'examen sous aucun pretexte \n\n3) Vous ne devez pas parler \n\n4) Les appareils mobiles doivent rester hors de porter" 
        popup = Tk()
        popup.wm_title("Consignes")
        label = Label(popup, text=msg, font=NORM_FONT)
        label.pack(side="top", fill="x", pady=10)
        B1 = Button(popup, text="Commencer", command = popup.destroy)
        B1.pack()
        popup.mainloop()

        

        
        
        #lancement du serveur
        serv = Serveur() 
        serv.openserver()
        serv.start()
        
        
        #lancement de la camera 
        camera = Camera()
        camera.start()
        
        #lancement de la reconnaissance vocale
        voice = Voice_recognizer()
        voice.start()
        
        
        
        """stop = stop_code(serv.balise,camera.balise, voice.balise)
        
        if stop :
            exit(1)"""
            
        
        #lancement condition d'arret
        
        condition_arret = threading.Thread(target=stop_code, args=(serv,camera, voice,))
        condition_arret.start()
        
           
  