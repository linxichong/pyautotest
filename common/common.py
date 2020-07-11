from common.enum import Messages, FlowNodeProp, FlowNodeType, OptionProp
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import time
import json
from selenium.webdriver.common.action_chains import ActionChains
from common import const
from common.screenshot import Screenshot
import random
import uuid


def get_screenshot(driver,
                   elements=None,
                   is_load_at_runtime=False):
    ob = Screenshot()
    ob.full_Screenshot(driver,
                       save_path=r'./pic/',
                       image_name='%s.png' % uuid.uuid1(),
                       elements=elements,
                       is_load_at_runtime=is_load_at_runtime)


""" 从对象获取指定值 """


def get_item(obj, name):
    val = obj.get(name)
    if val is None:
        raise Exception(Messages.Not_Null % name)
    return val


""" 处理可选操作 """


def handle_option(driver, option):
    # 处理无参数命令
    if isinstance(option, str):
        if option == OptionProp.Refresh.value:
            driver.refresh()
        elif option == OptionProp.Close.value:
            driver.close()
        elif option == OptionProp.ScreenShot.value:
            get_screenshot(driver)
    # 处理带参数命令
    elif isinstance(option, dict):
        opt_type = option['type']
        params = option['params']
        if opt_type == OptionProp.Wait.value:
            time.sleep(params)
        elif opt_type == OptionProp.Switch.value:
            swtich_window(driver, params)
        elif opt_type == OptionProp.ScreenShot.value:
            if len(params) == 2:
                get_screenshot(driver,
                               elements=params[0],
                               is_load_at_runtime=params[1])
    # 处理多条命令
    elif isinstance(option, list):
        for item in option:
            handle_option(driver, item)


""" 处理点击操作 """


def handle_click(driver, flowdata):
    # 点击次数（默认为1）
    count = flowdata.get(FlowNodeProp.Count.value, 1)
    element = None

    if FlowNodeProp.Target.value in flowdata and FlowNodeProp.FindMethod.value in flowdata:
        # 获取目标元素列表
        elements = get_elements_by_flow(driver, flowdata)
        # 点击目标元素索引（默认为0）
        index = flowdata.get(FlowNodeProp.Index.value, 0)
        # 根据索引获取指定元素
        element = elements[index]
    elif FlowNodeProp.Params.value in flowdata:
        # 获取循环当前参数值
        params = flowdata.get(FlowNodeProp.Params.value)
        if isinstance(params, WebElement):
            element = params

    # 获取节点类型
    t = get_item(flowdata, FlowNodeProp.Type.value)
    # 处理点击操作时，默认先定位到元素，避免因为遮挡出现点击失效
    driver.execute_script("arguments[0].scrollIntoView(false);", element)
    time.sleep(1)

    # 处理单击
    if t == FlowNodeType.Click.value:
        # 操作
        for i in range(count):
            element.click()
    # 处理双击
    elif t == FlowNodeType.DbClick.value:
        action = ActionChains(driver)
        action.double_click(element).perform()


""" 递归来匹配对应的页面元素设置相应的值 """


def recursive_set_data(driver, byType, data, prefix_name=''):
    curr_prefix = ''
    # 当配置项属于aaa.bbb.ccc类的嵌套name
    if isinstance(data, dict):
        for key in data:
            if prefix_name:
                curr_prefix = '%s.%s' % (prefix_name, key)
            else:
                curr_prefix = key
            recursive_set_data(driver, byType, data[key], curr_prefix)
    # 当配置项属于列表
    elif isinstance(data, list):
        for idx, value in enumerate(data):
            curr_prefix = '%s[%s]' % (prefix_name, idx)
            recursive_set_data(driver, byType, value, curr_prefix)
    else:
        set_element_val(driver, byType, data, prefix_name)


""" 页面元素设置相应的值 """


def set_element_val(driver, byType, data, prefix_name=''):
    # 等待到元素查找成功，否则抛出异常
    elements = get_elements(driver, byType, prefix_name)
    # 循环目标元素列表
    for element in elements:
        attr_type = element.get_attribute('type')
        # 隐藏域直接返回
        if attr_type == 'hidden':
            continue
        # checkbox,radio类
        if attr_type in ['checkbox', 'radio']:
            value = element.get_attribute('value')
            if value == data:
                driver.execute_script("arguments[0].click();", element)
        # 输入框
        elif element.tag_name in ['input', 'textarea'] or attr_type == 'file':
            element.clear()
            if isinstance(data, list):
                element.send_keys(random.choice(data))
            else:
                # 首选使用常量值
                element.send_keys(data)
        # select使用selenium提供的封装来操作
        elif element.tag_name == 'select':
            select = Select(element)
            select.select_by_value(data)


