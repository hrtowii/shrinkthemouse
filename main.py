from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
usleep = lambda x: time.sleep(x/1000000.0)

firefox_options = Options()
firefox_options.set_preference("general.useragent.override", 
                               "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
# firefox_options.add_argument("--headless")
firefox_options.add_argument("--width=375")
firefox_options.add_argument("--height=812")
driver = webdriver.Firefox(options=firefox_options)

console_logger = """
window.logs = [];
const originalLog = console.log;
console.log = function() {
    window.logs.push(Array.from(arguments).join(' '));
    originalLog.apply(console, arguments);
};
"""
driver.execute_script(console_logger)
driver.get('https://huntthemouse.sqkii.com')

def get_console_logs():
    logs = driver.execute_script("return window.logs || []")
    if logs:
        for log in logs:
            print(f"Console log: {log}")
        driver.execute_script("window.logs = []")
    return logs

def init_print_click():
    script = '''
    document.addEventListener('click', function(e) {
        console.log(`Clicked at: X: ${e.clientX}, Y: ${e.clientY}`);
    });
    '''
    driver.execute_script(script)
    print("Click listener initialized")

def click_i_agree():
    third_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), \"I agree\")]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", third_button)
    third_button.click()
    print("'I agree' clicked successfully!")

def click_letsgo():
    second_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), \"Let's go!\")]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", second_button)
    second_button.click()
    print("'Let's go!' clicked successfully!")

def click_skip():
    first_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".q-btn.q-btn-item .custom-btn img[alt='skip']"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
    first_button.click()
    print("Skip button clicked successfully!")

def click_map(x, y):
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
    print("asdkjakjsdhaksjd")

def click_shrink_circle():
    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'title') and text()='Shrink circle']/ancestor::button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", button)
    # driver.execute_script("arguments[0].click();", button)
    button.click()
    print("Successfully clicked 'Shrink circle' button")

def click_yes():
    # Wait for the overlay/modal to appear and the Yes button to be clickable
    yes_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[text()='Yes']/ancestor::button[contains(@class, 'o-custom-btn')]"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", yes_button)
    driver.execute_script("arguments[0].click();", yes_button)
    yes_button.click()
    print("Successfully clicked 'Yes' button")

try:
    init_print_click()
    click_skip()
    click_letsgo()
    time.sleep(1)
    click_i_agree()
    for _ in range(2):
        click_map(290, 323)
        time.sleep(1.25)
    try:
        click_i_agree()
    except Exception as e:
        print(f"First attempt to click agree failed: {e}")
        time.sleep(2)  # Wait longer and try again
        click_i_agree()

    click_shrink_circle()
    click_yes()
    # click_yes()

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    get_console_logs()
    # driver.quit()