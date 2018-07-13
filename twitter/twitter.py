from selenium import webdriver
import sys

import unittest, time, re
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import os.path
import re
import collections
import pymorphy2
import nltk


class AppTwitter:
    def __init__(self, email, password, parse_name):
        path = '../twitter/data'

        self.grab_followers_num = 5
        self.scroll_num = 5

        if os.path.exists(path) is False:
            os.mkdir(path)

        firefox_profile = webdriver.FirefoxProfile()

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile,
                                        executable_path='../geckodriver')
        self.parse_name = parse_name

        self.driver.person_url = 'https://twitter.com/' + self.parse_name + '/following'
        self.driver.login_url = 'https://twitter.com/login'

        self.email_user = email
        self.password_user = password

        self.driver.get(self.driver.login_url)

        self.login()

        time.sleep(1)

        self.driver.get(self.driver.person_url)

        self.scroll()

        self.main_info()

        self.driver.close()

    def login(self):

        email_input = self.driver.find_element_by_xpath('//input[@class="js-username-field email-input js-initial-focus"]')
        email_input.send_keys(self.email_user)

        password_input = self.driver.find_element_by_xpath('//input[@class="js-password-field"]')
        password_input.send_keys(self.password_user)

        time.sleep(1)

        password_input.submit()

    def main_info(self):

        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        arr = [x.div['data-screen-name'] for x in soup.body.findAll('div', attrs={'data-item-type': 'user'})]

        bios = [x.p.text for x in soup.body.findAll('div', attrs={'data-item-type': 'user'})]

        fullnames = [x.text.strip() for x in soup.body.findAll('a', 'fullname')][1:]

        time.sleep(0.5)

        a_info_main = {
            'usernames': arr,
            'bios': bios,
            'fullnames': fullnames}

        main_info_person = pd.DataFrame(data=a_info_main)

        print(main_info_person)

        main_info_person.to_csv('../twitter/data/BASICDATA_profile.csv')

        df_person = pd.read_csv('../twitter/data/BASICDATA_profile.csv', encoding="ISO-8859-1")

        arr = df_person.usernames

        self.grab_twits()

        self.grab_followers(arr)

    def grab_followers(self, arr):

        time.sleep(1)

        for i in range(0, self.grab_followers_num):
            current_user = arr[i]
            print('User ' + str(i) + ': ' + current_user)

            self.driver.base_url = "https://twitter.com/" + current_user + "/following"
            self.driver.get(self.driver.base_url)

            time.sleep(1.5)

            self.scroll()

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            name_follower_arr = [x.div['data-screen-name'] for x in
                                 soup.body.findAll('div', attrs={'data-item-type': 'user'})]
            bio_follower_arr = [x.p.text for x in soup.body.findAll('div', attrs={'data-item-type': 'user'})]

            d = {'usernames': name_follower_arr,
                 'bios': bio_follower_arr}
            df = pd.DataFrame(data=d)

            df.to_csv('../twitter/data/' + current_user + '.csv')

    def grab_twits(self):

        self.driver.base_url = "https://twitter.com/" + self.parse_name + "/with_replies"
        self.driver.get(self.driver.base_url)
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        time.sleep(1)

        self.scroll()

        time.sleep(1)

        name_follower = soup.find('a', class_="ProfileHeaderCard-nameLink").text

        location_follower = soup.find('img', alt_='HTML Academy')
        location_follower = location_follower.text.strip() if location_follower else ''

        link_info_follower = soup.find('span', class_='ProfileHeaderCard-urlText')
        link_info_follower = link_info_follower.a.get('title') if link_info_follower else None

        twits_follower = soup.find('a', {'data-nav': 'tweets'})
        twits_follower = twits_follower.find('span', class_='ProfileNav-value')['data-count'] if twits_follower else 0

        following_follower = soup.find('a', {'data-nav': 'following'})
        following_follower = following_follower.find('span', class_='ProfileNav-value')[
            'data-count'] if following_follower else 0

        followers_follower = soup.find('a', {'data-nav': 'followers'})
        followers_follower = followers_follower.find('span', class_='ProfileNav-value')[
            'data-count'] if followers_follower else 0

        favorites_follower = soup.find('a', {'data-nav': 'favorites'})
        favorites_follower = favorites_follower.find('span', class_='ProfileNav-value')[
            'data-count'] if favorites_follower else 0

        text_follower_arr = soup.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
        text_follower = [''.join(x.text) for x in text_follower_arr]

        text_without_link = []

        for x in text_follower_arr:
            if x.find(text=True) is None:
                print('CAN NOT READ THIS')
                continue

            text_without_link.append(x.find(text=True).strip())



        text_list = []

        for x in text_follower_arr:
            x = x.find(text=True)

            text_list.append(self.translate_ru(x))

        activity_tweets_follower = soup.find_all('li', class_='js-stream-item')

        activity_time_follower = soup.find_all('span', class_='_timestamp')
        activity_time_follower = [x.text.strip() for x in activity_time_follower]

        main = pd.DataFrame(data={
            'name': [name_follower],
            'location': [location_follower],
            'link info': [link_info_follower],
            'twits': [twits_follower],
            'following': [following_follower],
            'followers': [followers_follower],
            'likes': [favorites_follower],
            'most popular word in all selected twits': [self.translate_ru(text_without_link)],
            'twits: ': [len(activity_tweets_follower)]
        })

        main.to_csv('../twitter/data/BASICDATA.csv')

        a_person_posts = {
            'text tweets': text_follower,
            'time tweets': activity_time_follower,
            'popular word': text_list
        }

        main_person_posts = pd.DataFrame(data=a_person_posts)

        main_person_posts.to_csv('../twitter/data/BASICDATA_profile_twits.csv')

    def scroll(self):
        loop_counter = 0

        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            if loop_counter > self.grab_followers_num:
                break

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            time.sleep(1)
            min_height = self.driver.execute_script("return document.body.scrollHeight")

            if min_height == last_height:
                break

            last_height = min_height
            loop_counter = loop_counter + 1

        print('Кол-во скролов: ', str(loop_counter))

    def translate_ru(self, item_arr):
        text_item = str(item_arr).split()

        functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}
        text_item = [item for item in text_item if self.pos(item) not in functors_pos]

        popular_text = collections.Counter(re.findall(r'\w+', str(text_item))).most_common()

        if len(popular_text) > 0:
            popular_text = sorted(x for x, cnt in popular_text if cnt == popular_text[0][1])[0]
        else:
            popular_text = 'None'

        return popular_text

    def pos(self, word, morth=pymorphy2.MorphAnalyzer()):
        return morth.parse(word)[0].tag.POS


if __name__ == '__main__':
    app = AppTwitter()
