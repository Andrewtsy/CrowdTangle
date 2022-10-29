"""Author - Andrew Tao
This simple script opens up the Selenium WebDriver and enters Google.com
It's used to enable setup of the images folder
Please refer to the 'images_setup_instructions.docx' for instructions.
"""

# imports classes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Adds crowdtangle extension into driver
# Assumes environment is setup with crowdtangle crx in same folder
options = Options()
extension_path = 'crowdtangle.crx'
options.add_extension(extension_path)

# Creates Chrome driver with maximized windows and sets options
driver = webdriver.Chrome('./chromedriver', options=options)
driver.maximize_window()

# Opens Google.com
driver.get('https://www.google.com/')

# Waits for user to press enter in CLI until closing
input('Press Enter to Close')

# Closes driver
driver.close()
