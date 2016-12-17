#!/usr/bin/env python3
# TestKeyboard.py
# Python3 scalable Keyboard with Combobox

from tkinter import *
from tkinter import ttk
from functools import partial


class Keyboard: # scalable Keyboard with Combobox
    def __init__(self, parent, Inputvals, Title='Keyboard', Btnsize=28, Font='Helvetica 10'):
        self.top = Toplevel(parent)
        self.top['bg'] = '#AAAAAA'  # window background
        self.top.option_add('*background','#DDDDDD') # widget background
        self.top.title(Title)
        #self.top.overrideredirect(True) # without titlebar
        self.top.geometry(str(Btnsize*10+4)+'x'+str(round(Btnsize*5.8+3))+'+18+20') # size and position
        self.top.resizable(0,0)
        self.top.transient(parent)
        self.top.after(20, lambda: self.top.lift())   # on top
        self.shiftstat = 0
        X = 2
        Y = 1
        self.ComboBox = ttk.Combobox(self.top,height=6)
        self.ComboBox.place(x=X, y=Y, width=Btnsize*10, height=round(Btnsize*0.8))
        Y += round(Btnsize*0.8)
        self.ComboBox.focus()
        self.ComboBox['values'] = Inputvals
        self.ComboBox.current(0)
        self.ComboBox.icursor(END)
        self.ComboBox.bind('<Return>', self.enter)
        self.ComboBox.bind('<Escape>', self.escape)
        self.ComboBox.bind("<<ComboboxSelected>>", self.comboselect)
        self.buttons0 = [
        '1','2','3','4','5','6','7','8','9','0',
        'q','w','e','r','t','y','u','i','o','p',
        'a','s','d','f','g','h','j','k','l','\\',
        '^','z','x','c','v','b','n','m','#','<-',
        'Cancel',',','Space','.','-','+','Enter']
        self.buttons1 = [
        '!','"','§','$','%','&','/','(',')','=',
        'Q','W','E','R','T','Y','U','I','O','P',
        'A','S','D','F','G','H','J','K','L','?',
        '^','Z','X','C','V','B','N','M','@','<-',
        'Cancel',';','Space',':','_','*','Enter']
        n = 0
        self.btn = list(range(len(self.buttons0)))
        for label in self.buttons0:
            cmd = partial(self.click, label) # or: cmd = lambda x=label:self.click(x)
            if label in {'Space','Cancel','Enter'}:
                self.btn[n] = Button(self.top, text=label, command=cmd, font=Font)
                self.btn[n].place(x=X, y=Y, width=Btnsize*2, height=Btnsize)
                X += Btnsize
            else:
                self.btn[n] = Button(self.top, text=label, command=cmd, font=Font)
                self.btn[n].place(x=X, y=Y, width=Btnsize, height=Btnsize)
            X += Btnsize
            n += 1 # button index
            if X > Btnsize*10:
                X = 2
                Y += Btnsize
        self.top.focus_set()  # focus
        self.top.grab_set()   # modal
        self.result = chr(27) # ESC

    def comboselect(self, event):
        self.ComboBox.selection_clear()

    def click(self,btn):
        cursor = self.ComboBox.index(INSERT)
        if btn == 'Cancel':
            self.top.destroy()
        elif btn == 'Enter':
            self.result = self.ComboBox.get()
            self.top.destroy()
        elif btn == '<-':
            self.ComboBox.delete(cursor-1)
        elif btn == 'Space':
            self.ComboBox.insert(cursor,' ')
        elif (btn == '^'):
            self.shift()
        else:
            self.ComboBox.insert(cursor,btn)

    def shift(self):
        n = 0
        if self.shiftstat == 1:
            self.shiftstat = 0
            self.btn[30].config(bg='#DDDDDD')
            for label in self.buttons0:
                cmd = partial(self.click, label)
                self.btn[n].config(text=label, command=cmd)
                n += 1
        else:
            self.btn[30].config(bg='#AAAAAA')
            self.shiftstat = 1
            for label in self.buttons1:
                cmd = partial(self.click, label)
                self.btn[n].config(text=label, command=cmd)
                n += 1
    def escape(self,event):
        self.top.destroy()

    def enter(self,event):
        self.result = self.ComboBox.get()
        self.top.destroy()


def Get_Input():
    Items = ['Item1','Item2', 'Item3']
    KeyInput = Keyboard(root,Items,Title='Keyboard 1', Btnsize=28, Font='Helvetica 10')
    root.wait_window(KeyInput.top)
    if KeyInput.result != chr(27): # ESC or cancel
        print ('Keyboard return: '+KeyInput.result)



root = Tk()
Get_Input()
root.mainloop()

