"""
Autor: Lizhong Tang
Matrikelnummer: 4068443
Datum: 24.04.2021
Version: 6.0

Beschreibung des Programms:
Das ist ein "Snake" Programm, in dem man durch die Tastaturtasten "w","s","a" und "d"
oder "up","down","left" und "right" die Snake steuert. Am Anfang tretet ein Essen
zufällig auf, und Snake fängt immer im Recht Unten an. Nach dem Essen wird die Snake immer Länger.
Snake ist tot,wenn sie an die Wand oder an den eigenen körper gestoßen hat.
Nach dem Tote zeigt uns die Spielnote, Spielstand, Rang, Name, Anzahl des Spieles, beste Note und Zeitdauer.
Man kann Enter-Taste drücken, um das Spiel neu anzufangen.
Nach dem Start kann man den Spielstand und die Hintergrundsfarbe verändern.
Jeder kann 3 Mal spielen,die beste Note von 3 wird in eine note Datei gespeichert.
Name muss Buchstaben sein,und zwar max.5 Buchstaben mit Leerzeichen
Man darf nicht gleichzeitig 2 Tasten drücken,sonst Game Over.
"""


#Module tkinter,messagebox,colorchooser,random und time
from tkinter import *                    
from tkinter import messagebox,colorchooser       
import random
import time
import sys
import pygame

pygame.init()       
pygame.mixer.init()
pygame.mixer.music.load("snake.mp3")



