from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup
from xlsxwriter import Workbook

import os
import requests
import shutil


class AppInsta:
    def __init__(self,
                 user_name,
                 password,
                 target_name,
                 path='../instagram/photos'):

        self.user_name = user_name
        self.password = password
        self.target_name = target_name
        self.path = path

        firefox_profile = webdriver.FirefoxProfile()
        # firefox_profile.set_preference('permissions.default.stylesheet', 2)
        # firefox_profile.set_preference('permissions.default.image', 2)
        # firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        self.driver = webdriver.Firefox(firefox_profile=firefox_profile, executable_path='../geckodriver')

        self.error = False
        self.main_url = 'https://www.instagram.com'
        self.driver.get(self.main_url)

        scroll_height = '.scrollHeight'
        scroll_subs = 'document.getElementsByClassName("_gs38e")[0]'
        scroll_body = 'document.body'

        if os.path.exists(path) is False:
            os.mkdir(path)

        sleep(1)

        self.log_in()

        sleep(1)

        if self.error is False:
            self.close_dialog_popup()
            self.input_search_profile()

        if self.error is False:
            self.info_user()
            self.input_sub()

            sleep(1)

            self.scroll(scroll_subs + '.scrollTo(0, ' + scroll_subs + scroll_height + ');', scroll_subs + scroll_height)

            sleep(1)

            self.sub_to_excel()

            sleep(1)

            self.input_close_sub()

        if self.error is False:
            self.scroll('window.scrollTo(0, ' + scroll_body + scroll_height + ');', scroll_body + scroll_height)

        if self.error is False:
            self.download_img()

        self.driver.quit()

    def log_in(self):
        try:
            print('Заходим на главную страницу')

            log_in_btn = self.driver.find_element_by_xpath('//p[@class="_g9ean"]/a')
            log_in_btn.click()

            try:
                print('Вводим имя и пароль')

                user_name_input = self.driver.find_element_by_xpath('//input[@name="username"]')
                user_name_input.send_keys(self.user_name)

                password_input = self.driver.find_element_by_xpath('//input[@name="password"]')
                password_input.send_keys(self.password)

                sleep(1)

                password_input.submit()

                self.close_settings_tab()

            except Exception:
                self.error = True
                print('Не нашли поле Юзер или Пароль')

        except Exception:
            self.error = True
            print('Не нашли поле Вход')

    def close_dialog_popup(self):
        try:
            print('Закрываем окно всплывающее')
            sleep(1)

            close_btn_v2 = self.driver.find_element_by_xpath('//button[@class="_dbnr9"]')
            close_btn_v2.click()

            sleep(1)

        except Exception:
            pass

    def close_settings_tab(self):
        try:

            self.driver.switch_to.window(self.driver.window_handles[1])
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])

        except Exception as e:
            pass

    def input_search_profile(self):
        try:
            print('Нажимаем на поле Поиск профиля')

            sleep(1)

            input_search = self.driver.find_element_by_xpath('//input[@class="_avvq0 _o716c"]')
            input_search.send_keys(self.target_name)

            profile_url = self.main_url + '/' + self.target_name + '/'
            self.driver.get(profile_url)

            sleep(1)

        except Exception:
            self.error = True
            print('Не нашли поле Поиск профиля')

    def scroll(self, script, initial_height):
        try:
            loop_counter = 0

            last_height = self.driver.execute_script("return " + initial_height + "")

            while True:
                if loop_counter > 12:
                    break

                self.driver.execute_script(script)

                sleep(1)
                min_height = self.driver.execute_script("return " + initial_height + "")

                if min_height == last_height:
                    break

                last_height = min_height
                loop_counter = loop_counter + 1

        except Exception:
            self.error = True
            print('Не нашли нужный селектор')

    def info_user(self):
        try:
            print('Получаем информацию нашего Юзера')

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            all_info = soup.find_all('li', class_='_bnq48 ')

            text = [info.text for info in all_info]

            return ', '.join(text)

        except Exception:
            print('Не смогли получить информацию')

    def input_sub(self):
        try:
            print('Открываем окно с подписчиками')

            subs_button = self.driver.find_element_by_xpath('//a[@href="/' + self.target_name + '/following/"]')
            subs_button.click()

        except Exception:
            print('Не смогли открыть окно с подписчиками')

    def sub_desc(self):
        try:
            print('Получаем ники подписчиков')

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            all_subs_desc = soup.find_all('a', class_='_2g7d5 notranslate _o5iw8 ')

            sub_desc = [sub_val.text for sub_val in all_subs_desc]

            return sub_desc

        except Exception:
            print('Не смогли получить ники подписчиков')

    def sub_names(self):
        try:
            print('Получаем имена подписчиков')

            soup = BeautifulSoup(self.driver.page_source, 'lxml')

            all_subs_names = soup.find_all('div', class_='_9mmn5 ')

            sub_names = [sub_val_name.text for sub_val_name in all_subs_names]

            return sub_names

        except Exception:
            print('Не смогли получить имена подписчиков')

    def sub_to_excel(self):
        print('Записываем данные в эксель ...')

        workbook = Workbook(os.path.join(self.path, 'info_subs.xlsx'))

        worksheet = workbook.add_worksheet()
        row = 0

        worksheet.write(row, 0, 'Descriptions')
        worksheet.write(row, 1, 'Subscriber names')

        row += 1

        for desc in self.sub_desc():
            worksheet.write(row, 0, desc)
            row += 1

        row = 1

        for name in self.sub_names():
            worksheet.write(row, 1, name)
            row += 1

        print('Все ок!')

        workbook.close()

    def input_close_sub(self):
        print('Закрываем окно с подписчиками')

        input_close = self.driver.find_element_by_xpath('//button[@class="_dcj9f"]')
        input_close.click()

    def write_to_exel(self, images, path):
        print('Записываем в эксель ...')

        workbook = Workbook(os.path.join(path, 'info_photos.xlsx'))

        worksheet = workbook.add_worksheet()
        row = 0

        worksheet.write(row, 0, 'Info about user: ' + self.info_user())
        worksheet.write(row, 1, 'Image name')
        worksheet.write(row, 2, 'Caption')

        row += 1

        for index, img in enumerate(images):
            file_name = 'image_' + str(index) + '.jpg'

            try:
                hash_tag = img['alt']

            except KeyError:
                hash_tag = 'No hash tags for this photo!'

            worksheet.write(row, 1, file_name)
            worksheet.write(row, 2, hash_tag)
            row += 1

        print('Записали!')

        workbook.close()

    def download_tag_img(self, images):
        print('Загружаем хеш-теги фотографий')

        tag_img_path = os.path.join(self.path, 'hash_tags')

        if os.path.exists(tag_img_path) is False:
            os.mkdir(tag_img_path)

        self.write_to_exel(images, tag_img_path)

        for index, image in enumerate(images):

            try:
                hash_tags = image['alt']

            except KeyError:
                hash_tags = 'No hash tags for this photo'

            file_name = 'hash_tags_photo_' + str(index) + '.txt'
            file_path = os.path.join(tag_img_path, file_name)

            link = image['src']

            with open(file_path, 'wb') as file:
                file.write(str('link: ' + str(link) + '\n' + 'caption: ' + hash_tags).encode())

    def download_img(self):
        print('Загружаем фотографии')

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        arr_img = soup.find_all('img')

        self.download_tag_img(arr_img)

        for index, img in enumerate(arr_img):
            file_name = 'image_' + str(index) + '.jpg'
            img_path = os.path.join(self.path, file_name)
            link = img['src']

            res = requests.get(link, stream=True)

            try:
                with open(img_path, 'wb') as file:
                    shutil.copyfileobj(res.raw, file)

            except Exception:
                self.error = True
                print('Error when trying to copy file ', index)
                print('Image link: ', link)


if __name__ == '__main__':
    app = AppInsta()