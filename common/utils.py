from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import json
import time
from selenium.webdriver.common.alert import Alert
from common.enum import BrowserType, FlowNodeType, FlowNodeProp, Messages
import pyperclip
from types import MethodType, FunctionType
import copy
import pyautogui
import random
from common.common import get_item, recursive_set_data, handle_click, get_element_by_flow, open_file, repalce_dynamic_val, set_element_val, repalce_const_val, handle_option, get_elements_by_flow
from common import logger, const
from common.decorator import logit, doprocess
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import uuid

# 创建浏览器启动实例
def create_driver(browser, useproxy):
    # ie
    if browser == BrowserType.IE.value:
        driver = webdriver.Ie(executable_path=r"./drivers/IEDriverServer.exe")
    # chrome
    elif browser == BrowserType.Chrome.value:
        chrome_options = webdriver.ChromeOptions()
        # 是否加载代理
        if useproxy:
            chrome_options.add_extension("proxy.zip")
        driver = webdriver.Chrome(
            executable_path=r"./drivers/chromedriver.exe",
            chrome_options=chrome_options)

    return driver


def get_flow_items(flowdata_path):
    flows = {}
    for root, dirs, files in os.walk(flowdata_path, topdown=False):
        if 'hidden' in root:
            continue
        for name in files:
            if name.startswith('cmn_'):
                continue
            flows[name] = os.path.join(root, name)
    return flows

def do_one_flow(driver, path):
    try:
        with open(path, encoding='utf-8') as f:
            filename = f.name
        logger.info(Messages.Start_Flow % filename)
        open_file(driver, path, do_flow)
        logger.info(Messages.End_Flow % filename)
    except Exception as e:
        logger.error(Messages.Flow_Handle_Failed % e)


