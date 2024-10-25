from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# from urllib.parse import quote

sys_path = r'C:/Users/abc/Desktop/Django/Messenger/'

# Config
login_time = 30                         # Time for login (in seconds)
new_msg_time = 5                        # Time for new message (in seconds)
send_msg_time = 5                       # Time for sending a message (in seconds)
country_code = 91                       # Set your country code
action_time = 2                         # Set time for button click action                         
image_path = sys_path + "test2.jpeg"      # Set your absolute image path

# Create driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Encode message text
with open(sys_path + "message.txt", 'r') as file:
    msg = file.read()    

# Open browser with default link
link = "https://web.whatsapp.com"
driver.get(link)
time.sleep(login_time)

# Loop through numbers list
with open(sys_path + 'numbers.txt', 'r') as file:
    for n in file.readlines():
        num = n.rstrip()
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
        driver.get(link)
        time.sleep(new_msg_time)
        # Click on button to load the input DOM
        attach_button = driver.find_element(By.CSS_SELECTOR, '._1OT67')
        attach_button.click()
        time.sleep(action_time)
        msg_input = driver.find_element(By.CSS_SELECTOR, '._1CGek input')
        msg_input.send_keys(image_path)
        time.sleep(action_time)
        actions = ActionChains(driver)
        for line in msg.split('\n'):
            actions.send_keys(line)
            actions.key_down(Keys.SHIFT).send_keys(Keys.ENTER).key_up(Keys.SHIFT) 
        actions.send_keys(Keys.ENTER)
        actions.perform()
        time.sleep(send_msg_time)

# Quit the driver
driver.quit()
