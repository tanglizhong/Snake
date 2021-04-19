"""
Autor: Lizhong Tang
Matrikelnummer: 4068443
Datum: 20.04.2021
Version: 6.0

Beschreibung des Programms:
Das ist ein "Snake" Programm, in dem man durch die Tastaturtasten "w","s","a" und "d"
oder "up","down","left" und "right" zur Steuerung der Snake. Am Anfang tretet ein Essen
zufällig auf, und Snake fängt immer im Recht Unten an. Nach dem Essen wird die Snake immer Länger.
Snake ist tot,wenn sie an die Wand oder an den eigenen körper gestoßen hat.
Nach dem Tote zeigt uns die Spielnote, Spielstand, Rang, Name, Anzahl des Spieles, beste Note und Zeitdauer.
Man kann egal welche Taste drücken, um das Spiel neu anzufangen.
Nach dem Start kann man den Spielstand und die Hintergrundsfarbe verändern.
Jeder kann 3 Mal spielen,die beste Note von 3 wird in eine note Datei gespeichert.
"""


#Module tkinter,messagebox,colorchooser,random und time
from tkinter import *                    
from tkinter import messagebox,colorchooser       
import random
import time
class SnakeGame:
    def __init__(self):
        # Initialisierung
        
        self.step = 15      
        self.spielnote = -10
        self.rang = 0
        self.anzahl = 1
        self.best = 0
        self.st = 0
        self.et = 0
        self.dt = 0
        
        
        #3 Rechtecke als Anfangssnake, Anfangsstelle
        r = 566
        self.snakeX = [r, r + self.step, r + self.step * 2]
        self.snakeY = [356, 356, 356]
        #Bewegungsrichtung initialisieren
        self.snakeRichtung = 'left'
        self.snakeMove = [-1, 0]
        
        
        # Grenze,Ergebnis,Essen und Snake zeichnen
        self.zeichnen_wand()
        self.zeichnen_ergebnis()
        self.zeichnen_essen()
        self.zeichnen_snake()
        self.spielen()
        fenster.mainloop()
        
        
    #Spieloberfläche erstellen
    def zeichnen_wand(self):
        self.st = time.time()
        canvas.create_rectangle(71,10,595,385,fill=hintergrund)
        x = 71
        for x in range(x,595,self.step):
            canvas.create_line(x+self.step,10,x+self.step,385,fill="black")
        y = 11
        for y in range(y,385,self.step):
            canvas.create_line(70,y+self.step,595,y+self.step,fill="black")
            
            
    #Label für Note,Spielstand,Rang,Name,Anzahl des Spieles,beste Note,Zeitdauer erstellen
    def zeichnen_ergebnis(self):
        global zeit_label
        self.ergebnis()
        self.score_label = Label(canvas, text=" Note :\n  "+str(self.spielnote),bg = "lightblue")
        self.score_label.place(x=3,y=90)
        self.level_label = Label(canvas, text=" Rang : \n "+str(self.rang),bg = "lightblue")
        self.level_label.place(x=3,y=50)
        self.mode_label = Label(canvas, text=" Stand : \n"+ m,bg = "lightblue")
        self.mode_label.place(x=3,y=10)
        self.name_label = Label(canvas, text=" Name :\n"+ name,bg = "lightblue")
        self.name_label.place(x=3,y=130)
        self.anzahl_label = Label(canvas, text=" Anzahl :\n"+ str(self.anzahl) ,bg = "lightblue")
        self.anzahl_label.place(x=3,y=170)
        self.best_label = Label(canvas, text=" Beste :\n"+ str(self.best) ,bg = "lightblue")
        self.best_label.place(x=3,y=210)
        zeit_label = Label(canvas, text="  Zeit :\n"+str(0) + " S",bg = "lightblue")
        zeit_label.place(x=2.5,y=250)
        
  
    #Essen erstellen
    def zeichnen_essen(self):
        while True:
            self.foodx, self.foody = random.randrange(86, 570, self.step), random.randrange(86, 370, self.step)
            #Snake und Essen dürfen nicht auf eine gleiche Stelle auftreten
            if self.foodx not in self.snakeX or self.foody not in self.snakeY:
                canvas.create_rectangle(self.foodx, self.foody, self.foodx + 15, self.foody + 15, fill="red", tags="essen")
                break

            
    #Snake erstellen
    def zeichnen_snake(self):
        canvas.delete("snake")
        x, y = self.snake()  
        for i in range(len(x)):  
            canvas.create_rectangle(x[i], y[i], x[i] + self.step, y[i] + self.step, fill="orange", tags='snake')

            
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
        self.spielnote = self.spielnote + 10
        #50 Punkte als eine Stufe
        if self.spielnote % 50 == 0:
            self.rang = self.spielnote // 50 + 1
            if self.rang > 1:
                messagebox.showinfo(title="Info",message="Glueckwunsch\nRang: "+str(self.rang))
                time.sleep(1)
        return self.spielnote, self.rang
    

    #Urteilung:gegessen oder nicht
    def essen(self):
        if self.snakeX[0] == self.foodx and self.snakeY[0] == self.foody:
            canvas.delete("essen")
            return True
        else:
            return False

        
    #Kopf von  Snake an die Wand oder an die selber
    def tot(self):
        if self.snakeX[0] < 71 or self.snakeX[0] > 595 or self.snakeY[0] < 11 or self.snakeY[0] > 385:
            return True

        for i in range(1, len(self.snakeX)):
            if self.snakeX[0] == self.snakeX[i] and self.snakeY[0] == self.snakeY[i]:
                return True
        else:
            return False

        
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
        global t,file1,rekord,zeit_label
        canvas.bind_all("<Key>", self.move)
        canvas.focus_set()
        while True:
            #Game over
            if self.tot():
                if self.best > self.spielnote:
                    pass
                else:
                    self.best = self.spielnote
                self.best_label = Label(canvas, text=" Beste :\n"+ str(self.best) ,bg = "lightblue")
                self.best_label.place(x=3,y=210)
                rekord = self.best
                self.et = time.time()
                self.dt = self.et - self.st
                zeit_label.place_forget()
                zeit_label = Label(canvas, text="  Zeit :\n "+ str(round(self.dt,2))+" S" ,bg = "lightblue")
                zeit_label.place(x=2.5,y=250)
                zeit = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
                file1.add_command(label=zeit)
                self.gameover()
                break
            
            #gegessen
            elif self.essen():
                self.snakeX[0] += self.snakeMove[0] * self.step
                self.snakeY[0] += self.snakeMove[1] * self.step
                time.sleep(0.005)
                self.snakeX.insert(1, self.foodx)    #2te Stelle steht
                self.snakeY.insert(1, self.foody)
                self.zeichnen_ergebnis()
                self.zeichnen_essen()
                self.zeichnen_snake()
                
            #nichts passiert
            else:
                self.zeichnen_snake()
                #Geschwindigkeit der Snake
                canvas.after(t)
                #Canvas akualisieren
                canvas.update()
                
                
    #game over
    def gameover(self):
        messagebox.showwarning(title="Info",message="Game Over!")
        canvas.delete("essen","snake")
        canvas.bind_all("<Key>", self.restart)
        canvas.create_text(340, 190, text="Druecken Sie bitte egal \nwelche Taste zum Start", font='Helvetica -30 bold', tags='text')
        
        
    #neu starten 
    def restart(self, event):
        zeit_label.place_forget()
        self.anzahl += 1
        if self.anzahl == 4:
            messagebox.showwarning(title="Info",message="Vielen Dank für Ihr Spielen!\nSie haben schon 3 Mal gespielt,die beste Note\nvon Ihnen ist schon in eine note Datei gespeichert geworden")
            button2()
        else:
            canvas.delete("essen", "snake", "text")
            #Initialisierung
            r = 566
            self.snakeX = [r, r + self.step, r + self.step * 2]
            self.snakeY = [356, 356, 356]
            self.snakeRichtung = 'left'
            self.snakeMove = [-1, 0]
            self.spielnote = -10
            self.zeichnen_ergebnis()
            self.zeichnen_essen()
            self.zeichnen_snake()
            self.spielen()


        
