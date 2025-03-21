from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.webdriver import WebDriver


class ConfigManager :
    __currentAccount : str = ""
    __PagesOnAccount : list[WebElement] = [] 
    __wdriver : WebDriver = None

    def __init__(self):
        pass


    def getAccountPages(self,cAccount: str = __currentAccount, unorgnizedElements : list[WebElement] = __PagesOnAccount) -> list[WebElement]:
        orgnizedElements : list[WebElement] = []
        
        for element in unorgnizedElements:
            



class DataManager:
    
    account_name : str ="//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']" 
    account_icon : str = "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']"
    all_profiles_button : str = "//*[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f x1dem4cn')]//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft']"
    pages_containter : set = "//*/*[@role='list']//span[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')]"
    account_pages : list[str] = []
