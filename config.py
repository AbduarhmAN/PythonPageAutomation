from selenium.webdriver.remote.webelement import WebElement
from typing import List


class DataManager:

    mainPage: str = ""
    post_input_field: str = (
        "//*[local-name()='div' and @class='x1i10hfl x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xmjcpbm x107yiy2 xv8uw2v x1tfwpuw x2g32xy x78zum5 x1q0g3np x1iyjqo2 x1nhvcw1 x1n2onr6 xt7dq6l x1ba4aug x1y1aw1k xn6708d xwib8y2 x1ye3gou']"
    )
    groups_open_button: str = (
        "//*[local-name()='a' and @class='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g xkrqix3 x1sur9pj x1pd3egz' and @role='link']"
    )
    see_all_groups_button: str = (
        "//*[local-name()='a' and contains(@class,'x1i10hfl x1qjc9v5 xjqpnuy xa49m3k xqeqjp1 x2hbi6w x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xdl72j9 x2lah0s xe8uvvx x2lwn1j xeuugli x16tdsg8 x1hl2dhg xggy1nq x1ja2u2z x1t137rt x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1q0g3np x87ps6o x1lku1pv x1a2a7pz x1fey0fg x1ypdohk x1k74hu9 x1ejq31n xd10rxx x1sy0etr x17r0tee x1rg5ohu xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x1n2onr6 x3ajldb')]"
    )
    groups_button : str = (
        "//*[local-name()='img' and contains(@src,'https://static.xx.fbcdn.net/rsrc.php/v4/yZ/r/MhkwI3R0SHP.png?_nc_eui2=AeERq3fS_avM27H0Ey8ZRM-jALFbgMvRWKAAsVuAy9FYoOCCTqTOMKnJYH0EjwbiiqzdGC1VLbIZ3zfNOneavfPE')]"
    )
    menu_button: str = (
        "//*[local-name()='path' and contains(@d,'M18.5 1A1.5 1.5 0 0 0 17 2.5v3A1.5 1.5 0 0 0 18.5 7h3A1.5 1.5 0 0 0 23 5.5v-3A1.5 1.5 0 0 0 21.5 1h-3zm0 8a1.5 1.5 0 0 0-1.5 1.5v3a1.5 1.5 0 0 0 1.5 1.5h3a1.5 1.5 0 0 0 1.5-1.5v-3A1.5 1.5 0 0 0 21.5 9h-3zm-16 8A1.5 1.5 0 0 0 1 18.5v3A1.5 1.5 0 0 0 2.5 23h3A1.5 1.5 0 0 0 7 21.5v-3A1.5 1.5 0 0 0 5.5 17h-3zm8 0A1.5 1.5 0 0 0 9 18.5v3a1.5 1.5 0 0 0 1.5 1.5h3a1.5 1.5 0 0 0 1.5-1.5v-3a1.5 1.5 0 0 0-1.5-1.5h-3zm8 0a1.5 1.5 0 0 0-1.5 1.5v3a1.5 1.5 0 0 0 1.5 1.5h3a1.5 1.5 0 0 0 1.5-1.5v-3a1.5 1.5 0 0 0-1.5-1.5h-3zm-16-8A1.5 1.5 0 0 0 1 10.5v3A1.5 1.5 0 0 0 2.5 15h3A1.5 1.5 0 0 0 7 13.5v-3A1.5 1.5 0 0 0 5.5 9h-3zm0-8A1.5 1.5 0 0 0 1 2.5v3A1.5 1.5 0 0 0 2.5 7h3A1.5 1.5 0 0 0 7 5.5v-3A1.5 1.5 0 0 0 5.5 1h-3zm8 0A1.5 1.5 0 0 0 9 2.5v3A1.5 1.5 0 0 0 10.5 7h3A1.5 1.5 0 0 0 15 5.5v-3A1.5 1.5 0 0 0 13.5 1h-3zm0 8A1.5 1.5 0 0 0 9 10.5v3a1.5 1.5 0 0 0 1.5 1.5h3a1.5 1.5 0 0 0 1.5-1.5v-3A1.5 1.5 0 0 0 13.5 9h-3z')]"
    )
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
        try:
            print("[DEBUG] Retrieving account pages...")
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
            print("[DEBUG] Account pages retrieved successfully.")
            return organizedElements
        except Exception as e:
            print(f"[ERROR] Error retrieving account pages: {e}")
            return []

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
