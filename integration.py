from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from pyautogui import moveTo
from pyautogui import click


class SeleniumManager:
    __wdriver: WebDriver = None

    # C:/Users/OBT/AppData/Local/Google/Chrome/User Data
    # Profile 5

    def Initialze_webdriver(self):
        try:
            print("[DEBUG] Initializing WebDriver...")
            chrome_options = Options()
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option(
                "excludeSwitches", ["enable-automation"]
            )
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument(
                "user-data-dir=C:/Users/AM/AppData/Local/Google/Chrome/User Data"
            )
            chrome_options.add_argument("profile-directory=Profile 4")
            self.__wdriver = webdriver.Chrome(options=chrome_options)
            self.__wdriver.maximize_window()
            print("[DEBUG] WebDriver initialized successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to initialize WebDriver: {e}")

    def get_webdriver(self) -> WebDriver:
        return self.__wdriver

    def navigate_to_elem(self, element, min_coordinate=10, movement_duration=1):
        try:
            print("[DEBUG] Navigating to element...")
            outer_pos = (
                self.__wdriver.get_window_position()
            )  # Example: {'x': 0, 'y': 0}

            browser_offset_y = self.__wdriver.execute_script(
                "return window.outerHeight - window.innerHeight;"
            )
            browser_offset_x = self.__wdriver.execute_script(
                "return window.outerWidth - window.innerWidth;"
            )

            rect = self.__wdriver.execute_script(
                "return arguments[0].getBoundingClientRect();", element
            )

            center_x = rect["left"] + rect["width"] / 2
            center_y = rect["top"] + rect["height"] / 2

            absolute_x = outer_pos["x"] + center_x + (browser_offset_x / 2)
            absolute_y = outer_pos["y"] + browser_offset_y + center_y

            absolute_x = max(absolute_x, min_coordinate)
            absolute_y = max(absolute_y, min_coordinate)

            moveTo(absolute_x, absolute_y, duration=movement_duration)
            print("[DEBUG] Navigation to element completed.")
        except Exception as e:
            print(f"[ERROR] Failed to navigate to element: {e}")

    def clickOnScreen(self):
        click()
