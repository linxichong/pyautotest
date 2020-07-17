from functools import wraps
from common import logger
from common.enum import BrowserType, FlowNodeType, FlowNodeProp, Messages
from threading import current_thread
 
def logit(func):
    @wraps(func)
    def with_logging(*args, **kwargs):
        msg = str(args[1])
        logger.info(msg)
        return func(*args, **kwargs)
    return with_logging

def doprocess(func):
    @wraps(func)
    def do_func(*args, **kwargs):
        driver = args[0]
        flowdata = args[1]

        driver.implicitly_wait(10)
        # 处理当前流程节点
        retval = func(*args, **kwargs)
        # 当前节点配置doafter时，完成其对应的操作
        if FlowNodeProp.DoAfter.value in flowdata:
            after_flow = flowdata.get(FlowNodeProp.DoAfter.value)
            if FlowNodeProp.FindMethod.value not in after_flow:
                after_flow[FlowNodeProp.FindMethod.value] = flowdata.get(FlowNodeProp.FindMethod.value)
                after_flow[FlowNodeProp.Target.value] = flowdata.get(FlowNodeProp.Target.value)
            func(driver, after_flow)
        return retval
    return do_func