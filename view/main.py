import PySimpleGUI as sg
from common.utils import get_flow_items, do_one_flow, create_driver, get_proxy_ip
from view import config
from threading import Thread
from common.widgetlogger import WidgetLogger
from common import logger

# 流程文件所在文件夹
flow_file_path = './flowdata'
# 获取所有流程文件
flow_files = get_flow_items(flow_file_path)
# 浏览器类型定义
brower_types = ['Chrome', 'IE']
# 浏览器驱动对象
driver = None

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

    cbx = sg.Checkbox('启用代理', key='cbxUseProxy')
    if 'on' == config['use_proxy']:
        cbx.InitialState = True
    columns2 = [cbx]

    options = [sg.Frame('操作选项', [columns1, columns2])]

    return options


# 内容区UI定义
def get_contents():
    contents = [
        sg.Listbox(values=list(flow_files.keys()),
                   size=(100, 10),
                   key='lstFlowFile')
    ]

    return contents

def get_logs():
    contents = [
        sg.Multiline(
            key='mulLogs',
            autoscroll=True,
            size=(100, 10))
    ]

    return contents


# 按钮区UI定义
def get_buttons():
    return [sg.Button('执行', key='run'), sg.Button('刷新', key='refresh'), sg.Button('test', key='test')]


# 执行选中的流程文件方法
def run(params, brower_type):
    selected_val = params[0]
    use_proxy = params[1]
    # 根据选中项获取文件路径
    path = flow_files[selected_val]

    if path:
        # 创建执行浏览器驱动实例
        with create_driver(brower_type, use_proxy) as driver:
            # 窗口最大化
            driver.maximize_window()
            # 具体执行
            do_one_flow(driver, path)


# 获取浏览器类型
def get_browser_type(values):
    for key in values:
        if key in brower_types and values[key]:
            return key


# UI布局对象
layout = [get_options(), get_contents(), get_logs() , get_buttons()]
# 初始化UI窗口
window = sg.Window('AutoTest',
                   layout,
                   icon='favicon.ico',
                   default_element_size=(40, 1),
                   grab_anywhere=False)

# 初始化日志实例并将输出绑定到Multiline控件
logwidget = window.find_element('mulLogs')
widget_logger = WidgetLogger(logwidget)
logger.addHandler(widget_logger)

while True:
    event, values = window.Read(timeout=10)
    # 处理刷新事件
    if event == 'refresh':
        flow_files = get_flow_items(flow_file_path)
        window.find_element('lstFlowFile').update(list(flow_files.keys()))
    # 处理执行事件
    elif event == 'run':
        if len(values['lstFlowFile']) == 0:
            sg.popup_error('错误', '请选择要执行的流程文件！', icon='favicon.ico')
            continue
        selected_val = values['lstFlowFile'][0]
        use_proxy = values['cbxUseProxy']
        brower_type = get_browser_type(values)
        params = [selected_val, use_proxy]
        t = Thread(target=run, args=(params, brower_type))
        t.start()
    # 处理执行事件
    elif event == 'test':
       print(get_proxy_ip())
    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
