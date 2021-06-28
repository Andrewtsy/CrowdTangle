"""This script was created by Andrew Tao for Professor Jennifer Pan
in order to automate the CrowdTangle Chrome Extension.

Users should enter csv file of article links upon inquiry.

Pauses (time.sleep()) are sometimes necessary, other times not.
This may depend on system's/browser's speed/noise and is subject
to adjustments according to user wishes.
Locate by element confidence may also be subject to change according
to screen specs/ratio.
When used in the docs, 'element' refers to the thing that is clicked on screen.

Happy Automating!
"""

import csv
import time
import os
from datetime import datetime

import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui


class Scraper:
    """Class to hold the driver and attributes needed
    Note that term scraper is not technically accurate and is used loosely so as to have no possibility of conflict with driver
    and because it looks pretty (aesthetic value?) for the purposes of docs they will be used interchangeably

    Attributes
    ----------
    links : list
        stores a list of links (self-explanatory)
    coords : dict
        dictionary of coordinates assigned to each object to be clicked.
        physical coordinates are used as in tandem with locate by image
        where the latter is used to identify when the item has loaded and the former is used to click it.
    current_title : str
        tempory value of the current article title.
        this changes for each new article (older ones are not stored)
    un : str
        self-explanatory. See file opening comments for information on file feeding.
    pw : str
        self-explanatory. See file opening comments for information on file feeding.
    options : class
        not technically needed as an instance attribute in this scenario,
        but could be nice if one wanted to build/adjust multiple 'scrapers' with different options
    driver : class
        all important Selenium driver – heart of the object

    Methods
    -------
    primary_setup():
        primes the instance with all its tools (esp. coordinates)
    enter(link):
        opens each new article and extracts its title
    click(value, conf=1, image='images/placeholder.png',
              location=None, bycoords=False, clicked=True)
        used either to click or locate each element
    auth(post, conf=None, image=None, location=None):
        used for email/password entering
    download(social_media, loaded=None, location=None):
        downloads each of the csv files with the right name and path
    """

    def __init__(self):
        """Starts scraper with attributes explained above and creates driver"""

        self.links = []
        self.coords = {}
        self.current_title = ''

        # Rows with links should only contain link in form ['https://www...]
        with open(input('Please enter csv file of article links: ')) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row:
                    self.links.append(row[0].strip())

        # This simply reads text file for Facebook username and password
        # File should be in format:
        # [USERNAME]
        # [PASSWORD]
        # encrypted file or direct user input may be substitued if user would like
        with open('cred.txt', 'r') as filereader:
            self.un, self.pw = map(lambda x: x.strip('\n'), filereader.readlines())

        self.options = Options()

        # Adds crowdtangle extension into driver
        # Assumes environment is setup with crowdtangle crx in same folder
        extension_path = 'crowdtangle.crx'
        self.options.add_extension(extension_path)

        # Sets driver download path to designated downloads folder in same directory
        # Path may be adjusted if wished, however user should also adjust download file naming (see download method)
        download_path = os.path.abspath('downloads')
        p = {'download.default_directory': download_path}
        self.options.add_experimental_option('prefs', p)

        # Creates Chrome driver with maximized windows and sets options
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()

    def primary_setup(self):
        """This is the important priming of the driver.
        The main goals are to pin CrowdTangle extension icon,
        login to Facebook for access,
        and collect needed coordinates using pyautogui\'s *amazing* locate by image (paired with opencv).
        This is done on Google homepage as a dummy site *(they\'re not dum)*
        so as to avoid interfering/unpredictable elements.
        """

        self.driver.get('https://www.google.com/')
        assert 'No results found.' not in self.driver.page_source
        # Opens extensions addon, pins CrowdTangle to bar, and opens CrowdTangle
        self.click('extensions', 0.8, 'images/extensions_icon.png')
        self.click('pin', 0.8, 'images/pin_icon.png')
        self.click('extensions', 0.8, 'images/extensions_clicked_icon.png')
        self.click('crowdtangle', 0.8, 'images/crowdtangle_icon.png')
        # Opens (Powered by Facebook) Login Page
        self.click('login', 0.7, 'images/login_icon.png')
        # Enters username/email
        self.auth(self.un, 0.8, 'images/email_icon.png')
        # Enters password
        self.auth(self.pw, 0.8, 'images/password_icon.png')
        # Submits Login
        self.click('login_sub', 0.8, 'images/login_sub_icon.png')
        # Reopens CrowdTangle
        self.click('crowdtangle', image='images/crowdtangle_icon.png', bycoords=True)
        # Each of these 'clicks' doesn't actually click the item (clicked=False)
        # Instead they use locate by image to extract the physical coordinates to the coords dicationary to be used later
        # Note that Facebook's icon is not needed as it opens upon startup of CrowdTangle
        self.click('download', 0.85, 'images/download_icon.png', clicked=False)
        for i in ['Twitter', 'Reddit', 'Instagram']:
            image = 'images/{}_icon.png'.format(i.lower())
            self.click(i, 0.7, image, clicked=False)

    def enter(self, link):
        """
        Accesses each individual article while seeing if each link is valid.
        If invalid, the CrowdTangle is not used.

        Parameters
        ----------
        link : str
            url to article; should begin with 'https://www.'

        Returns
        -------
        bool
            returns whether article link was valid/successfully opened.
        """

        # opens new tab and link
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        try:
            self.driver.get(link)
        except selenium.common.exceptions.InvalidArgumentException:
            # if link is invalid exception is thrown, page is closed, and driver moves on to next link
            print('{} is invalid url (aka unable to access)'.format(link))
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            return False
        assert 'No results found.' not in self.driver.page_source
        # attempts to set current_title to filtered string with only alphanumeric characters
        # this is done so there are no encoding/filenaming errors and resulting name is typically PascalCase
        try:
            self.current_title = ''.join([i for i in self.driver.title if i.isalnum()])
        except TypeError:
            pass
        # if extracted/cut title is wacko (nonexistent) the article link is substitued as title
        if self.current_title == '' or self.current_title.strip() is None:
            self.current_title = (link)
        time.sleep(0.25)
        return True

    def click(self, value, conf=1, image='images/placeholder.png',
              location=None, bycoords=False, clicked=True):
        """
        Clicks on given element (value).
        When in the priming stage, bycoords is set to False:
            physical coordinates are collected using locate by image
        When in the extraction stage, bycoords is always set to True:
            locate by image is used to verify when element has loaded
            locate by coordinates is used to click it

        Parameters
        ----------
        value : str
            indicates which element is being selected
        conf : float, optional
            confidence used by opencv. Set on scale of 0-1,
            higher confidence means image location is more selective (used for elements that may look like other elements)
            lower confidence is less selective (used for elements that may have greater variation across different screens).
            The default is 1.
        image : str, optional
            filename of the image to be used. They are all stored in the 'images' folder. The default is 'images/placeholder.png'.
        location : NoneType/class, optional
            pyautogui's point class. Essentially a tuple of (x,y) screen coordinates to be given by coords dictionary or locate by image. The default is None.
        bycoords : bool, optional
            whether or not to locate by coords (False with priming/locate by image, True with bulk of actual extraction). The default is False.
        clicked : bool, optional
            whether or not to click on element (False only when priming/locate by image for download button and [Twitter, Reddit, Instagram] icons
             so as not to extract data from Google, True for all else). The default is True.
        """

        # logs start_time for later measure of execution time
        start_time = datetime.now()
        time.sleep(0.25)
        # main loop to look for element using locate by image.
        while location is None:
            try:
                # tries to locate element by image (meant to ensure loading is finished and/or element has appeared). If not found, location is stored as None, and loop continues running
                location = pyautogui.locateCenterOnScreen(image, confidence=conf)
                # in priming (primary setup) location bycoords is turned off and the location coordinates are stored to coords
                if bycoords is False and location is not None:
                    self.coords[value] = location
            except ImageNotFoundException:
                pass
            # if over ten seconds has elapsed without successful identification of image, loading is assumed to have finished and loop is automatically broken
            if (datetime.now() - start_time).total_seconds() > 10:
                break
        # locating by coordinates is used
        if bycoords is True:
            location = self.coords[value]
        # element is clicked
        if clicked is True:
            pyautogui.click(location)

    def auth(self, post, conf=None, image=None, location=None):
        """
        Special authentification steps. Similar to click method, but more specialized and posts identification info

        Parameters
        ----------
        post : str
            indicates the string to be posted to input box (username or password).
        conf : NoneType/float, optional
            confidence used by opencv. Set on scale of 0-1,
            higher confidence means image location is more selective (used for elements that may look like other elements)
            lower confidence is less selective (used for elements that may have greater variation across different screens).
            The default is 1.
        image : NoneType/str, optional
            filename of the image to be used. They are all stored in the 'images' folder. The default is 'images/placeholder.png'.
        location : NoneType/class, optional
            pyautogui's point class. Essentially a tuple of (x,y) screen coordinates to be given by coords dictionary or locate by image. The default is None.
        """

        time.sleep(0.25)
        # main loop to look for element (same as above)
        # authenficiation on login page is very bare and tends not to mess up
        while location is None:
            try:
                location = pyautogui.locateCenterOnScreen(image, confidence = conf)
            except ImageNotFoundException:
                pass
        pyautogui.click(location)
        time.sleep(0.5)
        # enter username/password
        pyautogui.typewrite(post)

    def download(self, social_media, loaded=None, location=None):
        """
        Download steps.
        Part 1 is similar to click method with a catch:
            Sometimes there is no data for a social media in an article. If so, after 5 seconds of loading, loop is broken
        Part 2 changes each downloaded file's name to unique name:
            Note that while most likely not, there is a possibilty that os steps may need to be changed for different OS (Windows is used here)

        Parameters
        ----------
        social_media : str
            name of social media in question: ['Facebook', 'Twitter', 'Reddit', 'Instagram'].
        loaded : NoneType/class, optional
            indicates whether the element has loaded. While not loaded, value is set to None, when loaded value is set to point class of image coordinates.
            Image in question is a slice of screen only displayed after CrowdTangle's social media block has loaded (see images folder for 'images/loaded_icon'. The default is None.
        location : NoneType/class, optional
            pyautogui's point class. Essentially a tuple of (x,y) screen coordinates to be given by coords dictionary or locate by image. The default is None.

        """

        start_time = datetime.now()
        time.sleep(0.25)
        # P1. Loop should only quit once element is found and data is done loading/exists (or too much time elapses)
        while location is None or loaded is None:
            try:
                # attempts to locate download image on screen to verify it is there
                location = pyautogui.locateCenterOnScreen(image='images/download_icon.png', confidence=0.8)
                # identifies if there is data present (when data is present the below image is also present)
                loaded = pyautogui.locateCenterOnScreen(image='images/loaded_icon.png', confidence=0.7)
            except ImageNotFoundException:
                pass
            # if 5 seconds have elapsed and the data/loaded image is not present, the data is taken to be unavailable and scraper moves on
            if (datetime.now() - start_time).total_seconds() > 5:
                if loaded is None:
                    print('May have missed {} data for {} (no data available)'.\
                          format(social_media, self.current_title))
                    return None
                break
        # locate and click by image
        location = self.coords['download']
        pyautogui.click(location)

        time.sleep(2)
        # P2. Loop checks for downloaded file and sets that to fname. Each newly downloaded file from CrowdTangle has format 'data (?).csv'.
        # if the most recent file starts with 'data' ie. hasn't been named yet, we know the download we initiated above has finished and we change the file's name.
        fname = ''
        while not fname.startswith('data'):
            # sets fname to the most recent file. Keeps looping until this become the unnamed file we want.
            fname = max(os.listdir('downloads'),
                        key = lambda x: os.path.getatime(os.path.join('downloads', x)))
            time.sleep(1)
            # 50 seconds total elapsed is rather generous, but if it takes that long, something is definitely wrong and we exit the method
            if (datetime.now() - start_time).total_seconds() > 50:
                print('May have misdownloaded {} data for {} as "data(?)"'.\
                      format(social_media, self.current_title))
                return None
        # new name file is the article title plus the social media name extracted from CrowdTangle typically PascalCase
        new_name = ''.join((self.current_title, social_media, '.csv'))
        # renames the file
        try:
            os.rename(os.path.join('downloads', fname),
                      os.path.join('downloads', new_name))
        # if one has already run the script on the article there will already be a file with the given name there. This will throw an os error.
        # to solve for this, we add an incremented integer to the back until a fresh name is availabe. Note that exception type may need to be changed for different OS.
        except WindowsError:
            count = 1
            while True:
                try:
                    os.rename(os.path.join('downloads', fname),
                              os.path.join('downloads', ''.join((new_name[:-4], '(', str(count), ')', '.csv'))))
                except WindowsError:
                    count += 1
                else:
                    break
        print('Extracted {} data for {}'.format(social_media, self.current_title))

def main():
    """Main code to be run"""

    # scraper instance is created from class. This will be our primary protagonist!
    scraper = Scraper()
    # runs primary_setup/priming of scraper.
    scraper.primary_setup()
    # main loop that loops through each article link and extracts data
    for link in scraper.links:
        # enters/setsup article. Skips article if invalid url.
        if scraper.enter(link):
            # reopens CrowdTangle
            scraper.click('crowdtangle', conf=0.7, image='images/crowdtangle_icon.png', bycoords=True)
            # downloads Facebook data
            scraper.download('Facebook')
            for i in ['Twitter', 'Reddit', 'Instagram']:
                image = 'images/{}_icon.png'.format(i.lower())
                # clicks on each social media icon to shift to that social media
                scraper.click(i, conf=0.7, image=image, bycoords=True)
                time.sleep(2.5)
                # downloads the data
                scraper.download(i)
            # closes article page and shifts back to Google dummy/homepage
            scraper.driver.close()
            scraper.driver.switch_to.window(scraper.driver.window_handles[0])
    # ends the scraper/driver
    scraper.driver.quit()

if __name__ == '__main__':
    # runs the script!
    main()