#niedrige Geschwindigkeit       
def einfach():
    global t,m,bt_einfach,bt_normal,bt_schwer,topmenu
    bt_einfach.place_forget()
    bt_normal.place_forget()
    bt_schwer.place_forget()
    t = 100
    m = "einfach"
    canvas.delete(foto)
    topmenu.add_command(label="Hintergrund",command=bg)
    SnakeGame()

    
#normale  Geschwindigkeit  
def normal():
    global t,m,bt_einfach,bt_normal,bt_schwer,topmenu
    bt_einfach.place_forget()
    bt_normal.place_forget()
    bt_schwer.place_forget()
    t = 50
    m = "normal"
    canvas.delete(foto)
    topmenu.add_command(label="Hintergrund",command=bg)
    SnakeGame()

    
#hohe  Geschwindigkeit
def schwer():
    global t,m,bt_einfach,bt_normal,bt_schwer,topmenu
    bt_einfach.place_forget()
    bt_normal.place_forget()
    bt_schwer.place_forget()
    t = 20
    #Stand
    m = "schwer"
    canvas.delete(foto)
    #erst Hintergrundsfarbe ändern, nach dem Start
    topmenu.add_command(label="Hintergrund",command=bg)
    SnakeGame()

    
#Menü
def menue():
    global file1,file2,topmenu
    topmenu = Menu(fenster)
    file = Menu(fenster)
    file.add_command(label="einfach",command=einfach)
    file.add_command(label="normal",command=normal)
    file.add_command(label="schwer",command=schwer)
    file1 = Menu(fenster)
    file2 = Menu(fenster)
    file2.add_command(label = "weiter")
    topmenu.add_cascade(label="Stand",menu=file)
    topmenu.add_cascade(label="Pause",menu=file2)
    topmenu.add_cascade(label="Totzeit",menu=file1)
    topmenu.add_command(label="Verlassen",command=button2)
    fenster.config(menu=topmenu)

    
