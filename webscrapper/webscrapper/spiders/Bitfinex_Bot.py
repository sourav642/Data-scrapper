# -*- coding: utf-8 -*-
import scrapy
import csv
from os import path
import datetime
from selenium import webdriver as wd
from selenium.webdriver.chrome.options import Options
import time


def csv_output(spyder_name, dic):
        file_name = "%s.csv"%(spyder_name)
        if not path.exists(file_name):
            with open(file_name,'a+',newline='') as csv_file:
                writer=csv.writer(csv_file)
                writer.writerow(dic.keys())
        with open(file_name,'a+',newline='') as csv_file:
            writer=csv.writer(csv_file)
            writer.writerow(dic.values())




class BitfinexBotSpider(scrapy.Spider):
    name = 'Bitfinex_Bot'
    allowed_domains = ['www.bitfinex.com/']
    start_urls = ['https://www.bitfinex.com']
    
    def __init__(self):
        options = Options()
        options.set_headless(headless=True)
        #options.add_argument('--disable-gpu')
        options.add_argument('window-size=1920x1080')
        self.driver =wd.Chrome("E:/chromedriver.exe",chrome_options=options)


    def parse(self, response):
        self.driver.implicitly_wait(15)
        self.driver.get(response.url);
        time.sleep(5)
        result=dict()
        i=0
        while self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[2]').text != "BCHUSD":
            i+=1
        result['Datetime']=datetime.datetime.now()

        result['Last Current price']=self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[3]').text

        result['24 Hr Price Change']=self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[4]').text

        result['24 Hr High Price']=self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[5]').text

        result['24 Hr Low Price']= self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[6]').text

        result['24 Hr Volume']= self.driver.find_element_by_xpath('//*[@id="fav-ticker-list-table"]/tbody/tr['+str(i+1)+']/td[7]/span/span[1]').text

        result['Coins']= "Bitcoin Cash"#self.driver.find_element_by_xpath('').text

        result['Base Currency']=self.driver.find_element_by_xpath('//*[@id="tickers-landing-container"]/div/div/div[1]/div[2]').text

        result['Exchanges URL']=response.url

        result['Exchanges']="Bitfinex"

        csv_output(self.name, result)
  