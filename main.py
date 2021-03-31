import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep

# insert account's credential
username = ''
password = ''
# insert a name or a link to the account we want to search
name = ''
link = ''

class Instabot:

    def __init__(self, username, password, name = '', link = ''):

        self.username = username
        self.password = password
        self.name = name
        self.link = link
        #insert your path of chromedriver.exe
        PATH = "C:\Program Files (x86)\chromedriver_win32\chromedriver.exe"
        self.driver = webdriver.Chrome(PATH)


    def run(self):
        self.login()
        sleep(3)
        if self.link != '':
            self.search_by_link()
        else:
            self.search_by_name()
        sleep(3)
        self.num_following = self.open_following()
        sleep(1)
        self.get_following()
        self.driver.quit()


    def login(self):
        self.driver.get("https://www.instagram.com/")

        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "react-root"))
            )
            #if your browser is in english, instead of "Accetta" put "Accept"
            accept_cookie = self.driver.find_element(By.XPATH, '//button[text()="Accetta"]')
            accept_cookie.click()

            emailInput = self.driver.find_elements_by_css_selector('form input')[0]
            passwordInput = self.driver.find_elements_by_css_selector('form input')[1]
            emailInput.send_keys(self.username)
            passwordInput.send_keys(self.password)
            login_button = self.driver.find_element_by_xpath("//button[@type='submit']")
            login_button.click()

        except:
            self.driver.quit()

    def search_by_name(self):
        searchbar = self.driver.find_element_by_class_name('XTCLo')
        searchbar.clear()
        searchbar.send_keys(self.name)
        sleep(2)
        searchbar.send_keys(Keys.ENTER)
        sleep(2)
        searchbar.send_keys(Keys.ENTER)

    def search_by_link(self):
        self.driver.get(self.link)

    def open_following(self):
        # if your browser is in english, instead of "profili seguiti" put "following"
        following = self.driver.find_element_by_partial_link_text("profili seguiti")
        following.click()
        text_following = following.text
        list_text_following = text_following.split()
        num_following = list_text_following[0]
        return num_following

    def get_following(self):
        nicknames = []
        i = 0

        jsCode = """followings = document.querySelector(".isgrP");
                    followings.scrollTo(0, followings.scrollHeight);         
                    var lenOfPage = followings.scrollHeight;
                    return lenOfPage;"""

        lenOfPage = self.driver.execute_script(jsCode)
        match = False

        while not match:
            lastCount = lenOfPage
            sleep(1)
            lenOfPage = self.driver.execute_script(jsCode)
            if lastCount == lenOfPage:
                match = True

        followings = self.driver.find_element_by_css_selector(".PZuss").text
        text_followings = followings.splitlines()
        #append all the nicknames of the text, the first is a nicknames and the others nicknames come right after the word 'segui' or 'following'
        try:
            while True:
                nicknames.append(text_followings[i])
                while True:
                    if text_followings[i] == "Segui":
                        i += 1
                        break
                    i += 1
        except IndexError:
            pass

        with open('nickname.csv', 'w', newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(['Id', 'Nickname'])
            writer.writerows([[x + 1, nickname] for x, nickname in enumerate(nicknames)])


if __name__ == "__main__":
    bot = Instabot(username, password, name)
    bot.run()

