import configparser


class Utility():
    cf = None

    def __init__(self):
        ini_path = "./config/config.ini"
        self.cf = configparser.ConfigParser()
        self.cf.read(ini_path, encoding='UTF-8')

    def get(self, name):
        return self.cf.get("start_init", name)