class SnakeSpiel:
    def __init__(self):
        global Tot,rx,ry,bereit,hoch,size,topmenu
        topmenu.delete(index1=leben,index2=None)
        # Initialisierung
        if size == 2:
            self.step=45
            #rx = bereit-self.step*2-3
            #ry = hoch-self.step*3-1
            rx = 71+self.step*30
            ry = 11+self.step*15
           
        elif size == 3:
            self.step = 15
            #rx = bereit-self.step*3-5
            #ry = hoch-self.step*3
            rx = 71+45*30
            ry = 11+45*15
            
        else:
            self.step = 15  
            rx = 551 
            ry = 356   
        self.spielnote = 480
        self.rang = 0
        self.anzahl = 1
        self.best = 0
        self.st = 0
        self.et = 0
        self.dt = 0
        self.xy_x = []
        self.xy_y = []
        
        #3 Rechtecke als Anfangssnake, Anfangsstelle
        self.snakeX = [rx, rx + self.step, rx + self.step * 2]
        self.snakeY = [ry, ry, ry]
        #Bewegungsrichtung initialisieren
        self.snakeRichtung = 'left'
        self.snakeMove = [-1, 0]
        
        
        # Grenze,Ergebnis,Essen und Snake zeichnen
        self.zeichnen_wand()
        self.zeichnen_ergebnis()
        self.zeichnen_essen()
        self.zeichnen_snake()
        self.spielen()
        
        
        
    #Spieloberfläche erstellen
    def zeichnen_wand(self):
        global bereit,hoch
        self.st = time.time()
        canvas.create_rectangle(71,10,bereit-3-self.step,hoch-self.step+2,fill=hintergrund,width=4)
        x = 71
        for x in range(x,bereit-3-self.step*2,self.step):
            canvas.create_line(x+self.step,10,x+self.step,hoch-self.step+2,fill="black")
        y = 11
        for y in range(y,hoch-self.step+2,self.step):
            canvas.create_line(70,y+self.step,bereit-3-self.step,y+self.step,fill="black")
            
            
    #Label für Note,Spielstand,Rang,Name,Anzahl des Spieles,beste Note,Zeitdauer erstellen
    def zeichnen_ergebnis(self):
        global zeit_label,spiel_rang,spiel_note,spieler_name,spiel_zahl,Note_beste,spiel_zeit,modul
        self.ergebnis()
        self.mode_label = Label(canvas,  text=modul + mode,bg = "lightblue")
        self.mode_label.place(x=3,y=10)
        self.level_label = Label(canvas, text=spiel_rang +str(self.rang),bg = "lightblue")
        self.level_label.place(x=3,y=60)
        self.score_label = Label(canvas, text=spiel_note +str(self.spielnote),bg = "lightblue")
        self.score_label.place(x=3,y=110)
        self.name_label = Label(canvas,  text=spieler_name+ name,bg = "lightblue")
        self.name_label.place(x=3,y=160)
        self.anzahl_label = Label(canvas,text=spiel_zahl+ str(self.anzahl) ,bg = "lightblue")
        self.anzahl_label.place(x=3,y=210)
        self.best_label = Label(canvas, text= Note_beste + str(self.best) ,bg = "lightblue")
        self.best_label.place(x=3,y=260)
        zeit_label = Label(canvas,      text= spiel_zeit,bg = "lightblue")
        zeit_label.place(x=2.5,y=310)
     
    #Essen erstellen
    def zeichnen_essen(self):
        while True:
            fall = True
            self.foodx, self.foody = random.randrange(71, bereit-self.step*2, self.step), random.randrange(11, hoch-self.step*2, self.step)
            if self.spielnote >= 50:
                for i in range(len(self.xy_x)):
                    #print(self.xy_x[i],self.foodx,self.xy_y[i],self.foody)
                    if self.xy_x[i] <= self.foodx <= self.xy_x[i]+self.step*3 and self.xy_y[i] <= self.foody <= self.xy_y[i] + self.step*3:
                        fall = False
                        break
                if fall and ((self.foodx not in self.snakeX) or (self.foody not in self.snakeY)):
                    canvas.create_rectangle(self.foodx, self.foody, self.foodx + self.step, self.foody + self.step, fill=essen_farbe, tags="essen")
                    break
            #Snake,Hindernis und Essen dürfen nicht auf eine gleiche Stelle auftreten
            else:
                if(self.foodx not in self.snakeX) or (self.foody not in self.snakeY):
                    canvas.create_rectangle(self.foodx, self.foody, self.foodx + self.step, self.foody + self.step, fill=essen_farbe, tags="essen")
                    break  
            
    #Snake erstellen
    def zeichnen_snake(self):
        canvas.delete("snake","snakekopf","snakekopf1")
        x, y = self.snake()  
        for i in range(1,len(x)):  
            #canvas.create_rectangle(x[i], y[i], x[i] + self.step, y[i] + self.step, fill=snake_farbe, tags='snake')
            canvas.create_oval(x[i], y[i], x[i] + self.step, y[i] + self.step, fill=snake_farbe, tags='snake')
        canvas.create_oval(x[0],y[0],x[0] + self.step, y[0] + self.step, fill="red", tags='snakekopf')
        canvas.create_oval(x[0]+self.step/2-3,y[0]+self.step/2-3,x[0]+self.step/2+3,y[0]+self.step/2+3, fill="black", tags='snakekopf1')
       
        

            
    #Bewegung von Snake
    def snake(self):
        for i in range(len(self.snakeX) - 1, 0, -1):
            self.snakeX[i] = self.snakeX[i - 1]
            self.snakeY[i] = self.snakeY[i - 1]
            #Den Kopf von Snake aktualisieren
        self.snakeX[0] += self.snakeMove[0] * self.step
        self.snakeY[0] += self.snakeMove[1] * self.step
        #x,y
        return self.snakeX, self.snakeY

    
    #Spielnote+10 nach dem essen 
    def ergebnis(self):
        global ton,bereit,hoch,xx,yy,gewonnen,funf,zeit_label
        self.spielnote = self.spielnote + 10
        #50 Punkte als eine Stufe
        if self.spielnote == 500:
            self.et = time.time()
            self.dt = self.et - self.st
            zeit_label = Label(canvas,      text=spiel_zeit+"  "+ str(round(self.dt,2))+" S" ,bg = "lightblue")
            zeit_label.place(x=2.5,y=310)
            if ton == True:
                sound=pygame.mixer.Sound("9.mp3")
                sound.set_volume(0.5)
                sound.play()
                pygame.mixer.music.stop()
            self.score_label = Label(canvas, text=spiel_note +str(self.spielnote),bg = "lightblue")
            self.score_label.place(x=3,y=110)
            self.best_label = Label(canvas, text= Note_beste + str(500) ,bg = "lightblue")
            self.best_label.place(x=3,y=260)
            messagebox.showinfo(title="Info",message=gewonnen)
            button2("verlassen")
        else:
            if ton== True:
                if self.spielnote == 10:
                    pygame.mixer.Sound("1.mp3").play()
                if self.spielnote == 20:
                    pygame.mixer.Sound("2.mp3").play()
                if self.spielnote == 30:
                    pygame.mixer.Sound("3.mp3").play()
                if self.spielnote == 40:
                    pygame.mixer.Sound("4.mp3").play()
            if self.spielnote % 50 == 0:
                self.rang = self.spielnote // 50 + 1
                if 1 < self.rang <11 :
                    if ton== True:
                        pygame.mixer.Sound("pentakill.mp3").play()
                    while True:
                        xx, yy = random.randrange(71+self.step, bereit-self.step*4, self.step), random.randrange(11+self.step, hoch-self.step*3, self.step)
                        
                        if xx <= self.snakeX[0] < xx+self.step*3 and yy <= self.snakeY[0] < yy + self.step*3:
                            continue
                        else:
                            canvas.create_rectangle(xx, yy, xx + self.step*3, yy + self.step*3, fill="black", tags='wand')
                            self.xy_x.append(xx)
                            self.xy_y.append(yy)
                            break
                    messagebox.showinfo(title="Info",message= funf+str(self.rang))
                    time.sleep(1)
                    #pygame.time.delay(1000)
            if self.spielnote == 80:
                if ton == True:
                    pygame.mixer.Sound("8.mp3").play()
            
            
            return self.spielnote, self.rang
    

    #Urteilung:gegessen oder nicht
    def essen(self):
        if self.snakeX[0] == self.foodx and self.snakeY[0] == self.foody:
            canvas.delete("essen")

            return True
        else:
            return False

        
    #Kopf der Snake an die Wand oder an die selber
    def tot(self):
        global Tot,xx,yy,size,bereit,hoch
        hochmax = hoch-self.step
        if size == 2 or size == 3:
            hochmax = hoch-self.step*2
        
        if self.snakeX[0] < 71 or self.snakeX[0] > bereit-self.step*2 or self.snakeY[0] < 11 or self.snakeY[0] > hochmax:
            Tot = True
            return True
        elif self.spielnote >= 50 :
            for i in range(len(self.xy_x)):
                if self.xy_x[i] <= self.snakeX[0] < self.xy_x[i]+self.step*3 and self.xy_y[i] <= self.snakeY[0] < self.xy_y[i] + self.step*3:
                    Tot = True
                    return True
        
        for i in range(1, len(self.snakeX)):
            if self.snakeX[0] == self.snakeX[i] and self.snakeY[0] == self.snakeY[i]:
                Tot = True
                return True
            

        
    #Tastatur Event
    def move(self, event):
        if (event.keysym == 'Right' or event.keysym == 'd') and self.snakeRichtung != 'left':
            self.snakeMove = [1,0]
            self.snakeRichtung = "right"
        elif (event.keysym == 'Up' or event.keysym == 'w') and self.snakeRichtung != 'down':
            self.snakeMove = [0,-1]
            self.snakeRichtung = "up"
        elif (event.keysym == 'Left' or event.keysym == 'a') and self.snakeRichtung != 'right':
            self.snakeMove = [-1,0]
            self.snakeRichtung = "left"
        elif (event.keysym == 'Down' or event.keysym == 's') and self.snakeRichtung != 'up':
            self.snakeMove = [0,1]
            self.snakeRichtung = "down"
        else:
            pass

        
    #Tastatur Event verbinden
    def spielen(self):
        global t,file1,rekord,zeit_label,Tot,ton,stop,Note_beste,spiel_zeit
        canvas.bind_all("<Key>", self.move)
        canvas.focus_set()
        while True:
            #Game over
            if self.tot():
                
                if self.best > self.spielnote:
                    pass
                else:
                    self.best = self.spielnote
                if ton== True:
                    pygame.mixer.music.stop()
                self.xy_x = []
                self.xy_y = []
                self.best_label = Label(canvas, text=Note_beste+ str(self.best) ,bg = "lightblue")
                self.best_label.place(x=3,y=260)
                rekord = self.best
                self.et = time.time()
                self.dt = self.et - self.st
                zeit_label.place_forget()
                zeit_label = Label(canvas,      text=spiel_zeit+"  "+ str(round(self.dt,2))+" S" ,bg = "lightblue")
                zeit_label.place(x=2.5,y=310)
                #zeit = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
                self.gameover()
                break
            
            #gegessen
            elif self.essen():
                if ton== True:
                    pygame.mixer.Sound("essen.mp3").play()
                #time.sleep(0.005)
                
                self.snakeX.insert(1, self.foodx)    #2te Stelle steht
                self.snakeY.insert(1, self.foody)
                
                self.zeichnen_ergebnis()
                self.zeichnen_essen()
                self.zeichnen_snake()
                
            #nichts passiert
            else:
                if stop == False:
                    self.zeichnen_snake()
                #Geschwindigkeit der Snake
                canvas.after(t)
                #Canvas aktualisieren
                canvas.update()


    def relive(self):
        global Tot,zeit_label,topmenu,bereit,hoch,live
        #topmenu.delete(index1=leben,index2=None)
        
        zeit_label.place_forget()
        live.place_forget()
        while True:
            a,b=random.randrange(71+self.step*2, bereit-self.step*3, self.step), random.randrange(11+self.step*2, hoch-self.step*3, self.step)
            if (a not in self.snakeX) or (b not in self.snakeY):
                self.snakeX[0] = a
                self.snakeY[0] = b
                break
        canvas.delete("text","wand")
        Tot = False
        if ton== True:
            pygame.mixer.music.play(-1)
        self.spielen()

            
                
                
    #game over
    def gameover(self):
        global ton,Tot,stop,bereit,hoch,size,leben,leben_button,go,cont,topmenu,live
        stop = False
        live = Button(fenster ,text=leben,bg="green",font=("bold",20),command = self.relive)       
        live.place(x=bereit/2-100, y=50)
        if ton == True:
            pygame.mixer.Sound("gameover.mp3").play()
        messagebox.showwarning(title="Info",message = go)
        canvas.create_text(bereit/2+30, (hoch-10)/2-10, text= cont, font='Helvetica -30 bold', tags='text')
        canvas.bind_all("<Key>", self.restart)
        
        
        
    #neu starten 
    def restart(self, event):
        global Tot,ton,rx,ry,topmenu,live
        live.place_forget()
        Tot = False
        #zeit_label.place_forget()
        self.anzahl += 1
        if self.anzahl == 4:
            if ton== True:
                pygame.mixer.Sound("verlassen.mp3").play()
            messagebox.showwarning(title="Info",message="Vielen Dank für Ihr Spielen!\nSie haben schon 3 Mal gespielt,die beste Note\nvon Ihnen ist schon in eine note Datei gespeichert geworden")
            button2("VERLASSEN")
        else:
            if ton== True:
                pygame.mixer.music.play(-1)
            canvas.delete("essen","snake","snakekopf","snakekopf1","wand","text")
            #Initialisierung
            
            self.snakeX = [rx, rx + self.step, rx + self.step * 2]
            self.snakeY = [ry, ry, ry]
            self.snakeRichtung = 'left'
            self.snakeMove = [-1, 0]
            self.spielnote = -10
            self.st = 0
            self.st = time.time()
            self.zeichnen_ergebnis()
            self.zeichnen_essen()
            self.zeichnen_snake()
            self.spielen()


        
