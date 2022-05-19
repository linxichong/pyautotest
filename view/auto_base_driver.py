
import json
import logging
from common.config import AppConfig

from common.const import Const
from common.utils import do_flow


class AutoBaseDriver():
    def __init__(self, flow_file):
        logging.basicConfig()
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)
        self._logger = logger



        self._const = Const()
        self._appconfig = AppConfig()

        if self._appconfig.proxy['host'] != '':
            self._proxy = self._appconfig.proxy
        else:
            self._proxy = None

        self._user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
                            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                            ]
        
        with open(flow_file, encoding='utf-8') as f:
            flow_data = json.load(f)
            self._flow_data = []
            for no in flow_data:
                if no.startswith('n'):
                    continue
                self._flow_data.append(flow_data[no])
                

    def __exit__(self, exc_type, exc_value, traceback):
        if self._driver is not None:
            self._driver.quit()

    def run(self):
        for item in self._flow_data:
            do_flow(self._driver, item)

    
        