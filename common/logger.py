import yaml
import logging
import time

class Logger:
    def __init__(self):
        with open('logger.yaml', encoding='utf-8') as logger_cfg:
            config = yaml.load(logger_cfg, Loader=yaml.SafeLoader)

            log_level = config['level']
            log_type = config['type']
            app_name = self.__class__.__name__
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            logger = logging.getLogger(app_name)
            logger.setLevel(log_level)
            if log_type == 'cmd':
                cmdlogger = logging.StreamHandler()
                logger.addHandler(cmdlogger)
                cmdlogger.setFormatter(formatter)
            elif log_type == 'file':
                filelogger = logging.FileHandler("%s_%s.log" % (app_name, time.strftime("%Y%m%d")))
                logger.addHandler(filelogger)
                filelogger.setFormatter(formatter)
            
            self.logger = logger
    
    def info(self, msg):
        self.logger.info(msg)
    
    def error(self, msg):
        self.logger.error(msg)
    
    def warning(self, msg):
        self.logger.warning(msg)