#niedrige Geschwindigkeit       
def einfach(event):
    global t,mode,einf
    if Tot:
        mode = einf
        t = 180
        mode_wahl()
    else:
        messagebox.showinfo(title="Info",message= msg)

#normale  Geschwindigkeit  
def normal(event):
    global t,mode,noma
    if Tot:
        mode = noma
        t = 120
        mode_wahl()
    else:
        messagebox.showinfo(title="Info",message= msg)
       
#hohe  Geschwindigkeit
def schwer(event):
    global t,mode,schw
    if Tot:
        mode = schw
        t = 40
        mode_wahl()
    else:
        messagebox.showinfo(title="Info",message= msg)

def mode_wahl():
    global bt_einfach,bt_normal,bt_schwer,topmenu,canvas,Tot,ton,bag,sf,ef
    bt_einfach.place_forget()
    bt_normal.place_forget()
    bt_schwer.place_forget()
    menue()
    restart()
        
def pause(event):
    global stop,pause_weiter
    if stop:
        stop = False
    else:
        stop = True
        messagebox.showinfo(title="Info",message= pause_weiter)

    
#Menü
def menue():
    global file1,file2,topmenu,mod,pw,tz,bag,sf,ef,einf,noma,schw,ende
    topmenu = Menu(fenster,bg="lightblue")
    file = Menu(fenster,tearoff=0)
    file.add_command(label=einf,command = lambda:einfach("einfach"))
    file.add_command(label=noma,command = lambda:normal("normal"))
    file.add_command(label=schw,command = lambda:schwer("schwer"))
    file1 = Menu(fenster,tearoff=0)
    file2 = Menu(fenster,tearoff=0)
    file3 = Menu(fenster,tearoff=0)
    file3.add_command(label=ende,command= lambda:button2("Verlassen"),accelerator = "         CTRL+Q")   
    topmenu.add_cascade(label=mod,menu=file)
    topmenu.add_command(label=pw,command =lambda:pause("pause"))
    topmenu.add_command(label=bag,command=Hintergrund)
    topmenu.add_command(label=sf,command=Snake_farbe)
    topmenu.add_command(label=ef,command=Essen_farbe)
    topmenu.add_cascade(label=ende,menu=file3)
    topmenu.add_command(label=leben)
    fenster.config(menu=topmenu)
    fenster.bind("<Control-q>",lambda event:button2("Verlassen") )
    #fenster.bind("<Control-e>",lambda event:einfach("einfach") )
    #fenster.bind("<Control-n>",lambda event:normal("normal") )
    #fenster.bind("<Control-s>",lambda event:schwer("schwer") )
    fenster.bind("<space>",lambda event:pause("pause") )
    

