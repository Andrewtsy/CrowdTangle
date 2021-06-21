from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
import csv
import time
import os

class Scraper:
    def __init__(self):
        self.coords = {}
        self.links = []

        # Rows with links should be in form Link: '....'
        with open('input.csv') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                self.links.append(row[0].split()[1])
        
        with open('cred.txt', 'r') as filereader:
            self.un, self.pw = map(lambda x: x.strip('\n'), filereader.readlines())
        
        # First download crowdtangle crx file into specified path, more docs coming soon...
        self.options = Options()
        extension_path = 'crowdtangle.crx'        
        self.options.add_extension(extension_path)
        download_path = r'C:\Users\Andrew\Code\CrowdTangle\downloads'
        p = {'download.default_directory': download_path}
        self.options.add_experimental_option('prefs', p)
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
    
        
    def start(self, link):
        # retrieves first link for authentification
        self.driver.get(link)
        assert 'No results found.' not in self.driver.page_source
        time.sleep(5)
    
    def enter(self, link):
        # retrives link
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get(link)
        assert 'No results found.' not in self.driver.page_source
        self.current_title = self.driver.title
        if self.current_title.strip() == '' or self.current_title.strip() == None:
            self.current_title = (link)
        time.sleep(5)
    
    def click(self, value, wait, conf=1, image='images/placeholder.png'):
        if not value in self.coords.keys():
            self.coords[value] = pyautogui.locateCenterOnScreen(image, confidence = conf)
        pyautogui.click(self.coords[value])
        time.sleep(wait)
    
    def auth(self, value, wait, post, conf=None, image=None):
        if not value in self.coords.keys():
            self.coords[value] = pyautogui.locateCenterOnScreen(image, confidence = conf)
        pyautogui.click(self.coords[value])
        time.sleep(1)
        pyautogui.typewrite(post)
        time.sleep(wait)
        
    def download_path(self, article_title, social_media):
        new_name= '-'.join(article_title.split() + [social_media])
        new_name = ''.join(i for i in new_name if i.isalnum() or i == '-') + '.csv'
        time.sleep(1)
        fname = max([f for f in os.listdir('downloads')], key=lambda x: os.path.getctime(os.path.join('downloads', x)))
        while '.part' in fname:
            time.sleep(1)
        os.rename(os.path.join('downloads', fname), os.path.join('downloads', new_name))
    
def main():
    
    scraper = Scraper()
    scraper.start('https://www.google.com/')
    # Open CrowdTangle
    scraper.click('extensions', 1, 0.8, 'images/extensions_icon.png')
    scraper.click('pin', 1, 0.8, 'images/pin_icon.png')
    scraper.click('extensions', 1)
    scraper.click('crowdtangle', 6, 0.7, 'images/crowdtangle_icon.png')
    # Open Login Page
    scraper.click('login', 2.5, 0.7, 'images/login_icon.png')
    # Enter username/email
    scraper.auth('email', 1, scraper.un, 0.8, 'images/email_icon.png')
    # Enter password
    scraper.auth('password', 1, scraper.pw, 0.8, 'images/password_icon.png')
    # Submit Login
    scraper.click('login_sub', 5, 0.8, 'images/login_sub_icon.png')
    # Open Selenium Chrome Driver.
    # [insert more quirky docs later]
    for link in scraper.links:
        scraper.enter(link)
        # Reopen CrowdTangle
        scraper.click('crowdtangle', 5)
        # Download Data
        scraper.click('download', 2, 0.8, 'images/download_icon.png')
        scraper.download_path(scraper.current_title, 'facebook')
        for i in ['twitter', 'reddit', 'instagram']:
            image = 'images/{}_icon.png'.format(i)
            scraper.click(i, 5, 0.7, image)
            scraper.click('download', 1)
            scraper.download_path(scraper.current_title, i)
        scraper.driver.close()
        scraper.driver.switch_to.window(scraper.driver.window_handles[0])
        # input('Press Enter to continue')
    scraper.driver.quit()
    
if __name__ == '__main__':
    main()