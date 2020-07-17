# from common.logger import Logger
from common.const import Const
import logging

# logger = Logger()
# 初始化日志实例并将输出绑定到Multiline控件
# logging.basicConfig(filename='autotest.log',
#             level=logging.DEBUG, 
#             format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.basicConfig()
logger = logging.getLogger('AutoTest')
logger.setLevel(logging.INFO)

const = Const()