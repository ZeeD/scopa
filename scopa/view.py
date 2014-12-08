#!/usr/bin/env python3

import tkinter

class Application(tkinter.Frame):
    def __init__(self):
        tkinter.Frame.__init__(self)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

    def say_hi(self):
        print("hi there, everyone!")

def mainloop():
    tkinter.Tk()
    Application().mainloop()

def pprint(fmt, *elements):
    acc = []
    for element in elements:
        if isinstance(element, list) or isinstance(element, tuple):
            acc.append(', '.join(map(str, element)))
        else:
            acc.append(element)
    print(fmt % tuple(acc))

