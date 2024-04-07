import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

service = Service(ChromeDriverManager().install())
URl = 'https://rabota.by/employer/vacancyresponses?vacancyId=34590154'


def login_in_account(driver):
    driver.find_element(By.CLASS_NAME, 'bloko-form-item').find_element(By.TAG_NAME, 'input').send_keys(username)
    driver.find_element(By.CLASS_NAME, 'bloko-form-item').find_element(By.XPATH, '//*[@id="HH-React-Root"]/div/div/div[4]/div[1]/div/div/div/div/div/div[1]/div/div/form/div[2]/fieldset/input').send_keys(password)
    driver.find_element(By.CLASS_NAME, 'account-login-actions').find_element(By.TAG_NAME, 'button').click()
    time.sleep(7)
    return driver


def get_source_code(URL:str) -> None:
    driver = webdriver.Chrome(service=service)
    driver.get(URl)
    driver.find_element(By.CLASS_NAME,'account-login-actions').find_element(By.CLASS_NAME, 'bloko-link').click()
    time.sleep(2)
    driver = login_in_account(driver)
    driver.find_element(By.CLASS_NAME, 'resume-serp-content').find_elements()



def main() -> None:
    get_source_code(URl)


if __name__ == '__main__':
    main()
