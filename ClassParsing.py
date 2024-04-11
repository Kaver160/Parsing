import time
import os
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import csv

logging.basicConfig(level=logging.ERROR, filename="py_log.log", filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")


class ParsingVacancies:

    def __init__(self, url):
        # self.url = input('Введите url для парсинга')
        self.file_name = input("введите имя файла:")
        self.driver = self._create_service(url)

    @staticmethod
    def _create_service(url):
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url)
        return driver

    def login_in_account(self):
        self.driver.find_element(By.CLASS_NAME, 'account-login-actions') \
            .find_element(By.CLASS_NAME, 'bloko-link').click()
        self.driver.find_element(By.CLASS_NAME, 'bloko-form-item').find_element(
            By.TAG_NAME, 'input').send_keys(os.getenv('USERNAME'))
        self.driver.find_element(By.CLASS_NAME, 'bloko-form-item').find_element(
            By.XPATH,
            '//*[@id="HH-React-Root"]/div/div/div[4]/div[1]/div/div/div/div'
            '/div/div[1]/div/div/form/div[2]/fieldset/input').send_keys(
            os.getenv('PASSWORD'))
        self.driver.find_element(By.CLASS_NAME, 'account-login-actions') \
            .find_element(By.TAG_NAME, 'button').click()
        time.sleep(7)

    def get_source_code(self):
        data = []
        try:
            list_vacancies = self.driver.find_element(By.CLASS_NAME,
                                                      'resume-serp-content') \
                .find_elements(By.CLASS_NAME,
                               'wrapper--eiknuhp1KcZ2hosUJO7g')
            count = 1
            for vacancies in list_vacancies:
                try:
                    xpath = (
                        '//*[@id="HH-React-Root"]/div/div/div[4]/div[1]/div/div/'
                        'div[2]/div[2]/div[3]/div[1]/div[{}]'
                    ).format(count)
                    label = self.driver.find_element(By.XPATH,
                                                     xpath).find_element(
                        By.CLASS_NAME,
                        'contacts-closed--XtQbIBwhAuw4VH8Xt8L6') \
                        .find_element(By.CSS_SELECTOR,
                                      '[data-qa="response-resume_show-phone-number"]')
                    self.driver.execute_script("arguments[0].click();", label)
                    time.sleep(1)
                    data.append({"name": vacancies.find_element(By.CSS_SELECTOR,
                                                                '[data-qa="resume-serp__resume-fullname"]').text,
                                 "telephone": str(vacancies.find_elements(
                                     By.CLASS_NAME,
                                     'field--_H26F7hkC9h1K_RsyjPq')[-1] \
                                                  .find_element(By.TAG_NAME,
                                                                'span').text),
                                 "vacation": vacancies.find_element(
                                     By.CLASS_NAME,
                                     'title--iPxTj4waPRTG9LgoOG4t').text
                                 })
                except Exception as e:
                    logging.error(e)
                count += 2
        except Exception as e:
            logging.error('Выбран не правильный каталог{}'.format(e))
        return data

    def create_csv(self, data_list):
        columns = ["name", "telephone", "vacation"]
        with open(self.file_name, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()
            for data in data_list:
                writer.writerow(data)

    def parsing(self):
        data_vacancies = []
        self.login_in_account()
        is_next_displed = False
        while not is_next_displed:
            data_vacancies.extend(self.get_source_code())
            try:
                button_next = self.driver.find_element(By.CLASS_NAME,
                                                       'pager') \
                                          .find_elements(By.CSS_SELECTOR,
                                                         '[data-qa="pager-next"]')[-1]
                self.driver.execute_script("arguments[0].click();",
                                           button_next)
                time.sleep(1)
            except Exception as e:
                is_next_displed = True
        self.driver.close()
        self.create_csv(data_vacancies)
        print('Парсинг завершён')


url = 'https://rabota.by/employer/vacancyresponses?vacancyId=38264095'
parsing_rabota = ParsingVacancies(url)
parsing_rabota.parsing()