def restart():
    global canvas,Tot,ton
    canvas.delete("essen","snake","snakekopf","snakekopf1","wand","text")
    Tot = False
    if ton == True:
        pygame.mixer.music.play(-1)
    SnakeSpiel()
    
#Hintergrundsfarbe ändern
def Hintergrund():
    global hintergrund,Tot,msg
    if Tot:
        color = colorchooser.askcolor()
        if color[1] != None:
            hintergrund = color[1]
            restart() 
    else:
        messagebox.showinfo(title="Info",message= msg)
        
def Snake_farbe():
    global snake_farbe,Tot,msg
    if Tot:
        color = colorchooser.askcolor()
        if color[1] != None:
            snake_farbe = color[1]
            restart()
    else:
        messagebox.showinfo(title="Info",message= msg)
                 
def Essen_farbe():
    global essen_farbe,Tot,msg
    if Tot:
        color = colorchooser.askcolor()
        if color[1] != None:
            essen_farbe = color[1]
            restart()
    else:
        messagebox.showinfo(title="Info",message= msg)
  
#Start, 3 Stände   
def button1():
    global bt_einfach,bt_normal,bt_schwer,bereit,hoch,groß,size,platz,ton
    bt1.place_forget()
    bt2.place_forget()
    if ton== True:
        pygame.mixer.Sound("start.mp3").play()
    bt_einfach = Button(fenster ,text=einf,bg="white",font=("bold",groß),command = lambda:einfach("einfach"))       
    bt_einfach.place(x=0.4*bereit,y=0.5*hoch-platz)
    bt_normal = Button(fenster ,text=noma,bg="white",font=("bold",groß),command = lambda:normal("normal"))       
    bt_normal.place(x=0.4*bereit,y=0.5*hoch)
    bt_schwer = Button(fenster ,text=schw,bg="white",font=("bold",groß),command = lambda:schwer("schwer"))       
    bt_schwer.place(x=0.4*bereit,y=0.5*hoch+platz)
    
    
