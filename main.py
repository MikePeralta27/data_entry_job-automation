from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import requests
from bs4 import BeautifulSoup
from pprint import pprint

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

form_link = ("https://docs.google.com/forms/d/e/1FAIpQLScVr17_ymMyx-mUBT_P4Cnt5nN5oXcTl8-bIJ-kBwEmsPCBew/viewform?usp"
             "=sf_link")
zillow_link = ("https://appbrewery.github.io/Zillow-Clone/")

price_selector = "li div.StyledPropertyCardDataArea-fDSTNn"
link_selector = "li a.StyledPropertyCardDataArea-anchor"


class DataEntryJob:
    def __init__(self):
        self.driver = webdriver.Chrome(chrome_options)

    def get_property_data(self):
        response = requests.get(zillow_link)
        zillow_html = response.text
        soup = BeautifulSoup(zillow_html, "html.parser")

        properties_links_tag = soup.select(selector='a.StyledPropertyCardDataArea-anchor')
        property_prices_tag = soup.select(selector='[data-test="property-card-price"]')
        property_addresses_tag = soup.select(selector='[data-test="property-card-addr"]')

        property_link_list = [prop.get('href') for prop in properties_links_tag]
        property_price_list = [prop.getText().split("+")[0].strip("$/mo") for prop in property_prices_tag]
        property_addresses = [prop.getText().strip("\n ") for prop in property_addresses_tag]

        print(property_price_list)
        print(property_addresses)
        print(property_link_list)

        property_data = []

        for item in range(len(property_price_list) - 1):
            property_dict = {"link": property_link_list[item], "address": property_addresses[item],
                             "price": property_price_list[item]}

            property_data.append(property_dict)

        pprint(property_data)
        return property_data

    def fill_property_from(self, property_data):

        for property in property_data:
            self.driver.get(form_link)
            property_link = property['link']
            property_address = property['address']
            property_price = property['price']
            time.sleep(4)
            form_price_textbox = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                          '1]/div/div/div[2]/div/div[1]/div/div['
                                                                          '1]/input')
            from_link_textbox = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                         '2]/div/div/div[2]/div/div[1]/div/div['
                                                                         '1]/input')
            form_address_textbox = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div['
                                                                            '3]/div/div/div[2]/div/div[1]/div/div['
                                                                            '1]/input')
            form_submit_button = self.driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div['
                                                                          '1]/div[1]/div')
            form_price_textbox.send_keys(property_price)
            time.sleep(2)
            from_link_textbox.send_keys(property_link)
            time.sleep(2)
            form_address_textbox.send_keys(property_address)
            time.sleep(2)
            form_submit_button.click()


data_entry = DataEntryJob()

data = data_entry.get_property_data()
data_entry.fill_property_from(data)
