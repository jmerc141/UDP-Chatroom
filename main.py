import os, sys
import tkinter as tk
from tkinter import ttk
import TKinterModernThemes as TKMT
from client import Connection

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, title, theme = '', mode = '', usecommandlineargs=True, useconfigfile=True):
        super().__init__(title, theme, mode, usecommandlineargs, useconfigfile)

        self.master.protocol('WM_DELETE_WINDOW', self.on_close)
        self.master.iconbitmap(self.resource_path('chat.ico'))
        
        self.text = ''
        self.chatEntry = tk.StringVar()

        #l = ttk.Label(self.popup, text='Enter IP/Host of server:')
        self.eserv = tk.StringVar()
        #ln= ttk.Label(self.popup, text='Enter username:')
        self.en = tk.StringVar()
        #b = ttk.Button(self.popup, text='Connect', command=self.initc)

        self.ssFrame = self.addLabelFrame('Server Select')
        self.ssFrame.Label('Enter IP/Host of server:', 10, 'normal', pady=(5,0))
        self.ssFrame.Entry(self.eserv, pady=(0,5))
        self.ssFrame.Label('Enter username:', 10, 'normal', pady=0)
        self.ssFrame.Entry(self.en, pady=(0,5))
        self.ssFrame.AccentButton('Connect', self.tryConnect)
        

    def tryConnect(self):
        self.cl = Connection(self.eserv.get(), self.en.get())
        if self.cl:
            for w in self.ssFrame.widgets:
                print(w)
                print(dir(w))
            self.ssFrame.master.grid_forget()
            self.ssFrame.master.destroy()
            
            self.master.update()
            self.main_win()
        else:
            tk.messagebox.showerror('Connection Error', 'Cannot connect to server')
            self.eserv.set('')


    def submit(self, ev=None):
        self.cl.sub(self.e.get())
        self.e.delete(0, tk.END)


    def main_win(self):
        self.master.geometry('400x400')
        self.tframe = self.addLabelFrame('Chat', 0, 0, pady=5)
        self.bframe = self.addLabelFrame('Entry', 1, 0, pady=5)

        self.ta = self.tframe.Text('', fontargs=28, sticky='news', row=0, col=0)
        
        self.e = self.bframe.Entry(self.chatEntry, 0, 0)
        self.e.bind('<Return>', self.submit)
        self.bframe.AccentButton('Submit', self.submit, ('',), 0, 1)

        self.bframe.master.columnconfigure(0, weight=1)

        self.master.after(1000, self.appen)


    '''
    Runs every 1 second, checks for messages on the message queue
    '''
    def appen(self):
        if len(self.cl.message_q) > 0:
            self.text += self.cl.message_q.pop() + '\n'
            self.ta.configure(text=self.text)
            
            #self.ta.config(state='normal')
            #self.ta.insert('end', text + '\n')
            #self.ta.see('end')
            #self.ta.config(state='disabled')
        self.master.after(1000, self.appen)


    def on_close(self):
        if self.cl:
            self.cl.cleanup()
        self.master.destroy()

    '''
    Added for pyinstaller images
    '''
    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    app = App('ChatPy','azure', 'dark')
    app.run()