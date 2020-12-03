import os
import time
import random
import requests
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from credentials import username as usr, password as passw
from seleniumwire import webdriver
import pickle
from igramscraper.instagram import Instagram

class Bot:
    def __init__(self, username, password , proxy= "learnmore2k20@gmail.com:JOfKHBr8HZ@64.225.19.160:8049" , tagged_page="fashionnova"):
        self.username = username
        self.password = password
        user_agent = "Mozilla/5.0 (iPhone; U; CPU iPhone OS 3_0 like Mac OS X; en-us) AppleWebKit/528.18 (KHTML, like Gecko) Version/4.0 Mobile/7A341 Safari/528.16"
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", user_agent)
        self.tags = tagged_page
        self.urls = []
        self.start = time.time()
        options = {
            'proxy': {
                'http': 'http://{}'.format(proxy),
                'https': 'https://{}'.format(proxy),
             
                }
        }
        self.bot  = webdriver.Firefox(seleniumwire_options=options , firefox_profile = profile  )
        self.bot.set_window_size(500, 950)
        self.number_of_comments = 0


    def exit(self):
        bot = self.bot
        bot.quit()

    def login(self):
        bot = self.bot
        bot.get('https://instagram.com/')
        time.sleep(5)

        if self.check_exists_by_xpath( "//button[text()='Accept']"):
            print("No cookies")
        else:
            bot.find_element_by_xpath("//button[text()='Accept']").click()
            print("Accepted cookies")
        if os.path.isfile(os.path.join(os.getcwd(), "{}.pkl".format(self.username))):
            cookies = pickle.load(open("{}.pkl".format(self.username), "rb"))
            for cookie in cookies:
                bot.add_cookie(cookie)
            bot.refresh()
            
        else:
            
            bot.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div/div/div/div[2]/button').click()
            print("Logging in...")
            time.sleep(1)
            username_field = bot.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[3]/div/label/input')
            username_field.send_keys(self.username)

            find_pass_field = (
                By.XPATH, '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[4]/div/label/input')
            WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_pass_field))
            pass_field = bot.find_element(*find_pass_field)
            WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_pass_field))
            pass_field.send_keys(self.password)
            bot.find_element_by_xpath(
                '/html/body/div[1]/section/main/article/div/div/div/form/div[1]/div[6]/button').click()
            time.sleep(4)

    def get_posts(self):
        print('Searching post by page...')
        bot = self.bot
        tags = self.tags
        
        
        link = "https://www.instagram.com/{}/tagged/".format(tags)
        bot.get(link)

        time.sleep(4)

        for i in range(2):
            ActionChains(bot).send_keys(Keys.END).perform()
            time.sleep(2)

        divs = bot.find_elements_by_xpath("//a[@href]")

        first_urls = []

        for i in divs:
            if i.get_attribute('href') != None:
                first_urls.append(i.get_attribute('href'))
            else:
                continue

        for url in first_urls:
            if url.startswith('https://www.instagram.com/p/'):
                self.urls.append(url)
        return self.comment(self.random_comment())

    def comment(self, comment):

        if len(self.urls) == 0:
            print('Finished tag jumping to next one...')
            return self.get_posts()

        bot = self.bot
        url = self.urls.pop()
        print('commenting...')
        bot.get(url)
        bot.implicitly_wait(1)

        bot.execute_script("window.scrollTo(0, window.scrollY + 300)")
        time.sleep(2)
        instagram = Instagram()
        username = bot.find_element_by_xpath("/html/body/div[1]/section/main/div/div/article/header/div[2]/div[1]/div[1]/a").text
        print(username)
        try : 
            image_link = bot.find_element_by_xpath("//img[@class='FFVAD']")
            print(image_link.get_attribute("src"))
            
        except : 
            time.sleep(1000)
        """bot.find_element_by_xpath(
            '/html/body/div[1]/section/main/div/div/article/div[3]/section[1]/span[1]/button').click()
        time.sleep(2)"""
        
        boolean = self.accountChecker(username)
        if(boolean) :
            try : 
            
                (bot.find_elements_by_class_name("wpO6b "))[2].click()
                
            
            except : 
                return self.comment(self.random_comment())

           
            find_comment_box = (
                By.XPATH, '/html/body/div[1]/section/main/section/div[1]/form/textarea')
            WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_comment_box))
            comment_box = bot.find_element(*find_comment_box)
            WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_comment_box))
            comment_box.click()
            time.sleep(1)
            comment_box.send_keys(comment)

            find_post_button = (
                By.XPATH, '/html/body/div[1]/section/main/section/div/form/button')
            WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_post_button))
            post_button = bot.find_element(*find_post_button)
            WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_post_button))
            post_button.click()
            try : 
                find_comment_box = (
                By.XPATH, '/html/body/div[1]/section/main/section/div[1]/form/textarea')
                WebDriverWait(bot, 50).until(
                EC.presence_of_element_located(find_comment_box))
                comment_box = bot.find_element(*find_comment_box)
                WebDriverWait(bot, 50).until(
                EC.element_to_be_clickable(find_comment_box))
                print(comment_box.text)
                self.number_of_comments =  self.number_of_comments + 1
                print("{} number of comments {}".format(self.username , self.number_of_comments))
            except : 
                print("{} is on hold ".format(self.username))
                time.sleep(1000)
            # edit this line to make bot faster
        time.sleep(random.randint(100,300))
        # ---------------------------------
        if(time.time() - self.start > 1800) : 
            time.sleep(1800)
        return self.comment(self.random_comment())


    def random_comment(self):
        with open(r'comments.txt', 'r' , encoding="utf-8") as f:
            commentsl = f.readlines()
        comments = commentsl
        comment = random.choice(comments)
        return comment


    def check_exists_by_xpath(self, xpath):
        try:
            self.bot.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return True

        return False
    def accountChecker(self , username) : 
        instagram = Instagram()
        instagram.set_proxies({
            'http': 'http://hp_739a8b6c:111111@167.71.74.160:7015',
            'https': 'http://hp_739a8b6c:111111@167.71.74.160:7015'
})
        try : 
            account = instagram.get_account(username)
        
            if(account.media_count > 5 and account.followed_by_count > 50 and account.followed_by_count <35000) : 
                return True 
            return False
        except : 
            return True
    
    

run = Bot(usr, passw)
run.login()

if __name__ == '__main__':
    if run.tags == []:
        print("Finished")
    else:
        run.get_posts()
