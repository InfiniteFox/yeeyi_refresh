import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import logging
from apscheduler.schedulers.background import BlockingScheduler
from datetime import datetime

#Set log
logging.basicConfig(filename='logger.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


# Account info
account = 'account'
password = 'password'

# Page to refresh
page = 'page'

def refresh():
    # chrome start option
    chrome_options = webdriver.ChromeOptions()

    # set chrome start option headless and disable gpu
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')

    # Set chrome as webdriver
    driver = webdriver.Chrome(options=chrome_options)
    #driver.maximize_window()


    # Login Page
    driver.get('http://www.yeeyi.com/forum/index.php?app=member&act=login')

    # Login
    driver.find_element_by_xpath('//*[@id="telTxtLogin"]').send_keys(account) # Enter account
    driver.find_element_by_xpath('//*[@id="passShow"]').send_keys(password,Keys.ENTER) # Enter password & Press Enter
    time.sleep(3) # Wait for cookie
    # Alert click
    alert=driver.switch_to.alert
    alert.accept()  # Accept
    
    print('Login Success')
    logging.info('Login Success')

    #cookies = driver.get_cookies()
    #print(cookies)

    # Open the page
    js = f"window.open('{page}')"
    driver.execute_script(js)

    # Switch to the new page
    windows = driver.window_handles
    driver.switch_to.window(windows[-1])

    time.sleep(5)

    #Refresh
    refresh = driver.find_element_by_id("k_refresh")
    #print(refresh.get_attribute("href"))
    refresh.click()
    logging.info('ReFresh Success')
    print('ReFresh Success')

    time.sleep(5)

    driver.quit()
    logging.info('Driver Quit Success')
    print('Quit')

# Background schedulers
scheduler = BlockingScheduler()
scheduler._logger = logging
# Add job like crontab
scheduler.add_job(refresh, 'cron', hour='8-15', minute='46')
scheduler.add_job(refresh, 'cron', hour='18-23', minute='37')
scheduler.start()
