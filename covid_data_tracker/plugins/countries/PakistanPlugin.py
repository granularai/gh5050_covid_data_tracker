import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from covid_data_tracker.plugins.base import BasePlugin

class PakistanPlugin(BasePlugin):

    COUNTRY = "Pakistan"
    # BASE_SOURCE = "http://covid.gov.pk/stats/pakistan"
    BASE_SOURCE = "https://datastudio.google.com/embed/reporting/1PLVi5amcc_R5Gh928gTE8-8r8-fLXJQF/page/R24IB"
    TYPE = "Dashboard: Google Data Studio"

    def fetch(self):
        pass
        # driver = webdriver.Chrome(executable_path='./bin/chromedriver_mac')
        # driver.implicitly_wait(15)
        # driver.get("https://datastudio.google.com/embed/reporting/1PLVi5amcc_R5Gh928gTE8-8r8-fLXJQF/page/R24IB")
        #
        # while True:
        #     counter = 1
        #     try:
        #         if counter <= 10:
        #             print('resolving dashbooard.')
        #             self.absolute_cases = driver.find_element_by_xpath('//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[74]/div/div/div[1]/div/div/kpimetric/div/div[2]')
        #             self.absolute_deaths = driver.find_element_by_xpath('//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[109]/div/div/div[1]/div/div/kpimetric/div/div[2]')
        #             # deceased_10_f = driver.find_element_by_xpath('//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[57]/div/div/div[1]/div/gviz-barchart/div/div[1]/div/svg/g[2]/g[4]/g[18]/g/text')
        #             # deceased_10_m = driver.find_element_by_xpath('//*[@id="body"]/div/div/div[1]/div[2]/div/div[1]/div[1]/div[1]/div/lego-report/lego-canvas-container/div/file-drop-zone/span/content-section/canvas-component[57]/div/div/div[1]/div/gviz-barchart/div/div[1]/div/svg/g[2]/g[4]/g[9]/g/text')
        #             print(self.absolute_cases)
        #             print(self.absolute_deaths)
        #             print(deceased_10_f)
        #             print(deceased_10_m)
        #             # deceased_20_f = driver.find_element_by_xpath('')
        #             # deceased_20_m = driver.find_element_by_xpath('')
        #             # deceased_30_f = driver.find_element_by_xpath('')
        #             # deceased_40_m = driver.find_element_by_xpath('')
        #             break
        #     except Exception as e:
        #         counter += 1
        #         print(e)