#tk-Fenster schließen
def button2(event):
    global rekord,name,mode
    
    file_note = open("note.txt","a")
    file_note.write(name+"\t      "+mode+"\t      "+ str(rekord)+"\n")
    file_note.close()
    print("Ergebnis:\n")
    print("Name"+"\t      "+"Stand"+"\t      "+"Note")
    print("------------------------------------")
    print(open("note.txt","r").read())
    pygame.quit()
    fenster.destroy()
    sys.exit()

    
#Button für Start und Ende
def button():
    global bt1,bt2,bereit,hoch,groß,size,platz,start,ende
    if size == 2 or size == 3:
        groß = 20
        platz = 100
    
    
    bt1 = Button(fenster ,text=start,bg="white",command=button1,font=("bold",groß))       
    bt1.place(x=0.3*bereit,y=3/8*hoch)
    bt2 = Button(fenster ,text=ende,font=("bold",groß),bg="white",command = lambda:button2("VERLASSEN"))       
    bt2.place(x=0.3*bereit,y=3/8*hoch+platz)
    
    
#Enter-Taste Event    
def print_name(event):
    global name,canvas,hoch,size,bereit,namefehler,leer
    try:
        name = event.widget.get()
        nlist = list(name)
        for i in range(len(nlist)):
            if ord(nlist[i])==32 or 65 <= ord(nlist[i]) <= 90 or 97 <= ord(nlist[i]) <= 122:
                n = 0
            else:
                n = 1
                break
        if n==0 and len(nlist) <= 5:
            canvas = Canvas(width=bereit, height=hoch, bg="lightblue")
            canvas.pack()
            
            if size == 2 :
                bereit = bereit +23
                hoch = hoch + 3
            if size == 3:
                bereit = bereit -5
                hoch = hoch -13
            
            name_frame.destroy()
            button()
            
        else:
            messagebox.showwarning(title="Info",message= namefehler)
    except:
        
      messagebox.showwarning(title="Info",message= leer)



