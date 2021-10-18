import os
from datetime import datetime


class Log:
    def __init__(self, fname):
        self.enable_printing = False
        self.fpath = os.getcwd() + "/"
        self.fname = fname


        if os.path.exists(self.fpath + self.fname) == False:
            print("No " + self.fname + " file found.")
            f = open(self.fname, "w+")
            f.close()
            print(self.fname + " created successfully.")

    def entry(self, message):
        str(message)
        f = open(self.fname, "a")
        f.write("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "]   " + message + "\n")
        if self.enable_printing:
            print(message)
        f.close()

