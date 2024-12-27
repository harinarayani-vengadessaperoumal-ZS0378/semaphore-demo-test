from libraries.locators import NavBarLocators

class   NavBar:
    """This class holds all the methods that we can do at NavBar of a Page"""
    def __init__(self, base_page):
        # base_page is an instance of BasePage, passed during initialization
        self.base_page = base_page

    def get_menus(self):
        """Retrieve all the menu items in the navigation bar"""
        menus_elem = self.base_page.wait_for_and_get_elements(NavBarLocators.XPATH_NAV_BAR_MENU)
        menus = [elem.text for elem in menus_elem]
        return menus
    
    def click_option_in_menu(self,option):
        """Clicks the provided option in the menu of navigation bar"""
        if option == "My Info":
            option = "MyDetails"
        self.base_page.click_element(NavBarLocators.XPATH_VARIABLE_NAV_BAR_MENU.replace("{VARIABLE}",option))
