from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import settings
from time import sleep
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


driver = webdriver.Firefox()
# options = webdriver.FirefoxOptions()

executor_url = driver.command_executor._url
session_id =  driver.session_id
print(executor_url)
# driver.get("https://www.instagram.com")

print(executor_url, session_id)

def create_driver_session(session_id, executor_url):
    print('Creating new driver session.')
    # Save the original function, so we can revert our patch
    org_command_execute = RemoteWebDriver.execute

    def new_command_execute(self, command, params=None):
        if command == "newSession":
            # Mock the response
            return {'success':0, 'value': None, 'sessionId': session_id}
        else:
            return org_command_execute(self, command, params)

    # Patch the function before creating the driver object
    RemoteWebDriver.execute = new_command_execute

    new_driver  = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
    new_driver.session_id = session_id

    # Replace the patched function with original function
    RemoteWebDriver.execute = org_command_execute
    print('Created new driver session.')
    return new_driver

def check_for_notif_popup():
    print('Inside check_for_notif_popup()')
    # alert = driver.switch_to.alert  # CHECK THIS OUT IN DOCS
    try:
            #For Turn on notifications popup
            notif_css_selector = "html.js.logged-in.client-root.js-focus-visible.sDN5V body div.RnEpo.Yx5HN div.pbNvD.fPMEg div._1XyCr div.piCib div.mt3GC button.aOOlW.HoLwm"
            wait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, notif_css_selector)))
            driver.find_element(By.CSS_SELECTOR, notif_css_selector).click()
            print('Popup closed')
    except:
        print('No button found')
        pass

def launch_insta(session_id, executor_url):
    create_driver_session(session_id, executor_url)
    driver.get("https://www.instagram.com")

    #Log in steps
    
    try:
        print('Waiting for username element to load')
        wait(driver, 5).until(EC.element_to_be_clickable((By.NAME, "username")))
        username_element = driver.find_element(By.NAME, "username")
        username_element.send_keys(settings.username)
        sleep(1)
        password_element = driver.find_element(By.NAME, "password")
        password_element.send_keys(settings.password)
        print('Logging in')
        login_element =  driver.find_element(By.CSS_SELECTOR, ".L3NKy > div:nth-child(1)")
        login_element.click()
        sleep(1)

        # Save info popup
        try:
            #For Save login info popup
            save_info_css_selector = "button.sqdOP:nth-child(1)"
            sleep(3)
            driver.find_element(By.CSS_SELECTOR, save_info_css_selector).click()
            print('Closed Save info popup')
        except:
            print('Closing Save info popup not found.')
    

    except:
        print('Checking for notifications popup, maybe already logged in. ')
        # check_for_popup()
        
    check_for_notif_popup()
    print('Fully logged in')

    open_upload_box()

def open_upload_box():
    driver.get('https://www.instagram.com/nice.maymays/')

    driver.find_element(By.CSS_SELECTOR, ".ZQScA > div:nth-child(1) > svg:nth-child(1)").click()
    driver.find_element(By.CSS_SELECTOR,"button.sqdOP").click()

if __name__ == '__main__':
    launch_insta(session_id, executor_url)