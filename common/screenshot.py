import os
import time
import uuid

from PIL import Image
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class Screenshot:
    def __init__(self):
        pass

    def full_Screenshot(self,
                        driver: WebDriver,
                        save_path: str = '',
                        image_name: str = 'selenium_full_screenshot.png',
                        elements: list = None,
                        is_load_at_runtime: bool = False,
                        load_wait_time: int = 5):

        image_name = os.path.abspath(save_path + '/' + image_name)

        final_page_height = 0
        original_size = driver.get_window_size()

        if is_load_at_runtime:
            while True:
                page_height = driver.execute_script(
                    "return document.body.scrollHeight")
                if page_height != final_page_height and final_page_height <= 10000:
                    driver.execute_script(
                        "window.scrollTo(0, {})".format(page_height))
                    time.sleep(load_wait_time)
                    final_page_height = page_height
                else:
                    break

        if isinstance(driver, webdriver.Ie):
            required_width = driver.execute_script(
                'return document.body.parentNode.scrollWidth')
            driver.set_window_size(required_width, final_page_height)
            driver.save_screenshot(image_name)
            driver.set_window_size(original_size['width'],
                                   original_size['height'])
            return image_name

        else:
            total_width = driver.execute_script(
                "return document.body.offsetWidth")
            total_height = driver.execute_script(
                "return document.body.parentNode.scrollHeight")
            viewport_width = driver.execute_script(
                "return document.body.clientWidth")
            viewport_height = driver.execute_script(
                "return window.innerHeight")
            driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)
            rectangles = []

            i = 0
            while i < total_height:
                ii = 0
                top_height = i + viewport_height
                if top_height > total_height:
                    top_height = total_height
                while ii < total_width:
                    top_width = ii + viewport_width
                    if top_width > total_width:
                        top_width = total_width
                    rectangles.append((ii, i, top_width, top_height))
                    ii = ii + viewport_width
                i = i + viewport_height
            stitched_image = Image.new('RGB', (total_width, total_height))
            previous = None
            part = 0

            for idx, rectangle in enumerate(rectangles):
                for item in elements:
                    xpath = item['xpath']
                    display_page = item['display_page']

                    if display_page == 'last':
                        if idx == 0:
                            self.handle_element_display(driver, xpath, 'display: none;')
                        elif idx == len(rectangles) - 1:
                            self.handle_element_display(driver, xpath, 'display: block;')
                    elif display_page == 'first' and idx != 0:
                        self.handle_element_display(driver, xpath, 'display: none;')
                    
                if not previous is None:
                    driver.execute_script("window.scrollTo({0}, {1})".format(
                        rectangle[0], rectangle[1]))
                    # time.sleep(1)
                file_name = "part_{0}.png".format(part)
                driver.get_screenshot_as_file(file_name)
                screenshot = Image.open(file_name)
                if rectangle[1] + viewport_height > total_height:
                    offset = (rectangle[0], total_height - viewport_height)
                else:
                    offset = (rectangle[0], rectangle[1])
                stitched_image.paste(screenshot, offset)
                del screenshot
                os.remove(file_name)
                part = part + 1
                previous = rectangle
            save_path = os.path.abspath(os.path.join(save_path, image_name))
            stitched_image.save(save_path)
            return save_path

    @staticmethod
    def handle_element_display(driver: WebDriver, xpath: str, attr_val: str):
        try:
            sp_xpath = xpath.split('=')
            if 'id=' in xpath.lower():
                driver.execute_script(
                    "document.getElementById('{}').setAttribute('style', '{}');"
                    .format(sp_xpath[1], attr_val))
            elif 'class=' in xpath.lower():
                driver.execute_script(
                    "document.getElementsByClassName('{}')[0].setAttribute('style', '{}');"
                    .format(sp_xpath[1], attr_val))
            elif 'tag=' in xpath.lower():
                driver.execute_script(
                    "document.getElementsByTagName('{}')[0].setAttribute('style', '{}');"
                    .format(sp_xpath[1], attr_val))
            else:
                print(
                    'For Hiding Or Displaying Element works with ID, Class and Tag Selector only'
                )
        except Exception as Error:
            print('Error : ', str(Error))
