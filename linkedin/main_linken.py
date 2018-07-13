import linkedin.param_linken as paramaters
import csv

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from parsel import Selector


class LinkenApp:
    def __init__(self, password, email, search_name):
        path_name = 'site:linkedin.com/in/ AND + ' + search_name + ''

        writer_csv = csv.writer(open(paramaters.file_name, 'w'))
        writer_csv.writerow(['Name', 'Description', 'company', 'Location', 'URL'])

        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.set_preference('permissions.default.stylesheet', 2)
        firefox_profile.set_preference('permissions.default.image', 2)
        firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

        driver = webdriver.Firefox(firefox_profile=firefox_profile,
                                   executable_path='../geckodriver')

        driver.get('https://www.linkedin.com/?trk=nav_logo')

        email_input = driver.find_element_by_class_name('login-email')
        email_input.send_keys(password)

        password_input = driver.find_element_by_class_name('login-password')
        password_input.send_keys(email)

        sign_btn = driver.find_element_by_xpath('//*[@type="submit"]')
        sign_btn.click()

        sleep(1)

        driver.get('https://www.google.com')

        search_name = driver.find_element_by_name('q')
        search_name.send_keys(path_name)

        google_start = driver.find_element_by_name('btnK')
        google_start.click()

        linkedin_links = driver.find_elements_by_tag_name('cite')
        linkedin_links_arr = [url.text for url in linkedin_links]

        for linkedin_url in linkedin_links_arr:
            driver.get(linkedin_url)
            sleep(2.5)

            sel = Selector(text=driver.page_source)

            name_person = sel.xpath('//h1/text()').extract_first()
            desc_person = sel.xpath('//h2/text()').extract_first()
            company_person = sel.xpath(
                '//*[starts-with(@class, "pv-top-card-section__company Sans-17px-black-70% mb1 inline-block")]/text()').extract_first()

            if company_person:
                company_person = company_person.strip()

            location_person = sel.xpath(
                '//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
            url_person = driver.current_url

            if company_person is None:
                company_person = ' No company '

            if name_person is None:
                name_person = ' No name '

            if desc_person is None:
                desc_person = ' No desc '

            if location_person is None:
                location_person = ' No location '

            if url_person is None:
                url_person = ' No url '

            name = self.validate_field(name_person)
            desc = self.validate_field(desc_person)
            company = self.validate_field(company_person)
            location = self.validate_field(location_person)
            url = self.validate_field(url_person)

            print('\n')
            print('Name: ', name)
            print('Description: ', desc)
            print('Company: ', company)
            print('Location: ', location)
            print('URL: ', url)
            print('\n')

            writer_csv.writerow([name_person.encode('utf-8'),
                                 desc_person.encode('utf-8'),
                                 company_person.encode('utf-8'),
                                 location_person.encode('utf-8'),
                                 url_person.encode('utf-8')])

            try:
                driver.find_element_by_xpath(
                    '//*[@class="pv-s-profile-actions '
                    'pv-s-profile-actions--connect '
                    'button-primary-large '
                    'mh1 '
                    'mt2"]').click()

                sleep(1)

                driver.find_element_by_xpath('//*[@class="button-primary-large ml1"]').click()

                sleep(1)

            except Exception:
                print('You can not contact with him :(')
                pass

        driver.quit()

    def validate_field(self, field):
        if field:
            pass

        else:
            field = ''

        return field


if __name__ == '__main__':
    app = LinkenApp()