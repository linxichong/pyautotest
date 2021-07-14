# from common.logger import Logger
from common.const import Const
from common.config import AppConfig
import logging

# 初始化日志实例
logging.basicConfig()
logger = logging.getLogger('AutoTest')
logger.setLevel(logging.INFO)

const = Const()
appconfig = AppConfig()

print(appconfig)