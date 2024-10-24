from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import threading
import queue

class BrowserAutomation(threading.Thread):
    def __init__(self, thread_id, screenshot_queue):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.screenshot_queue = screenshot_queue
        self.counter = 0
        
    def setup_driver(self):
        firefox_options = Options()
        firefox_options.set_preference("general.useragent.override", 
                                   "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
        firefox_options.add_argument("--headless")
        firefox_options.add_argument("--width=375")
        firefox_options.add_argument("--height=812")
        return webdriver.Firefox(options=firefox_options)

    def init_print_click(self, driver):
        script = '''
        document.addEventListener('click', function(e) {
            console.log(`Clicked at: X: ${e.clientX}, Y: ${e.clientY}`);
        });
        '''
        driver.execute_script(script)
        print(f"Thread {self.thread_id}: Click listener initialized")

    def click_i_agree(self, driver):
        third_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), \"I agree\")]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", third_button)
        third_button.click()
        print(f"Thread {self.thread_id}: 'I agree' clicked successfully!")

    def click_letsgo(self, driver):
        second_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(text(), \"Let's go!\")]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
        second_button.click()
        print(f"Thread {self.thread_id}: 'Let's go!' clicked successfully!")

    def click_skip(self, driver):
        first_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".q-btn.q-btn-item .custom-btn img[alt='skip']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
        first_button.click()
        print(f"Thread {self.thread_id}: Skip button clicked successfully!")

    def click_map(self, driver, x, y):
        script = f'''
        let evt = new MouseEvent('click', {{
            view: window,
            bubbles: true,
            cancelable: true,
            clientX: {x},
            clientY: {y}
        }});
        document.elementFromPoint({x}, {y}).dispatchEvent(evt);
        '''
        driver.execute_script(script)
        print(f"Thread {self.thread_id}: Map clicked at {x}, {y}")

    def click_shrink_circle(self, driver):
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'title') and text()='Shrink circle']/ancestor::button"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        print(f"Thread {self.thread_id}: Successfully clicked 'Shrink circle' button")

    def click_yes(self, driver):
        yes_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Yes']/ancestor::button[contains(@class, 'o-custom-btn')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", yes_button)
        driver.execute_script("arguments[0].click();", yes_button)
        yes_button.click()
        print(f"Thread {self.thread_id}: Successfully clicked 'Yes' button")

    def run(self):
        while True:
            self.counter += 1
            driver = None
            try:
                driver = self.setup_driver()
                driver.get('https://huntthemouse.sqkii.com')
                self.init_print_click(driver)
                self.click_skip(driver)
                self.click_letsgo(driver)
                time.sleep(1)
                self.click_i_agree(driver)
                
                for _ in range(2):
                    self.click_map(driver, 290, 323)
                    time.sleep(1.25)
                    
                try:
                    self.click_i_agree(driver)
                except Exception as e:
                    print(f"Thread {self.thread_id}: First attempt to click agree failed: {e}")
                    time.sleep(2)
                    self.click_i_agree(driver)

                self.click_shrink_circle(driver)
                self.click_yes(driver)

            except Exception as e:
                print(f"Thread {self.thread_id}: Error occurred: {e}")

            finally:
                if driver:
                    time.sleep(3)
                    screenshot_path = f"thread_{self.thread_id}_screenshot_{self.counter}.png"
                    driver.save_screenshot(screenshot_path)
                    self.screenshot_queue.put(screenshot_path)
                    driver.quit()

def main():
    screenshot_queue = queue.Queue()
    threads = []
    for i in range(5):
        thread = BrowserAutomation(i, screenshot_queue)
        thread.daemon = True
        threads.append(thread)
        thread.start()
        time.sleep(2)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")

if __name__ == "__main__":
    main()