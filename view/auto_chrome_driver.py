
from random import randrange
from common.common import create_proxyauth_extension
from view.auto_base_driver import AutoBaseDriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from distutils.util import strtobool
from selenium.webdriver.chrome.service import Service as ChromeService


class AutoChromeDriver(AutoBaseDriver):
    def __init__(self, *args):
        super(AutoChromeDriver, self).__init__(*args)

        

        headless = strtobool(self._appconfig.chrome['headless'])
        download_folder = self._appconfig.chrome['download_folder']
        opts = webdriver.ChromeOptions()
        # opts.add_experimental_option('excludeSwitches', ['enable-automation'])
        # opts.add_experimental_option('useAutomationExtension', False)
        # opts.add_argument('--remote-debugging-port=9222')
        # opts.add_argument('--proxy-server=http://10.3.32.201:8080')
        opts.add_argument('--start-maximized')
        opts.add_argument('--disable-gpu')
        if download_folder:
            prefs = {'profile.default_content_settings.popups': 0,
                     "download.default_directory": self._download_folder,
                     "download.prompt_for_download": False,
                     "directory_upgrade": True,
                     "safebrowsing.enabled": True}
            opts.add_experimental_option("prefs", prefs)
        opts.add_argument('--no-sandbox')
        if headless:
            opts.add_argument('--headless')
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        opts.add_argument('--ignore-ssl-errors=yes')
        opts.add_argument('--ignore-certificate-errors')

        # opts.add_argument('blink-settings=imagesEnabled=false')

        opts.add_argument(
            '--user-agent=' + self._user_agent[randrange(0, len(self._user_agent), 1)])
        
        if self._proxy is not None:
            proxy_zip = create_proxyauth_extension(proxy_host=self._proxy['host'], proxy_port=self._proxy['port'],
                                                   bypass_list=self._proxy['bypass_list'], proxy_username=self._proxy['username'], proxy_password=self._proxy['password'])
            opts.add_extension(proxy_zip)
            # PROXY = f"http://{self._proxy['host']}:{self._proxy['port']}"
            # webdriver.DesiredCapabilities.CHROME['proxy'] = {
            #     "httpProxy": PROXY,
            #     "ftpProxy": PROXY,
            #     "sslProxy": PROXY,
            #     "proxyType": "MANUAL",
            # }

        service = ChromeService(
            executable_path=ChromeDriverManager().install())
        self._driver = webdriver.Chrome(service=service, options=opts)
