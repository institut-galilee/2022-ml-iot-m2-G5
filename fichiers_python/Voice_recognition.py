import speech_recognition
import pyttsx3
import threading
import os.path
from os import path
from tkinter import *


class Voice_recognizer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.recognizer = speech_recognition.Recognizer()
        self.script = "C:/Users/User/AndroidStudioProjects/voix_retranscription/script.txt"
        
        # mots cles présent dans le partiel qui ne faut pas dire
        self.motsClefs =["banane", "pomme", "poire"]
        self.balise = False
        
        self.stop_thread = threading.Event()
    
  
        
    def run(self):
        
        # si notre fichier existe on le supprime
        if path.exists(self.script):
            
            os.remove(self.script)
        while True:
            try:
                with speech_recognition.Microphone() as mic:
                    self.recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                    audio = self.recognizer.listen(mic)
                    
                    text = self.recognizer.recognize_google(audio, language="fr-FR", show_all=True)
                    
                    f = open(self.script, "a")
                    f.write(f"{text}\n\n")
                    f.close()
                    
                     
                    
                    #verification des mots prononcés
                    with open(self.script) as file:
                        contents = file.read()
                        for word in self.motsClefs :
                            if word in contents:
                                print ('Vous avez dit le mot : ', word, ' qui fait partie du partiel, vous êtes éliminés ' )                            
                                self.balise = True
                                self.stop_thread.set()
                                
                                #generation d'une popup d'alerte
                                LARGE_FONT= ("Verdana", 12)
                                NORM_FONT = ("Helvetica", 10)
                                SMALL_FONT = ("Helvetica", 8)
                        
                                msg = "Vous avez dit le mot : " + word + " qui fait partie du partiel, vous êtes éliminés "
                                popup = Tk()
                                popup.wm_title("Alerte !")
                                label = Label(popup, text=msg, font=NORM_FONT)
                                label.pack(side="top", fill="x", pady=10)
                                B1 = Button(popup, text="Confirmer", command = popup.destroy)
                                B1.pack()
                                popup.mainloop()
                                exit(1)
            
                            
               
                    #print(f"{text}")
            except speech_recognition.UnknownValueError():
                 continue
     
   
         
                                
            
        
             


