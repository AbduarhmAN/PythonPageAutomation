# Description: This file contains the PostAutomation class which is responsible for automating the process of creating a post on a social media platform.
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from config import DataManager
from pynput.keyboard import Key, Controller
from pynput import keyboard
from selenium.common.exceptions import TimeoutException


class PostAutomation:

    def __init__(self, webdriver: webdriver, dataMgr: DataManager):
        self.postText = ""
        self.postImageAndVideo = ""
        self.webdriver: WebDriverWait = WebDriverWait(webdriver, 10)
        self.dataMgr: DataManager = dataMgr
        self.isPostEnabledInGroup: bool = False
        self.isPostInput: WebElement = None
        self.textInput: WebElement = None
        self.imageAndVideoInput: WebElement = None

    def __process_page(self):
        """
        Placeholder for processing a page in a new window.
        """
        print("[DEBUG] checking if the page is ready for posting or make wait decision")
        if self.isPostEnabledInGroup:
            try:
                isWelecome = self.webdriver.until(
                    EC.invisibility_of_element((By.XPATH, self.dataMgr.welecomePopup))
                )
                
                if isWelecome == True:
                    print(f"[DEBUG] this is not new Group")
                    self.isPostInput.click()
                else:
                    print(f"[DEBUG] closing the welcome popup")
                    isWelecome.find_element(By.XPATH, self.dataMgr.closePopupButton).click()
                    self.__process_page()

            except Exception as e:
                print(f"[DEBUG] Error checking welcome popup due to exception :\n{e}")
                
        else:
            print("[DEBUG] Post form not found")

        # Future implementation goes here.

    def process_post(self):
        """
        Placeholder for processing a post in a new window.
        """
        print("[DEBUG] Processing post ...")
        print("[DEBUG] checking if the page has a post form or close the window")
        self.__process_page()
        self.setPostData(
            self.dataMgr.post_text, self.dataMgr.post_image, self.dataMgr.post_video
        )
        self.__startPosting()

    def __checkAllFieldsAvailable(self) -> bool:
        """
        Placeholder for checking if all fields are available.
        """
        print("[DEBUG] Checking all fields are available ...")
        # Future implementation goes here.
        try:
            if self.postText:
                try:
                    print("[DEBUG] Text field found")
                except Exception as e:
                    print(
                        f"[DEBUG] Error checking text field availability due to exception :\n{e}"
                    )

            if self.postImageAndVideo:
                try:
                    self.imageAndVideoInput = self.webdriver.until(
                        EC.presence_of_element_located(
                            (By.XPATH, self.dataMgr.image_and_video_input_field)
                        )
                    )
                    print("[DEBUG] Image field found")
                except Exception as e:
                    print(
                        f"[DEBUG] Error checking image field availability due to exception :\n{e}"
                    )

            if self.postText or self.imageAndVideoInput:
                return True
            else:
                return False
        except Exception as e:
            print(f"[DEBUG] Error checking fields availability due to exception :\n{e}")
        return False

    def __startPosting(self):
        """
        Placeholder for starting the posting process.
        """
        if self.__checkAllFieldsAvailable():
            sleep(2)
            Controller().type(self.postText)
            self.imageAndVideoInput.click()
            sleep(2)
            print("[DEBUG] Image and video button clicking ...")
            try:
                self.imageAndVideoButton = self.webdriver.until(
                    EC.presence_of_element_located(
                        (By.XPATH, self.dataMgr.image_and_video_button)
                    )
                )
                print("[DEBUG] Image and video button found")
                self.imageAndVideoButton.click()
                sleep(2)
                Controller().type(self.postImageAndVideo)
                Controller().press(Key.enter)
                Controller().release(Key.enter)
                sleep(2)

                try:
                    # Wait until the "Post" button is clickable, then click it.
                    post_button = self.webdriver.until(
                        EC.element_to_be_clickable((By.XPATH, self.dataMgr.post_button))
                    )
                    print(
                        "[DEBUG] 'Post' button pressed; it is now expected to be disabled."
                    )
                    post_button.click()
                    sleep(2)
                    # Continuously monitor the button's state.
                    while True:
                        try:
                            try:
                                # If the button does not become clickable within 2 seconds, check if it has vanished.
                                invisible = self.webdriver.until(
                                    EC.invisibility_of_element(
                                        (By.XPATH, self.dataMgr.loading_post)
                                    )
                                )
                                if invisible:
                                    print(
                                        "[DEBUG] 'Post' button has disappeared. Process completed successfully."
                                    )
                                    break
                            except TimeoutException:
                               print("still loading ...")
                               continue
                        except TimeoutException:
                            try:
                                # If the button does not become clickable within 2 seconds, check if it has vanished.
                                invisible = self.webdriver.until(
                                    EC.invisibility_of_element_located(
                                        (By.XPATH, self.dataMgr.post_button)
                                    )
                                )
                                if invisible:
                                    print(
                                        "[DEBUG] 'Post' button has disappeared. Process completed successfully."
                                    )
                                    break
                            except TimeoutException:
                                # If the button is still visible but not clickable, wait a bit longer and recheck.
                                print(
                                    "[DEBUG] 'Post' button remains disabled and visible. Waiting and rechecking..."
                                )
                                sleep(2)
                except Exception as e:
                    print(
                        f"[DEBUG] Error encountered while handling the 'Post' button: {e}"
                    )

            except Exception as e:
                print(
                    f"[DEBUG] Error clicking image and video button due to exception :\n{e}"
                )

        print("[DEBUG] Starting posting ...")

    def setPostData(self, postText: str = "", postImage: str = "", postVideo: str = ""):
        """
        Placeholder for setting post data.
        """
        print("[DEBUG] Setting post data ...")
        self.postText = postText
        self.postImageAndVideo = postImage

        # Future implementation goes here.

    def verify_post(self) -> bool:
        """
        Placeholder for verifying a post in a new window.
        """
        print("[DEBUG] Verifying post in new window...")
        # Future implementation goes here.
        try:
            self.isPostInput = self.webdriver.until(
                EC.element_to_be_clickable((By.XPATH, self.dataMgr.post_input_field))
            )
            if self.isPostInput is not None:
                print("[DEBUG] Post input field found")
                self.isPostEnabledInGroup = True
                return self.isPostEnabledInGroup
            else:
                print("[DEBUG] Post input field not found")
                self.isPostEnabledInGroup = False
                return self.isPostEnabledInGroup
        except Exception as e:
            print(f"[DEBUG] Post input field not found due to exception :\n{e}")
            self.isPostEnabledInGroup = False
            return self.isPostEnabledInGroup
