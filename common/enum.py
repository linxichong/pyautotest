from enum import Enum
""" 浏览器类型 """


class BrowserType(Enum):
    Chrome = 'Chrome'
    IE = 'IE'


""" 流程节点操作类型 """


class FlowNodeType(Enum):
    # 打开指定网址
    Open = 'open'
    # 打开指定mock数据
    Read = 'read'
    # 单击操作
    Click = 'click'
    # 双击操作
    DbClick = 'dbclick'
    # 弹出对话框确认操作
    Alert = 'alert'
    # 剪切板操作(复制)
    Copy = 'copy'
    # 剪切板操作(剪贴)
    Paste = 'paste'
    # 循环操作
    For = 'for'
    # 缓存数据操作
    Cache = 'cache'
    # 单项值设置操作
    SetVal = 'setval'
    # 加载既存流程文件
    FlowFile = 'flowfile'
    # 鼠标键盘操作
    KeyBoard = 'keyboard'


""" 流程节点相关属性 """


class FlowNodeProp(Enum):
    # FlowNodeType枚举中定义的可选值
    Type = 'type'
    # 指定打开网址或加载mock数据文件
    TargetURL = 'targeturl'
    # 指定通过何种方式定位页面元素，使用selenium支持的查找方法，具体参考相关文档
    FindMethod = 'findmethod'
    # 指定FindMethod所操作的对象值，可以是ID，NAME或者CSS类等
    Target = 'target'
    # 指定点击操作的次数，默认1次
    Count = 'count'
    # 从对象集合中获取指定Index的操作对象
    Index = 'index'
    # 缓存操作对应的键值
    CacheKey = 'cachekey'
    # 操作时对应的值
    ItemVal = 'itemval'
    # For专用的开始索引
    StartIdx = 'startidx'
    # For专用的结束索引
    EndIdx = 'endidx'
    # 执行当前节点处理后执行
    DoAfter = 'doafter'
    # 动态字符串格式(语法参考python字符串格式化)
    Format = 'format'
    # 参数值(主要用于循环或读取子配置文件等操作中)
    Params = 'params'
    # for循环碎片数组集合
    Fragments = 'fragments'
    # 当前节点处理完成后的可选操作
    Option = 'option'
    # 当前节点子流程
    Flow = 'flow'

""" 可选执行操作 """


class OptionProp(Enum):
    # 是否刷新页面
    Refresh = 'refresh'
    # 是否停顿
    Wait = 'wait'
    # 是否退出selenium驱动
    Close = 'close'
    # 是否切换窗口
    Switch = 'switch'
    # 是否截屏
    ScreenShot = 'screenshot'
    # 是否滚动
    ScrollTo = 'scrollto'


""" 定义系统信息 """


class Messages:
    Element_Not_Found = '根据「%s」方式在画面上找不到匹配的元素「%s」。'
    Flow_Handle_Failed = '流程处理异常:「%s」'
    Start_Flow = '流程「%s」执行开始。'
    End_Flow = '流程「%s」执行结束。'
    Not_Null = '%s不能为空。'
    Success_Message = '指定流程执行成功终了！'