"""
Browser Environment for bAUTO
==============================

Provides a clean interface to Selenium WebDriver.
"""

import os
import time
import logging
from typing import Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)


class BrowserEnvironment:
    """
    Browser automation environment.
    Provides simplified access to Selenium WebDriver.
    """
    
    def __init__(self, driver: webdriver.Chrome, implicit_wait: float = 10.0):
        self.driver = driver
        self.implicit_wait = implicit_wait
        self.driver.implicitly_wait(implicit_wait)
        
    # ==================== Navigation ====================
    
    def navigate(self, url: str):
        """Navigate to URL."""
        logger.info(f"Navigating to: {url}")
        self.driver.get(url)
    
    def wait(self, seconds: float):
        """Wait for specified seconds."""
        logger.debug(f"Waiting {seconds} seconds")
        time.sleep(seconds)
    
    def refresh(self):
        """Refresh current page."""
        logger.info("Refreshing page")
        self.driver.refresh()
    
    # ==================== Element Finding ====================
    
    def find_element(self, by: str = 'xpath', value: Optional[str] = None) -> WebElement:
        """
        Find element.
        
        Args:
            by: Search method ('xpath', 'css', 'id', 'name', 'class', 'tag')
            value: Search value
        """
        by_map = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME
        }
        
        by_type = by_map.get(by.lower(), By.XPATH)
        return self.driver.find_element(by_type, value)
    
    def find_elements(self, by: str = 'xpath', value: Optional[str] = None) -> List[WebElement]:
        """Find multiple elements."""
        by_map = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME
        }
        
        by_type = by_map.get(by.lower(), By.XPATH)
        return self.driver.find_elements(by_type, value)
    
    def find_visible_element(self, by: str = 'xpath', value: Optional[str] = None) -> Optional[WebElement]:
        """Find first visible element."""
        elements = self.find_elements(by, value)
        for elem in elements:
            if self.is_visible(elem):
                return elem
        return None
    
    def find_element_by_text(self, text: str, tag: str = '*') -> Optional[WebElement]:
        """Find element containing text."""
        xpath = f"//{tag}[contains(normalize-space(), '{text}')]"
        try:
            return self.find_element('xpath', xpath)
        except:
            return None
    
    # ==================== Element Interaction ====================
    
    def click(self, element: WebElement):
        """Click element."""
        try:
            element.click()
        except Exception as e:
            # Try JavaScript click as fallback
            logger.warning(f"Regular click failed, trying JS click: {e}")
            self.driver.execute_script("arguments[0].click();", element)
    
    def type_text(self, element: WebElement, text: str):
        """Type text into element."""
        element.send_keys(text)
    
    def clear_and_type(self, element: WebElement, text: str):
        """Clear element then type text."""
        element.clear()
        element.send_keys(text)
    
    def select_option(self, element: WebElement, value: str):
        """Select option from dropdown."""
        select = Select(element)
        try:
            select.select_by_value(value)
        except:
            select.select_by_visible_text(value)
    
    def check_checkbox(self, element: WebElement, checked: bool = True):
        """Check or uncheck checkbox."""
        is_checked = element.is_selected()
        if is_checked != checked:
            self.click(element)
    
    def submit(self, element: WebElement):
        """Submit form."""
        element.submit()
    
    # ==================== Page Interaction ====================
    
    def scroll(self, direction: str):
        """
        Scroll page.
        
        Args:
            direction: 'up', 'down', 'top', 'bottom', or pixel amount (e.g., '500')
        """
        direction = direction.lower()
        
        if direction == 'top':
            self.driver.execute_script("window.scrollTo(0, 0);")
        elif direction == 'bottom':
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        elif direction == 'up':
            self.driver.execute_script("window.scrollBy(0, -500);")
        elif direction == 'down':
            self.driver.execute_script("window.scrollBy(0, 500);")
        else:
            # Treat as pixel amount
            try:
                pixels = int(direction)
                self.driver.execute_script(f"window.scrollBy(0, {pixels});")
            except:
                logger.warning(f"Invalid scroll direction: {direction}")
    
    def screenshot(self, filename: str):
        """Take screenshot."""
        os.makedirs(os.path.dirname(filename) or ".", exist_ok=True)
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
    
    def get_page_text(self) -> str:
        """Get all visible text from page."""
        return self.driver.find_element(By.TAG_NAME, "body").text
    
    def execute_script(self, script: str, *args):
        """Execute JavaScript."""
        return self.driver.execute_script(script, *args)
    
    # ==================== Element Properties ====================
    
    def get_text(self, element: WebElement) -> str:
        """Get element text."""
        return element.text
    
    def get_attribute(self, element: WebElement, attr: str) -> str:
        """Get element attribute."""
        return element.get_attribute(attr)
    
    def is_visible(self, element: WebElement) -> bool:
        """Check if element is visible."""
        return element.is_displayed()
    
    def is_enabled(self, element: WebElement) -> bool:
        """Check if element is enabled."""
        return element.is_enabled()
    
    def is_selected(self, element: WebElement) -> bool:
        """Check if element is selected (checkbox/radio)."""
        return element.is_selected()
    
    # ==================== Advanced ====================
    
    def wait_for_element(self, by: str = 'xpath', value: str = None, 
                         timeout: float = 10.0) -> WebElement:
        """Wait for element to be present."""
        by_map = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME
        }
        
        by_type = by_map.get(by.lower(), By.XPATH)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by_type, value)))
    
    def wait_for_clickable(self, by: str = 'xpath', value: str = None,
                          timeout: float = 10.0) -> WebElement:
        """Wait for element to be clickable."""
        by_map = {
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'id': By.ID,
            'name': By.NAME,
            'class': By.CLASS_NAME,
            'tag': By.TAG_NAME
        }
        
        by_type = by_map.get(by.lower(), By.XPATH)
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by_type, value)))
    
    def switch_to_frame(self, frame: int | str | WebElement):
        """Switch to iframe."""
        self.driver.switch_to.frame(frame)
    
    def switch_to_default(self):
        """Switch back to main content."""
        self.driver.switch_to.default_content()
    
    def get_current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url
    
    def get_title(self) -> str:
        """Get page title."""
        return self.driver.title


def create_browser(config) -> tuple[webdriver.Chrome, BrowserEnvironment]:
    """
    Create browser instance with configuration.
    
    Returns:
        Tuple of (WebDriver, BrowserEnvironment)
    """
    logger.info("Creating browser instance")
    
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    
    # Apply configuration
    options_dict = config.browser.get_chrome_options()
    for key, value in options_dict.items():
        if value is None:
            chrome_options.add_argument(key)
        else:
            chrome_options.add_argument(f"{key}={value}")
    
    # Force new window instead of new tab
    chrome_options.add_argument("--new-window")
    
    # Anti-detection settings
    if config.browser.disable_automation_flags:
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Create driver
    try:
        if config.browser.auto_download_driver:
            service = Service(ChromeDriverManager().install())
        else:
            service = Service()
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Additional anti-detection
        if config.browser.stealth_mode:
            driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )
        
        # Set timeouts
        driver.set_page_load_timeout(config.automation.page_load_timeout)
        
        # Create environment
        env = BrowserEnvironment(driver, config.automation.implicit_wait)
        
        logger.info("Browser created successfully")
        return driver, env
        
    except Exception as e:
        logger.error(f"Failed to create browser: {e}")
        raise

