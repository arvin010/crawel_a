import configparser
from tkinter.messagebox import NO

class Config():
    cf = None

    def __init__(self,conf_file):
        ini_path =f"./config/{conf_file}.ini"
        self.section=conf_file
        self.cf = configparser.ConfigParser()
        self.cf.read(ini_path, encoding='UTF-8')

    def get(self,name,section=None):
        section=section if section else self.section
        return self.cf.get(section, name)