def Fenster():
    global bereit,hoch,wahl
    while True:
        fenster.update()
        bereit,hoch = fenster.winfo_width(),fenster.winfo_height()
        if wahl:
            break
        
def einstellen(event):
    global wahl,bereit,hoch,size,set
    
    eingabe=event.widget.get()
    if eingabe == "1":
        wahl = True
        size = 1
        frame.destroy()
    elif eingabe == "2":
        wahl = True
        size = 2
        fenster.attributes('-fullscreen', True)
        frame.destroy()
    elif eingabe == "3":
        wahl = True
        size = 3
        fenster.attributes('-fullscreen', True)
        frame.destroy()
    elif eingabe == "4":
        wahl = True
        size = 4
        frame.destroy()
    else:
        messagebox.showwarning(title="Info",message= set)


def sound():
    global ton
    if var.get() == 1:
        ton = True
    else:
        ton = False
def wahl_frame():   
    global frame,a,b,c,d,e,f,g
    frame=Frame(fenster,width=bereit, height=hoch, bg="lightblue")
    frame.pack()
    Label(frame, text = a,font=("bold",20),bg="lightblue").place(x=120,y=70)
    Label(frame, text = b,font=("bold",20),bg="lightblue").place(x=120,y=120)
    Label(frame, text = c,font=("bold",20),bg="lightblue").place(x=120,y=170)
    Label(frame, text = d,font=("bold",20),bg="lightblue").place(x=120,y=220)
    Label(frame, text = e,font=("bold",15),bg="lightblue").place(x=120,y=280)
    eingabe=Entry(frame,bg="lightblue")
    eingabe.focus()
    eingabe.icursor(0)
    eingabe.place(x=180,y=280+5)
    eingabe.bind("<Return>", einstellen)
    Radiobutton(frame, text=f, variable=var,bg="lightblue" ,value=1, command=sound).place(x=520,y=20)
    Radiobutton(frame, text=g, variable=var, bg="lightblue", value=2, command=sound).place(x=520,y=50)  
def name_frame():
    global name_frame,text,name
    if size != 4: 
        name_frame = Frame(fenster,width=bereit, height=hoch, bg="lightblue")
        name_frame.pack()
        text_label = Label(name_frame,text=text,font=("bold",20),bg="lightblue")
        text_label.place(x=bereit/2-210,y=hoch*7/80+50)
        name_label = Label(name_frame, text = name,font=("bold",15),bg="lightblue")
        name_label.place(x=bereit/2-120-50,y=hoch*7/80+165+50)
        en = Entry(name_frame,bg="lightblue")
        en.focus()
        en.icursor(0)
        en.place(x=bereit/2-40-50,y=hoch*7/80+165+5+50)    
        en.bind("<Return>", print_name)
    else:
        fenster.destroy()
        sys.exit()

     