#Hintergrundsfarbe ändern
def bg():
    global hintergrund,zeit_label
    color = colorchooser.askcolor()
    hintergrund = color[1]
    zeit_label.place_forget()
    SnakeGame()

    
#Start, 3 Stände   
def button1():
    global bt_einfach,bt_normal,bt_schwer
    bt1.place_forget()
    bt2.place_forget()
    menue()
    bt_einfach = Button(fenster ,text="einfach",bg="white",command=einfach)       
    bt_einfach.place(x=240,y=200)
    bt_normal = Button(fenster ,text="normal",bg="white",command=normal)       
    bt_normal.place(x=240,y=250)
    bt_schwer = Button(fenster ,text="schwer",bg="white",command=schwer)       
    bt_schwer.place(x=240,y=300)

    
#tk-Fenster schließen
def button2():
    global rekord,name
    file_note = open("note.txt","a")
    file_note.write(name+" "+str(rekord)+"\n")
    file_note.close()
    fenster.destroy()

    
#Button für Start und Ende
def button():
    global bt1,bt2
    bt1 = Button(fenster ,text="START",bg="white",command=button1)       
    bt1.place(x=180,y=200)
    bt2 = Button(fenster ,text="VERLASSEN",bg="white",command=button2)       
    bt2.place(x=180,y=260)

    
#Enter-Taste Event    
def print_name(event):
    global name
    name = event.widget.get()
    name_frame.destroy()
    button()

    
#Anfang des Programms
if __name__ == "__main__":
    hintergrund = "green"
    fenster = Tk()
    rekord = 0
    fenster.geometry("600x400")
    fenster.maxsize(600, 400)
    fenster.minsize(600, 400)
    fenster.title("Snake")
    name_frame = Frame(fenster,width=600, height=400, bg="lightblue")
    name_frame.pack()
    text_label = Label(name_frame,text="Willkommen zum Spiel Snake\n\nGeben Sie bitte Ihren Name ein",font=("bold",22),bg="lightblue")
    text_label.place(x=80,y=35)
    name_label = Label(name_frame, text = "Name: ",font=("bold",15),bg="lightblue")
    name_label.place(x=100,y=200)
    en = Entry(name_frame,bg="lightblue")
    en.place(x=200,y=205)    
    en.bind("<Return>", print_name)
    canvas = Canvas(width=600, height=400, bg="lightblue")
    canvas.pack()
    foto_datei= PhotoImage(file='willkommen.gif')
    foto = canvas.create_image(90,0, anchor='nw', image=foto_datei)
    

