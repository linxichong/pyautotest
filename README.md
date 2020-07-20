# AutoTest 可配置自动化测试工具

### 项目介绍

  - 使用python+selenium实现的可配置自动化测试工具，只要稍微了解HTML及相关查询器的知识，就可以通过书写测试流程文件来完成测试流程定制，表单自动填写，按钮点击，流程截图，键盘事件，浏览器缓存操作等功能，目前仅支持Chrome, IE浏览器。一部分功能IE浏览器不支持，例如cookie操作，截取完整页等。

### 启动方法

- **开发环境运行**

  - 本地环境请预先安装好python3.8，下载项目到本地任意文件夹，使用pip安装pipenv包，使用vscode加载项目后，在控制台输入```pipenv shell```建立独立开发环境，然后输入```pipenv install```完成项目所需包安装。
  - 本地添加如下**lauch.json**启动文件
    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Python: Current File",
                "type": "python",
                "request": "launch",
                "program": "${workspaceFolder}/autotest.py",
                "console": "integratedTerminal"
            }
        ]
    }
    ```
  - 点击F5即可启动本项目。

- **exe文件运行**
  
  - 在完成开发环境配置后，可以通过项目中提供的**run.bat**文件来生成exe可执行文件来启动项目。

### 使用说明

  - 相关配置文件

    - autotest.yaml 项目全局配置文件，配置诸如默认启动浏览器，是否使用代理等。
    - const.yaml 常量定义，在自定义测试流程时使用

  - 流程文件定义说明

    - 流程文件是**json**格式文件，所有文件都必须放到项目根目录下的**flowdata**文件夹下，文件名取名任意，前缀为**cmn_XXXX.json**的文件将做为通用流程文件，提供给其他流程文件使用，不会直接加载到项目可执行流程文件中。
    - 如下代码所示，每一个键值对代表一个操作步骤，字典键无具体意义，可作为操作提示备注信息，**type**指定操作类型，这里的**open**是指的打开具体网址操作，**targeturl**表示目标网址，**option**表示当前操作后的一些额外动作，例如此处的```{ "type": "wait", "params": 5}```为停顿5秒。
      ```json
      {
        "打开简书": {
          "type": "open",
          "targeturl": "https://www.jianshu.com/",
          "option": { "type": "wait", "params": 5}
        }
      }
      ```
    - **type**包括以下类型
        - **open** 打开指定网址。
          - 必要属性：**targeturl**指定目标网站地址；
          - 可选属性：
            - **option**指定当前操作完成后的一些额外操作，包括**refresh**刷新页面，**wait**停顿，**close**关闭浏览器，**switch**切换窗口，**screenshot**截图；
            - **doafter**指定完成操作后的子操作，语法和父节点一致。
        - **read** 读取指定mock数据文件。
          - 必要属性：
            - **findmethod**指定页面元素使用的选择器，包括**ID，XPATH，LINK_TEXT，PARTIAL_LINK_TEXT，NAME，TAG_NAME，CLASS_NAME，CSS_SELECTOR**；
            - **targeturl**指定读取目标mock文件地址。mock文件作为流程中需要使用的共通数据文件，统一放置在**mockdata**文件夹中，mock文件格式也为json格式，其中的字典键对应与**findmethod**相匹配的查询表达式。
          - 可选属性：**option**，**doafter**。
        - **click** 处理页面元素单击操作。
          - 必要属性：**findmethod**，**target**指定与**findmethod**相匹配的查询表达式；
          - 可选属性：
            - **count**指定点击次数，默认为1次；
            - **index**通过指定索引值从匹配元素集中找到对应元素
            - **option**；
            - **doafter**。
        - **dbclick** 处理页面元素双击操作。
          - 必要属性：**findmethod**，**target**；
          - 可选属性：**option**，**doafter**。
        - **alert** 弹出对话框确认操作。系统中有时在点击关键按钮时会出现相关操作确认提示框，通过配置该节点默认确认进入下一节点。
          - 可选属性：**option**，**doafter**。
        - **copy** 将匹配值复制到剪贴板中，以备后续使用。
          - 必要属性：
            - 通过指定**findmethod**，**target**组合，可以复制页面指定元素值到剪贴板中；
            - 通过指定**itemval**，可以复制其对应值到剪贴板中，**itemval**支持设置常量值，如**copy**操作配置在某循环中，也可通过指定**format**来完成动态值设置。
          - 可选属性：**option**，**doafter**。
        - **paste** 将剪贴板值设置给页面指定元素。
          - 必要属性：**findmethod**，**target**；
          - 可选属性：**option**，**doafter**
        - **for** 循环操作。
          - 必要属性：
            - 通过指定**startidx**，**endidx**组合，完成指定范围的索引循环，其当前索引值可作为动态值提供给循环体内子节点使用；
            - 通过指定**findmethod**，**target**组合，完成对页面匹配元素集的循环操作，当前元素值可提供给循环体内子节点使用。当循环体内**click**子节点未指定元素时，会使用循环中的当前元素进行单击操作。
            - **flow**定义了循环体要处理的子节点集合。
          - 可选属性：**option**，**doafter**
        - **cache** 设置浏览器缓存。
          - 必要属性：
            - **cachekey**指定浏览器缓存键；
            - **itemval**指定缓存键对应的值。
          - 可选属性：**option**，**doafter**
        - **setval** 区别于**read**多项目读取，该操作为对页面单项目的值设定，主要用于设置上传文件，动态值设定等。
          - 必要属性：**findmethod**，**target**, **itemval**；
          - 可选属性：**option**，**doafter**
        - **flowfile** 加载共通流程模板文件。
          - 必要属性：**targeturl**；
          - 可选属性：**option**，**doafter**
        - **keyboard** 键盘操作。多用于点击键盘**PAGE_DOWN**事件完成页面滚动等，不支持键盘键组合。
          - 必要属性：
            - 通过指定**findmethod**，**target**组合，在指定页面元素上施加对应键盘操作。
            - **itemval**指定键盘键值；
          - 可选属性：**option**，**doafter**
    - 其他属性说明
      - **option**包括无参命令，有参命令，也可以通过数组形式包括多个命令。
        - 无参命令：
          - ```{"option":"refresh"}``` 刷新浏览器
          - ```{"option":"close"}``` 关闭浏览器
          - ```{"option":"screenshot"}``` 当前显示窗口截屏
          - ```{"option":"scrollto"}``` 滚动竖向滚动条到底部 
        - 有参命令
          - ```{"option": { "type": "wait", "params": 5} }``` 执行等待，等待时间由**params**参数指定。多用于解决页面加载缓慢问题；
          - ```{"option": { "type": "switch", "params": "new"} }``` 切换到新开窗口；```{"option": { "type": "switch", "params": "origin"} }``` 关闭新窗口后，切换回原始窗口；
          - 截取页面全屏，**params**指定参数数组，第一个参数为页面中需要处理的漂浮元素，**xpath**指定查询元素方式，当前支持*id=xxx*，*class=yyy*, *tag=zzz*等3种方式，**display_page**表示漂浮元素要显示的位置，一般情况下漂浮元素如简书的头需要显示在截屏的首页则设置为**first**，如简书的返回顶部按钮需要显示在截屏的尾页则设置为**last**，截取全屏功能仅通过**Chrome**测试；第二个参数为指定是否需要预先加载完页面，例如简书首页文章列表随着滚动加载，如需要截取全屏则需要设置为**True**，反之对于一次性加载的页面则设置为**False**。
            ```
            {
              "type": "screenshot",
              "params": [
                [
                  { "xpath":"tag=nav", "display_page":"first"},
                  { "xpath":"class=side-tool", "display_page":"last"}
                ],
                "True"
              ]
            }
            ```
          - ```{"option": { "type": "scrollto", "params": 400} }``` 竖向滚动条滚动到指定位置
    - bat文件说明
      - **run.bat** 执行后会在项目根目录生成dist文件夹，里面包含了项目可执行程序exe等相关文件。执行打包前，请先进入**pipenv**所创建的独立环境后，再请执行命令**pip install pyinstaller**安装对应包。
      - **zip.bat** 使用windows自带压缩软件，压缩浏览器代理插件用的压缩文件，使用前请先修改**proxy**文件下的代理配置文件**background.js**，直接**cmd**中进入项目目录输入**zip**命令执行。

### 更新日志

  - v1.0.0

### 版权声明

  - 本项目使用[MIT许可证](https://github.com/linxichong/pyautotest/blob/master/LICENSE)。