def sprache1():
    global pause_weiter,msg,funf,gewonnen,frame,name_frame,a,b,c,d,e,f,g,text,name,modul,start,ende,einf,noma,schw,mod,pw,bag,sf,ef,spiel_rang,spiel_note,spieler_name,spiel_zahl,Note_beste,spiel_zeit,leben,set,namefehler,leer,go,cont
    sprache_bt2.place_forget()
    foto_label.pack_forget()
    a,b,c,d,e,f,g,text = "1 --- Standard", "2 --- Vollbild","3 --- Vollbild mit mehrere Blöcke", "4 --- verlassen","Wahl: ", "Ton ein","Ton aus","Willkommen zum Spiel Snake\n\nGeben Sie bitte Ihren Name ein"
    name,start,ende,einf,noma,schw,mod,pw,bag,sf,ef = "Name: ","START","VERLASSEN","einfach", "normal", "schwer","Stand","Pause/weiter","Hintergrund","Snakefarbe","Essenfarbe"
    modul,spiel_rang,spiel_note,spieler_name,spiel_zahl,Note_beste,spiel_zeit = "   Stand  \n","   Rang   \n ","   Note   \n  ","   Name   \n","   Anzahl \n","   Beste  \n","   Zeit   \n"
    leben,set,namefehler,leer,go ="WIEDERBELEBEN","Bitte Geben Sie 1,2,3 oder 4 ein !!","Name muss Buchstaben sein,und zwar max.5 Buchstaben mit Leerzeichen","Bitte Geben Sie Ihren Name ein !","Game Over !"
    cont,gewonnen,funf,msg,pause_weiter = "Druecken   Sie   bitte   egal\nwelche-Taste zum Neustart","Gewonnen!!!","Glueckwunsch\nRang: ","erst ändern nach dem Game Over","              Spiel ist schon Pause gemacht\nDrücken Sie bitte Leertaste zum Weitermachen"
   
    wahl_frame()
    Fenster()
    name_frame()

def sprache2():
    global msg,pause_weiter,funf,gewonnen,frame,name_frame,a,b,c,d,e,f,g,text,name,modul,start,ende,einf,noma,schw,mod,pw,bag,sf,ef,spiel_rang,spiel_note,spieler_name,spiel_zahl,Note_beste,spiel_zeit,leben,set,namefehler,leer,go,cont
    sprache_bt1.place_forget()
    sprache_bt2.place_forget()
    foto_label.pack_forget()
    a,b,c,d,e,f,g,text = "1 --- 标准窗口","2 --- 全屏放大", "3 --- 全屏多块","4 --- 离开游戏","选择: ","声音 开启","声音 关闭", "          欢迎来到贪吃蛇\n        请输入您的名字(首字母)"
    name,start,ende,einf,noma,schw,mod,pw,bag,sf,ef = "姓名: ","开始游戏", "退出游戏","简单","一般", "困难", "游戏模式", "暂停/继续", "游戏背景","蛇身颜色","食物颜色"
    modul,spiel_rang,spiel_note,spieler_name,spiel_zahl,Note_beste,spiel_zeit = " 游戏模式\n" ," 游戏等级\n"," 游戏分数\n"," 玩家姓名\n"," 游戏次数\n"," 最佳成绩\n"," 游戏时间\n"
    leben,set,namefehler,leer,go,cont="复活","请输入1，2，3 或者 4 !!","姓名必须是字母，而且包括空格最多5位","请输入您的姓名 ！","游戏结束 !","按任意键重新开始游戏"
    gewonnen,funf,msg,pause_weiter= "游戏胜利！！！","恭喜进入关卡 ","游戏结束后才可以进行操作","游戏已暂停，请按空格键继续"
    wahl_frame()
    Fenster()
    name_frame()
  
       
#Anfang des Programms
if __name__ == "__main__":
    stop = False
    ton = True
    hintergrund = "green"
    mode = "None"
    wahl = False
    size = 1
    groß = 10
    platz = 80
    fenster = Tk()
    rekord = 0
    bereit=600
    hoch=400
    Tot = True
    snake_farbe = "orange"
    essen_farbe = "yellow"
    fenster.geometry("600x400+450+220")
    fenster.title("Snake")
    fenster.resizable(0,0)
    var = IntVar()
    var.set(1)
    width = fenster.winfo_screenwidth()
    height = fenster.winfo_screenheight()
    #fenster.maxsize(width, height)
    #fenster.minsize(600, 400)
    sprache_bt1 = Button(fenster ,text="Deutsch",bg="white",command=sprache1,font=("bold",20))       
    sprache_bt1.place(x=150,y=5)
    sprache_bt2 = Button(fenster ,text="简体中文",font=("bold",20),bg="white",command = sprache2)    
    sprache_bt2.place(x=320,y=5)
    foto = PhotoImage(file = "bg.gif")
    foto_label = Label(fenster,image = foto )
    foto_label.pack(side = BOTTOM)
    fenster.mainloop()
