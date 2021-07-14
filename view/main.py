from common.utils_yml import exec_flowdata
import PySimpleGUI as sg
from common.utils import get_flowdatas, do_one_flow, create_driver, get_proxy_ip
from view import config
from threading import Thread
from common.widgetlogger import WidgetLogger
from common import logger, appconfig

# 获取所有流程文件
flowdatas = get_flowdatas()
# 浏览器类型定义
brower_types = appconfig.settings['brower_type']
# 浏览器驱动对象
driver = None
# app标题
TITLE = appconfig.system['app_name']
# 流程文件列表控件名
FLOWDATA_LST_KEY = 'lstFlowFile'
# 是否使用内网代理控件名
# USE_PROXY_KEY = 'cbxUseProxy'
# 操作日志显示控件
LOGS_KEY = 'mulLogs'

sg.theme('LightGreen3')


# 选项区UI定义
def get_options():
    columns1 = [sg.Text('启动浏览器')]
    for key in brower_types:
        group = 'grpbrower'
        rdo = sg.Radio(key, group, key=key)
        if key == config['browser']:
            rdo.InitialState = True
        columns1.append(rdo)

    # cbx = sg.Checkbox('启用代理', key=USE_PROXY_KEY)
    # if 'on' == config['use_proxy']:
    #     cbx.InitialState = True
    # columns2 = [cbx]

    options = [sg.Frame('操作选项', [columns1])]

    return options


# 内容区UI定义
def get_contents():
    contents = [
        sg.Listbox(values=list(flowdatas.keys()),
                   size=(100, 10),
                   key=FLOWDATA_LST_KEY)
    ]

    return contents

# 日志输出栏


def get_logs():
    contents = [
        sg.Multiline(
            key=LOGS_KEY,
            autoscroll=True,
            size=(100, 10))
    ]

    return contents


# 按钮区UI定义
def get_buttons():
    return [sg.Button('执行', key='run'), sg.Button('刷新', key='refresh'), sg.Button('test', key='test')]


# 执行选中的流程文件方法
def exec_one(params):
    selected_val, brower_type = params
    # 根据选中项获取文件路径
    path = flowdatas[selected_val]

    if path:
        # 创建执行浏览器驱动实例
        with create_driver(brower_type) as driver:
            # 窗口最大化
            driver.maximize_window()
            if path.endswith('.json'):
                # 具体执行
                do_one_flow(driver, path)
            else:
                # 具体执行
                exec_flowdata(driver, selected_val, path)


# 获取选中的浏览器类型
def get_browser_type(values):
    for key in values:
        if key in brower_types and values[key]:
            return key

def build_params(values):
    selected_val = values[FLOWDATA_LST_KEY][0]
    # use_proxy = values[USE_PROXY_KEY]
    brower_type = get_browser_type(values)

    return selected_val, brower_type

# UI布局对象
layout = [get_options(), get_contents(), get_logs(), get_buttons()]
# 初始化UI窗口
window = sg.Window(TITLE,
                   layout,
                   icon='favicon.ico',
                   default_element_size=(40, 1),
                   grab_anywhere=False)

# 初始化日志实例并将输出绑定到Multiline控件
logwidget = window.find_element(LOGS_KEY)
widget_logger = WidgetLogger(logwidget)
logger.addHandler(widget_logger)

while True:
    event, values = window.Read(timeout=10)
    # 处理刷新事件
    if event == 'refresh':
        flowdatas = get_flowdatas()
        window.find_element(FLOWDATA_LST_KEY).update(list(flowdatas.keys()))
    # 处理执行事件
    elif event == 'run':
        if len(values[FLOWDATA_LST_KEY]) == 0:
            sg.popup_error('错误', '请选择要执行的流程文件！', icon='favicon.ico')
            continue

        params = build_params(values)
        t = Thread(target=exec_one, args=(params,))
        t.start()
    # 处理执行事件
    elif event == 'test':
        print(get_proxy_ip())
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
