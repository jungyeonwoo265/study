from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("C:/Users/Kiot/PycharmProjects/chromedriver_win32/chromedriver.exe")
driver.implicitly_wait(3)
driver.get("https://map.naver.com/")

search = driver.find_element(By.CLASS_NAME, 'input_search')
search.send_keys("스타벅스")
search.send_keys(Keys.ENTER)
