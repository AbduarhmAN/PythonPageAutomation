from selenium.webdriver.remote.webelement import WebElement
from typing import List


class DataManager:

    mainPage: str = ""
    account_name: str = (
        "//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6']"
    )
    create_page_button: str = (
        "//*[contains(@class,'x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli xz9dl7a xsag5q8 x4uap5 xkhd6sd x1n2onr6 x1ja2u2z')]//div[contains(@class,'x78zum5 xdt5ytf xz62fqu x16ldp7u')]//div[contains(@class,'xu06os2 x1ok221b')]//span[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h')]"
    )
    account_icon: str = "//*[local-name()='g' and @mask='url(#«R1ldm6l6ismipapd5aq»)']"
    all_profiles_button: str = (
        "//*[contains(@class,'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen x1s688f x1dem4cn')]//*[local-name()='span' and @class='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft']"
    )
    pages_containter: str = (
        "//div[contains(@class,'x78zum5 xdt5ytf')]//div[contains(@class,'xwxc41k x1y1aw1k')]/div[@class='html-div x11i5rnm x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1oo3vh0 x1rdy4ex' and @role='list']"
    )
    pages_filter: str = (
        "//div[@role='listitem']//*[contains(@class,'x1qjc9v5 x1q0q8m5 x1qhh985 xu3j5b3 xcfux6l x26u7qi xm0m39n x13fuv20 x972fbf x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1qughib xat24cr x11i5rnm x1mh8g0r xdj266r x2lwn1j xeuugli xz9dl7a xsag5q8 x4uap5 xkhd6sd x1n2onr6 x1ja2u2z')]//div[@class='x78zum5 xdt5ytf xz62fqu x16ldp7u']/div[@class='xu06os2 x1ok221b']/span[@class='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xk50ysn xzsf02u x1yc453h']"
    )

    account_pages: list[str] = []


class ConfigManager:
    def __init__(self, main_page: str = "", current_account: str = "", pages_on_account: WebElement = None):
        """
        Initializes ConfigManager with values passed from outside.
        :param main_page: The main page name (e.g. "Abdurahman Maghrbi")
        :param current_account: The current account being processed.
        :param pages_on_account: The unorganized WebElement container holding all pages.
        """
        self.currentAccount: str = current_account  # Assigned via external parameter
        self.PagesOnAccount: WebElement = pages_on_account  # Assigned via external parameter
        self.mainPage: str = main_page  # Provided externally

        # Initialize DataManager and update its mainPage if provided externally
        self.dataMgr: DataManager = DataManager()
        if main_page:
            self.dataMgr.mainPage = main_page

    def getAccountPages(
        self, 
        cAccount: str = "", 
        unorgnizedElements: WebElement = None
    ) -> List[WebElement]:
        """
        Processes an unorganized element container to retrieve account pages.
        The filtering changes based on whether the account is the main account.
        
        :param cAccount: Optionally provided account name (if empty, uses currentAccount)
        :param unorgnizedElements: Optionally provided container element (if empty, uses PagesOnAccount)
        :return: A list of filtered WebElement pages.
        """
        if not cAccount:
            cAccount = self.currentAccount
        if unorgnizedElements is None:
            unorgnizedElements = self.PagesOnAccount

        try:
            pages = unorgnizedElements.find_elements(
                by="xpath", value=self.dataMgr.pages_filter
            )
        except Exception as e:
            print(f"Error retrieving pages: {e}")
            return []

        # Use a single helper function with skip_last flag for main account
        skip_last = (cAccount == self.dataMgr.mainPage)
        organizedElements = self._filter_pages(pages, cAccount, skip_last)
        
        print(f"Pages on the account are: {[page.text for page in organizedElements]}")
        return organizedElements

    def _filter_pages(self, pages: List[WebElement], cAccount: str, skip_last: bool) -> List[WebElement]:
        """
        Filters a list of page elements based on common rules.
        
        :param pages: List of WebElement pages.
        :param cAccount: The account name for filtering.
        :param skip_last: If True, stops before processing the last page.
        :return: Filtered list of page WebElements.
        """
        filtered_pages = []
        for i, page in enumerate(pages):
            try:
                page_text = page.text.strip()
                if not page_text or page_text == cAccount:
                    continue
                # If skip_last is True and this is the last element, then break out.
                if skip_last and i == len(pages) - 1:
                    break
                filtered_pages.append(page)
            except Exception as e:
                print(f"Error processing page: {e}")
        return filtered_pages
