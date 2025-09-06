from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time

def setup_driver():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.hiflofiltro.com/catalogue#search-results')
    return driver

def select_dropdown_option(driver, dropdown_xpath, start_index=1):
    dropdown = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, dropdown_xpath))
    )
    return dropdown[start_index:]

def fetch_bike_results(driver):
     btn = WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Find Bikes")]'))
     )
     btn.click()
     time.sleep(2)
     result = []
     try:
          result = WebDriverWait(driver, 10).until(
          EC.visibility_of_all_elements_located((By.XPATH, '//div[@id="search-results"]//a')))
     except TimeoutException:
          pass

     return result

def fetch_parts(driver):
     result = []
     try:
          result =  WebDriverWait(driver, 10).until(
          EC.visibility_of_all_elements_located((By.XPATH, '//div[@class="part"]')))
     except TimeoutException:
          pass
     
     return result

def extract_filter_info(part, filter_type):
    filters = part.find_elements(By.XPATH, './/p/a')
    filter_info = ''
    if filters:
        for filter in filters:
            filter_info += f'\t{filter.text}'
    return filter_info

def main():
    driver = setup_driver()
    oil_filter_data = []
    air_filter_data = []

    manufacturers = select_dropdown_option(driver, '//select[@name="sel_manufacture"]/option')
    for manufacturer in manufacturers:
        bike_info = {'Manufacturer': manufacturer.get_attribute('value')}
        manufacturer.click()
        
        bike_types = select_dropdown_option(driver, '//select[@name="sel_type"]/option', start_index=2)
        for bike_type in bike_types:
            bike_info['Bike_Type'] = bike_type.get_attribute('value')
            bike_type.click()
            
            ccs = select_dropdown_option(driver, '//select[@name="sel_cc"]/option', start_index=2)
            for cc in ccs:
                bike_info['cc'] = cc.get_attribute('value')
                cc.click()
                
                results = fetch_bike_results(driver)
                if len(results)!=0:
                    for result in results:
                         model = result.find_element(By.XPATH, './/span[@class="model"]')
                         bike_info['Model'] = model.text
                         result.click()
                         
                         parts = fetch_parts(driver)
                         part1 = parts[0]
                         part2 = parts[1]
                         
                         oil_filter_info = extract_filter_info(part1, 'oil_filters')
                         if oil_filter_info:
                              oil_filter_data.append({**bike_info.copy(), 'oil_filters': oil_filter_info})
                         
                         air_filter_info = extract_filter_info(part2, 'air_filters')
                         if air_filter_info:
                             air_filter_data.append({**bike_info.copy(), 'air_filters': air_filter_info})
    
    with open('oil_filters.json', 'w', encoding='utf-8') as f:
        json.dump(oil_filter_data, f, indent=4)
    
    with open('air_filters.json', 'w', encoding='utf-8') as f:
        json.dump(air_filter_data, f, indent=4)
    
    driver.quit()

if __name__ == "__main__":
    main()