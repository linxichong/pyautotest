
import configparser as cp
import os

ROOT_PATH = os.path.abspath(os.path.dirname(__name__))

class Config:
    def __init__(self, filename):
        filepath = os.path.join(ROOT_PATH, filename)
        self._cfg = cp.ConfigParser()
        self._cfg.read(filepath, encoding='utf-8')

        for section in self._cfg.sections():
            obj = {}
            for option in self._cfg.options(section):
                val = self._cfg.get(section, option)
                if ',' in val:
                    val = val.split(',')
                obj[option] = val

            self.__dict__[section] = obj

    # def get(self, section, option):
    #     if self._cfg.has_option(section, option):
    #         return self._cfg.get(section, option)
    #     return ''


class AppConfig(Config):
    DEFAULT_SECTION = 'settings'

    def __init__(self):
        super(AppConfig, self).__init__('app.ini')

    # def get(self, option):
    #     return super().get(self.DEFAULT_SECTION, option)
        