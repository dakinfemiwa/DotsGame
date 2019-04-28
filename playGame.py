
import tkinter
from tkinter import ttk
from tkinter import *
import random
import threading
import time
import math
import queue

#INFO
#   DOTS FORMAT - [create_oval, xValue, yValue]

class Dots:
    def __init__(self):
        self.backgroundsWin = ["#000000", "#CCCCCC"]
        self.backgroundsWinIndex = random.randint(0, len(self.backgroundsWin)-1)
        self.backgroundsWinColour = self.backgroundsWin[self.backgroundsWinIndex]
        self.level = 1

        self.DotsWindow = Tk()
        self.DotsWindow.title("Dots")
        self.DotsWindow.geometry("1200x650")
        self.DotsWindow.config(bg="#000000")

        self.backgroundsDots = ["#AAFFFF", "#FFAAFF", "#AAAAFF", "#FFFFAA", "#FFFFAA"]

        self.DotsCanvas = Canvas(self.DotsWindow, height=650, width=1200, background="#000000")
        self.DotsCanvas.place(relx=.0, rely=.0)

        self.dots = []

        self.totalDots = (25 * (2 ^(self.level - 1)))
        self.vacuumSize = (160 / (2 ^ (self.level - 1)))

        for self.dotNo in range(0, self.totalDots):
            self.dots.append([])
            self.backgroundsDotsIndex = random.randint(0, len(self.backgroundsDots)-1)
            self.backgroundDotsColour = self.backgroundsDots[self.backgroundsDotsIndex]

            self.xValue = random.randint(0, 1150)
            self.yValue = random.randint(0, 600)

            self.dot = self.DotsCanvas.create_oval(self.xValue, self.yValue, self.xValue + 10, self.yValue + 10, fill=self.backgroundDotsColour, outline=self.backgroundDotsColour)
            self.dots[self.dotNo].append(self.dot)
            self.dots[self.dotNo].append(self.xValue)
            self.dots[self.dotNo].append(self.yValue)
            self.dots[self.dotNo].append(self.xValue + 10)
            self.dots[self.dotNo].append(self.yValue + 10)

        self.vacuumX = 250
        self.vacuumY = 500

        self.vacuumCoordinates = [self.vacuumX, self.vacuumY]

        self.vacuum = self.DotsCanvas.create_oval(self.vacuumX, self.vacuumY, self.vacuumX + self.vacuumSize, self.vacuumY + self.vacuumSize, fill="#FFFFFF", outline="#FFFFFF")


        self.thread1 = threading.Thread(target=self.move).start()
        self.thread2 = threading.Thread(target=self.check).start()
        self.thread3 = threading.Thread(target=self.DotsWindow.bind("<Key>", self.vacuumMove)).start()
        self.thread4 = threading.Thread(target=self.DotsWindow.mainloop()).start()


    def check(self):
        self.currentDots = len(self.dots)
        while True:
            for self.dotNO in range(0, len(self.dots) - 1):
                if self.currentDots != len(self.dots):
                    self.currentDots = len(self.dots)
                    print(str(len(self.dots)) + " Left")
                    #print(self.dots)

                self.contact = False

                self.vacuumCentre = [self.vacuumCoordinates[0] + (self.vacuumSize // 2), self.vacuumCoordinates[1] + (self.vacuumSize // 2)]
                self.dotsCentre = [self.dots[self.dotNO][1] + 5, self.dots[self.dotNO][2] + 5]

                for self.angle2 in range(0, 360):
                    d2x = 5 * math.cos(self.angle2)
                    d2y = 5 * math.sin(self.angle2)
                    v2x = self.dotsCentre[0] + d2x
                    v2y = self.dotsCentre[1] + d2y

                    self.checker = ((v2x - float(self.vacuumCentre[0])) ** 2) + ((v2y - float(self.vacuumCentre[1])) ** 2)

                    if self.checker <= (self.vacuumSize ** 2):
                        self.contact = True
                                        
                if self.contact == True:
                    self.DotsCanvas.delete(self.dots[self.dotNO][0])
                    self.dots.pop(self.dotNO)
                    break;
                
            if len(self.dots) == 1:
                print("1 Left")
                #print(self.dots)
                dotNO = 0
                if (((self.vacuumCoordinates[0] - self.dots[self.dotNO][1]) > -(self.vacuumSize)) and ((self.vacuumCoordinates[0] - self.dots[self.dotNO][1]) < (self.vacuumSize))) and (((self.vacuumCoordinates[1] - self.dots[self.dotNO][2]) < (self.vacuumSize)) and ((self.vacuumCoordinates[1] - self.dots[self.dotNO][2]) > -(self.vacuumSize))):
                    self.dot = 0
            if len(self.dots) == 0 or self.dot == 0:
                self.DotsCanvas.delete(self.vacuum)
                if self.level < 5:
                    self.level += 1
                    self.reset()
                else:
                    self.WinMessage = "GAME COMPLETE"
                    self.font = "Ebrima 45"
                    self.WinLabel = Label(self.DotsCanvas, text=self.WinMessage, font=self.font, background=self.backgroundsWin[0], foreground="white")
                    self.WinLabel.place(relx=.25, rely=.1)
                        
            time.sleep(0.01)

    def reset(self):
        self.dots = []

        self.totalDots = (25 * (2  ** (self.level - 1)))
        self.vacuumSize = (160 / (2 ** (self.level - 2)))

        for self.dotNO in range(0, self.totalDots):
            self.dots.append([])
            self.backgroundsDotsIndex = random.randint(0, len(self.backgroundsDots)-1)
            self.backgroundDotsColour = self.backgroundsDots[self.backgroundsDotsIndex]

            self.xValue = random.randint(0, 1150)
            self.yValue = random.randint(0, 600)

            self.dot = self.DotsCanvas.create_oval(self.xValue, self.yValue, self.xValue + 10, self.yValue + 10, fill=self.backgroundDotsColour, outline=self.backgroundDotsColour)
            self.dots[self.dotNO].append(self.dot)
            self.dots[self.dotNO].append(self.xValue)
            self.dots[self.dotNO].append(self.yValue)

        self.vacuumX = 250
        self.vacuumY = 500

        self.vacuumCoordinates = [self.vacuumX, self.vacuumY]

        self.vacuum = self.DotsCanvas.create_oval(self.vacuumX, self.vacuumY, self.vacuumX + self.vacuumSize, self.vacuumY + self.vacuumSize, fill="#FFFFFF", outline="#FFFFFF")        


    def vacuumMove(self, event):
        self.changeX = 0
         #= 0
        if event.keysym == "Left":
            self.changeX = -5
            self.changeY = 0
        if event.keysym == "Right":
            self.changeX = 5
            self.changeY = 0
        if event.keysym == "Up":
            self.changeX = 0
            self.changeY = -5
        if event.keysym == "Down":
            self.changeX = 0
            self.changeY = 5
        self.vacuumCoordinates[0] += self.changeX
        self.vacuumCoordinates[1] += self.changeY

        self.DotsCanvas.move(self.vacuum, self.changeX, self.changeY)

    def move(self):
        while True:
            time.sleep(0.25)
            for self.dotNO1 in range(0, len(self.dots)):
                try:
                    self.changeX = random.randint(-25, 25)
                    #self.dots[dotNO][1] += change
                    self.changeY = random.randint(-25, 25)
                    #self.dots[self.dotNO][2] += change
                    self.DotsCanvas.move(self.dots[self.dotNO1][0], self.changeX, self.changeY)
                except IndexError:
                    pass

Dots()