""" 根据指定的查找方式获取页面元素集合 """


def get_elements(driver, byType, prefix_name=''):
    # 等待到元素查找成功，否则抛出异常
    wait = WebDriverWait(driver, 10)
    elements = wait.until(
        EC.presence_of_all_elements_located((byType, prefix_name)),
        Messages.Element_Not_Found % (prefix_name, byType))
    return elements


""" 根据指流程节点信息获取页面元素集合 """


def get_elements_by_flow(driver, flowdata):
    # 点击目标元素
    target = get_item(flowdata, FlowNodeProp.Target.value)
    # 获取目标元素方式
    findmethod = get_item(flowdata, FlowNodeProp.FindMethod.value)
    # 获取目标元素列表
    elements = get_elements(driver, By.__dict__[findmethod], target)
    return elements


""" 根据指定的查找方式获取页面元素 """


def get_element(driver, byType, prefix_name=''):
    elements = get_elements(driver, byType, prefix_name)
    return elements.get(0)


""" 根据指流程节点信息获取页面元素 """


def get_element_by_flow(driver, flowdata):
    # 获取目标元素列表
    elements = get_elements_by_flow(driver, flowdata)
    return elements[0]


""" 读取流程配置文件 """


def open_file(driver, file_url, do_flow, param=None):
    with open(file_url, encoding='utf-8') as f:
        flow_data = json.load(f)
        for no in flow_data:
            if no.startswith('n'):
                continue
            obj = flow_data[no]
            if param:
                obj[FlowNodeProp.Params.value] = param
            do_flow(driver, obj)


""" 获取动态参数生成的项目值 """


def repalce_dynamic_val(flowdata):
    # 目标元素
    target = flowdata.get(FlowNodeProp.Target.value)
    # 获取設定値
    itemval = flowdata.get(FlowNodeProp.ItemVal.value)
    # 动态设置的参数值存在的情况
    if FlowNodeProp.Params.value in flowdata:
        param = get_item(flowdata, FlowNodeProp.Params.value)
        if FlowNodeProp.Format.value in flowdata:
            # 判断获取常量值
            itemval = const.get_const_val(itemval)
            formatstr = get_item(flowdata, FlowNodeProp.Format.value)
            if target and '{0}' in target:
                # 生成动态元素目标值
                target = target.replace('{0}', formatstr).format(param)
            if itemval and '{0}' in itemval:
                # 生成动态字符串值
                itemval = itemval.replace('{0}', formatstr).format(param)
        elif FlowNodeProp.Fragments.value in flowdata:
            fragments = flowdata.get(FlowNodeProp.Fragments.value)
            formatstr = fragments[param]
            if target and '{0}' in target:
                # 生成动态元素目标值
                target = target.replace('{0}', formatstr)
            if itemval and isinstance(itemval, str):
                if '{0}' in itemval:
                    # 生成动态字符串值
                    itemval = itemval.replace('{0}', formatstr)
            elif isinstance(itemval, list):
                itemval = itemval[param]

    flowdata[FlowNodeProp.Target.value] = target
    flowdata[FlowNodeProp.ItemVal.value] = itemval

    return flowdata


""" 替换常量操作 """


def repalce_const_val(flowdata):
    # 如果存在常量值优先替换
    itemval = get_item(flowdata, FlowNodeProp.ItemVal.value)
    if isinstance(itemval, str):
        flowdata[FlowNodeProp.ItemVal.value] = const.get_const_val(itemval)
    return flowdata


""" 窗口切换操作 """


def swtich_window(driver, switch_type):
    if len(driver.window_handles) > 1:
        if switch_type == 'new':
            # 原窗口控制句柄
            original_window = driver.current_window_handle
            for window_handle in driver.window_handles:
                if window_handle != original_window:
                    # 控制句柄切换到新窗口
                    driver.switch_to.window(window_handle)
                    break
        elif switch_type == 'origin':
            # 原窗口控制句柄
            original_window = driver.window_handles[0]
            # 关闭当前窗口
            driver.close()
            # 控制句柄切换回主窗口
            driver.switch_to_window(original_window)
