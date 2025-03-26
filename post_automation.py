# Description: This file contains the PostAutomation class which is responsible for automating the process of creating a post on a social media platform.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from config import DataManager

class PostAutomation:

    def __init__(self, webdriver: webdriver, dataMgr: DataManager):
        self.postText = ""
        self.postImage = ""
        self.postVideo = ""
        self.webdriver : WebDriverWait = WebDriverWait(webdriver, 20)
        self.dataMgr : DataManager = dataMgr
        self.isPostEnabledInGroup : bool = False
        self.isPostInput : WebElement = None
        
    def __process_page(self):
        """
        Placeholder for processing a page in a new window.
        """
        print("[DEBUG] checking if the page is ready for posting or make wait decision")
        if self.isPostEnabledInGroup:
            self.isPostInput.click()            
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
        
        # Future implementation goes here.

    def verify_post(self)-> bool:
        """
        Placeholder for verifying a post in a new window.
        """
        print("[DEBUG] Verifying post in new window...")
        # Future implementation goes here.
        try:
            self.isPostInput = self.webdriver.until(EC.element_to_be_clickable((By.XPATH, self.dataMgr.post_input_field)))
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