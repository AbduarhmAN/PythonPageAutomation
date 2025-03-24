from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep

class GroupRetrieval:
    def __init__(self, webdriver, button_xpath: str, scroll_pause_time: int = 2):
        self.webdriver = webdriver
        self.button_xpath = button_xpath
        self.scroll_pause_time = scroll_pause_time

    def __scroll_to_bottom(self) -> None:
        try:
            print("[DEBUG] Scrolling to the bottom of the page...")
            last_height = self.webdriver.execute_script("return document.body.scrollHeight")
            while True:
                self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(self.scroll_pause_time)
                new_height = self.webdriver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            print("[DEBUG] Scrolling completed.")
        except Exception as e:
            print(f"[ERROR] Failed to scroll to bottom: {e}")

    def __get_buttons(self):
        self.__scroll_to_bottom()
        buttons = self.webdriver.find_elements(By.XPATH, self.button_xpath)
        print(f"[DEBUG] Found {len(buttons)} buttons before filtering")
        if buttons:
            buttons = buttons[2:]
        print(f"[DEBUG] {len(buttons)} buttons after filtering")
        return buttons

    def process_buttons(self):
        print("[DEBUG] Entering process_buttons()")
        buttons = self.__get_buttons()
        original_window = self.webdriver.current_window_handle
        actions = ActionChains(self.webdriver)
        
        for index, button in enumerate(buttons):
            try:
                print(f"[DEBUG] Processing button {index+1} out of {len(buttons)}")
                # Open in a new window/tab via CONTROL+click.
                actions.key_down(Keys.CONTROL).click(button).key_up(Keys.CONTROL).perform()
                sleep(2)  # Allow time for the new window/tab to open

                new_windows = [handle for handle in self.webdriver.window_handles if handle != original_window]
                if not new_windows:
                    print("[DEBUG] No new window detected, skipping button")
                    continue
                    
                print(f"[DEBUG] New windows detected: {new_windows}")
                new_window = new_windows[-1]  # Assume the last in the list is the new one
                yield new_window
                sleep(1)
                print(f"[DEBUG] Successfully processed button {index+1}")
            except Exception as e:
                print(f"[ERROR] Processing button error: {e}")
                self.webdriver.switch_to.window(original_window)