@logit
@doprocess
def do_flow(driver, flowdata):
    if flowdata:
        # 获取流程节点类型
        t = flowdata.get(FlowNodeProp.Type.value)
        # 流程-打开目标网址
        if t == FlowNodeType.Open.value:
            # 获取目标网站网址
            target_url = get_item(flowdata, FlowNodeProp.TargetURL.value)
            # 如果存在常量值执行替换
            target_url = const.get_const_val(target_url)
            driver.get(target_url)
        # 流程-处理读取数据文件
        elif t == FlowNodeType.Read.value:
            # 读取方式
            findmethod = get_item(flowdata, FlowNodeProp.FindMethod.value)
            # 读取文件路径
            target_url = get_item(flowdata, FlowNodeProp.TargetURL.value)
            # 读取数据文件
            with open(target_url, encoding='utf-8') as f:
                mock_data = json.load(f)
            # 根据数据文件，页面自动赋值
            if mock_data:
                # 获取常量值
                mock_data = const.repalce_const_val(mock_data)
                recursive_set_data(driver, By.__dict__[findmethod], mock_data)
        # 流程-处理单击
        elif t == FlowNodeType.Click.value or t == FlowNodeType.DbClick.value:
            handle_click(driver, flowdata)
        # 流程-处理弹出框
        elif t == FlowNodeType.Alert.value:
            # 等待弹出框出现
            wait = WebDriverWait(driver, 10)
            wait.until(EC.alert_is_present())
            # 获取弹出框
            alert = driver.switch_to.alert
            # 弹出框确认（默认执行弹出框确认操作）
            alert.accept()
        # 流程-剪切板操作(复制)
        elif t == FlowNodeType.Copy.value:
            if flowdata.get(FlowNodeProp.FindMethod.value) != None:
                # 获取目标元素
                element = get_element_by_flow(driver, flowdata)
                if element.text:
                    copy_val = element.text
                elif element.get_attribute('value'):
                    copy_val = element.get_attribute('value')
            else:
                # 如果存在常量值优先替换
                flowdata = repalce_const_val(flowdata)
                flowdata = repalce_dynamic_val(flowdata)
                copy_val = get_item(flowdata, FlowNodeProp.ItemVal.value)
            # 复制到ClipBoard
            pyperclip.copy(copy_val)
        # 流程-剪切板操作(粘贴)
        elif t == FlowNodeType.Paste.value:
            # 获取目标元素
            element = get_element_by_flow(driver, flowdata)
            # 复制到ClipBoard
            setval = pyperclip.paste()
            if setval:
                element.clear()
                # 首选使用常量值
                val = const.get_const_val(setval)
                element.send_keys(val)
        # 流程-添加缓存值
        elif t == FlowNodeType.Cache.value:
            # 获取想要设置的缓存值
            val = get_item(flowdata, FlowNodeProp.ItemVal.value)
            if isinstance(val, str):
                # 首选使用常量值
                val = const.get_const_val(val)
                setval = val
            elif isinstance(val, object):
                setval = json.dumps(val)
            # 获取缓存键
            cachekey = get_item(flowdata, FlowNodeProp.CacheKey.value)
            # 添加浏览器缓存
            driver.add_cookie({'name': cachekey, 'value': setval})
        # 流程-画面要素設定
        elif t == FlowNodeType.SetVal.value:
            # 如果存在常量值优先替换
            flowdata = repalce_const_val(flowdata)
            # 获取动态生成的项目設定値
            flowdata = repalce_dynamic_val(flowdata)
            # 目标元素
            target = get_item(flowdata, FlowNodeProp.Target.value)
            # 获取目标元素方式
            findmethod = get_item(flowdata, FlowNodeProp.FindMethod.value)
            # 获取动态生成的项目設定値
            itemval = get_item(flowdata, FlowNodeProp.ItemVal.value)
            # 指定元素设置缓存值
            set_element_val(driver, By.__dict__[findmethod], itemval, target)
        # 流程-循环操作
        elif t == FlowNodeType.For.value:
            # 子操作流程节点集合
            child_flows = get_item(flowdata, FlowNodeProp.Flow.value)
            if FlowNodeProp.StartIdx.value in flowdata and FlowNodeProp.EndIdx.value in flowdata:
                # 开始索引
                startIdx = get_item(flowdata, FlowNodeProp.StartIdx.value)
                # 结束索引
                endIdx = get_item(flowdata, FlowNodeProp.EndIdx.value)
                # 循环指定索引范围
                for idx in range(int(startIdx), int(endIdx) + 1):
                    handle_for_childflow(driver, child_flows, idx)
            else:
                # 获取目标元素列表
                elements = get_elements_by_flow(driver, flowdata)
                # 循环处理元素列表
                for element in elements:
                    handle_for_childflow(driver, child_flows, element)
        # 流程-加载既存流程文件
        elif t == FlowNodeType.FlowFile.value:
            # 读取文件路径
            file_url = get_item(flowdata, FlowNodeProp.TargetURL.value)
            param = flowdata.get(FlowNodeProp.Params.value)
            open_file(driver, file_url, do_flow, param)
        # 流程-鼠标键盘操作
        elif t == FlowNodeType.KeyBoard.value:
            # 读取鼠标键盘操作
            itemval = get_item(flowdata, FlowNodeProp.ItemVal.value)
            # 获取操作次数
            count = flowdata.get(FlowNodeProp.Count.value, 1)
            source = None
            if FlowNodeProp.Target.value in flowdata and FlowNodeProp.FindMethod.value in flowdata:
                # 读取指定元素
                source = get_element_by_flow(driver, flowdata)
            else:
                source = driver
            for i in range(count):
                source.send_keys(Keys.__dict__[itemval])
                # ActionChains(source).send_keys(Keys.__dict__[itemval]).perform()
        # 获取节点可选操作配置
        option = flowdata.get(FlowNodeProp.Option.value)
        if option:
            # 处理可选操作
            handle_option(driver, option)


""" 处理循环中的子节点 """


def handle_for_childflow(driver, child_flows, params):
    # 处理子流程节点
    for flow in child_flows:
        # 原始流程节点
        source_childflow = child_flows[flow]
        # 浅拷贝临时流程节点
        temp_childflow = copy.copy(source_childflow)
        temp_childflow[FlowNodeProp.Params.value] = params
        # 处理子流程节点
        do_flow(driver, temp_childflow)