from urllib.parse import urlparse
from contextlib import contextmanager
from PageObjectLibrary import PageObject
from selenium.webdriver.common.by import By
from libraries.locators import CommonLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from PageObjectLibrary.keywords import PageObjectLibraryKeywords
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.expected_conditions import staleness_of

class   BasePage(PageObject):
    """Base Page - this class holds all the reusable methods that can be used at the child Pages"""
    PAGE_LOCATOR = None

    def __init__(self):
        # Initialize the parent class (PageObject) to ensure it is properly set up
        super().__init__()
        self.page_keywords = PageObjectLibraryKeywords()

    def load_page(self, page_name, page_root=None):
        """
        Go to the url for the given page object -  this is the alternate method for go_to_page of PageObjectLibrary
        Implemented this since we have one open issue with PageobjectLibrary - https://github.com/boakley/robotframework-pageobjectlibrary/pull/29
        Additionally, we can one more checkpoint PAGE_LOCATOR to ensure correct page is loaded
        """

        # Retrieve the page object
        page = self.page_keywords._get_page_object(page_name)

        # Get the base URL (up to /web/index.php) from page_root or current page location
        base_url = page_root if page_root else page.selib.get_location()
        parsed_url = urlparse(base_url)
        # Orange HRM has additonal part of URL, that been configured here. If not needed this can be removed for other websites
        base_url_up_to_index = f"{parsed_url.scheme}://{parsed_url.netloc}/web/index.php"

        # Construct the full target URL by joining the base URL with the page-specific path
        target_url = f"{base_url_up_to_index}{page.PAGE_URL}"

        # Check if the current browser URL matches the target URL
        current_url = page.selib.get_location()
        if current_url == target_url:
            self.logger.info("Already on the correct page; no navigation needed.")
        else:
            # Navigate to the specified page and wait for it to load if the URL is different
            with self._wait_for_page_navigate_refresh():
                page.selib.go_to(target_url)

        # If PAGE_LOCATOR is defined, verify the locator exists on the page
        if hasattr(page, 'PAGE_LOCATOR') and page.PAGE_LOCATOR:
            self.wait_element_iterable(page.PAGE_LOCATOR)

            # Confirm that we're on the correct page by checking the PAGE_LOCATOR
            if not self.is_element_visible(page.PAGE_LOCATOR):
                raise Exception(f"Expected element with locator {page.PAGE_LOCATOR} not found on the {page_name}.")
            
        # Confirm we're on the expected page using page title as well
        self.page_keywords.the_current_page_should_be(page_name)

    def _is_current_page(self):
        """Check PAGE_TITLE, PAGE_URL, and PAGE_LOCATOR"""
        actual_title = self.selib.get_title()
        expected_title = self.PAGE_TITLE

        actual_url = self.selib.get_location()
        expected_url = self.PAGE_URL

        title_check = expected_title == actual_title
        url_check = expected_url in actual_url

        # Verify if PAGE_LOCATOR is defined and present on the page
        locator_check = True  # Default to True if no locator
        if hasattr(self, 'PAGE_LOCATOR') and self.PAGE_LOCATOR:
            locator_check = self.is_element_present(self.PAGE_LOCATOR)

        return title_check and url_check and locator_check

    def wait_element_iterable(self, element_to_interact):
        """Wait for the element to be present in the DOM and visible"""
        self.selib.wait_until_page_contains_element(element_to_interact,timeout=30)
        self.selib.wait_until_element_is_visible(element_to_interact)

    def click_element(self, element_locator):
        """Method to click on an element"""
        try:
            self.wait_element_iterable(element_locator)
            self.selib.click_element(element_locator)
        except Exception as e:
            raise e
        
    def is_element_present(self, element_locator):
        """Check if an element is present in the DOM."""
        try:
            self.selib.find_element(element_locator)
            return True
        except NoSuchElementException:
            return False

    def is_element_visible(self, element_locator):
        """Check if an element is visible on the page."""
        try:
            element = self.selib.find_element(element_locator)
            return element.is_displayed()
        except (NoSuchElementException, ElementNotVisibleException):
            return False
     
    def enter_text(self, element_locator, text):
        """Method to enter text into an input field"""
        try:
            self.selib.wait_until_element_is_visible(element_locator)
            self.selib.press_keys(element_locator,"CTRL+a","BACKSPACE")
            self.scroll_to_element(element_locator)
            self.selib.input_text(element_locator, text)
            self.selib.capture_page_screenshot()
        except Exception as e:
            raise e

    def select_from_list_by_index(self, element_to_interact, index):
        """Select an option from list by its index"""
        self.selib.select_from_list_by_index(element_to_interact, index)

    def select_from_list_by_value(self, element_to_interact, value):
        """Select an option from list by its value"""
        self.selib.select_from_list_by_value(element_to_interact, value)

    def get_value(self, element_to_interact):
        """Get the the value displayed at a field"""
        return self.selib.get_text(element_to_interact)
    
    def scroll_to_element(self, element_locator):
        """Scroll the page to bring the element into view."""
        element = self.selib.find_element(element_locator)
        self.browser.execute_script("arguments[0].scrollIntoView();", element)

    def hover_over_element(self, element_locator):
        """Hover over an element to reveal additional UI elements or tooltips."""
        element = self.selib.find_element(element_locator)
        ActionChains(self.browser).move_to_element(element).perform()

    def get_element_attribute(self, element_locator, attribute_name):
        """Get the specified attribute of an element."""
        return self.selib.get_element_attribute(element_locator, attribute_name)

    def clear_text_field(self, element_locator):
        """Clear the text from a text field before entering new data."""
        self.selib.clear_element_text(element_locator)

    def press_key(self, element_locator, key):
        """Simulate pressing a key on a specified element."""
        self.wait_element_iterable(element_locator)
        element = self.selib.find_element(element_locator)
        element.send_keys(key)

    def verify_element_contains_text(self, element_locator, expected_text):
        """Verify that the element contains the expected text."""
        actual_text = self.get_value(element_locator)
        if expected_text not in actual_text:
            raise AssertionError(f"Expected text '{expected_text}' not found in element text '{actual_text}'.")

    def is_checkbox_selected(self, element_locator):
        """Check if a checkbox is selected."""
        self.wait_element_iterable(element_locator)
        return self.selib.is_checkbox_selected(element_locator)

    def switch_to_iframe(self, iframe_locator):
        """Switch to an iframe by locator."""
        self.wait_element_iterable(iframe_locator)
        self.selib.select_frame(iframe_locator)

    def switch_to_default_content(self):
        """Switch back to the main content from an iframe."""
        self.selib.unselect_frame()

    def wait_for_and_get_elements(self,element_locator):
        """Returns list of available elements in the DOM"""
        self.wait_element_iterable(element_locator)
        return self.selib.find_elements(element_locator)

    def capture_toast_message(self,element_locator):
        """Captures the details present in the toast message and returns them"""
        self.wait_element_iterable(element_locator)
        toast = self.selib.find_element(element_locator)
        title = toast.find_element("xpath",CommonLocators.XPATH_TXT_TOAST_TITLE).text
        message = toast.find_element("xpath",CommonLocators.XPATH_TXT_TOAST_MESSAGE).text

        return title,message

    @contextmanager
    def _wait_for_page_navigate_refresh(self, timeout=10):
        """Context manager that waits for a page transition.
        Use this method only when a page is navigated from one to another

        This keyword works by waiting for two things to happen:

        1) the <html> tag to go stale and get replaced, and
        2) the javascript document.readyState variable to be set
           to "complete"
        """
        old_page = self.browser.find_element(By.TAG_NAME, 'html')

        yield
        WebDriverWait(self.browser, timeout).until(
            staleness_of(old_page),
            message="Old page did not go stale within %ss" % timeout
        )
        self.selib.wait_for_condition("return (document.readyState == 'complete')", timeout=10)
