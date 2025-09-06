import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

data_str = ''
with open('data_unf.json', 'r', encoding='utf-8') as f:
     data_str = f.read()

data = json.loads(data_str)
oil_filters = []
air_filters = []
for row in data[:100]:
     dict1 = row
     dict2 = row
     driver.get(row['Link'])
     time.sleep(1)
     try:
          parts = driver.find_elements(By.XPATH, '//div[@class="part"]')
          time.sleep(1)
          if len(parts)!=0:
               for part in parts:
                    if 'oil' in part.find_element(By.XPATH, './/h3').text.lower():
                         time.sleep(1)
                         pns = part.find_elements(By.XPATH, './/p//a')
                         for p in pns:
                              dict1['Oil_filter'] = dict1.get('Oil_filter', '') + p.text + '\n'
                         oil_filters.append(dict1)
                    if 'air' in part.find_element(By.XPATH, './/h3').text.lower():
                         time.sleep(1)
                         pns = part.find_elements(By.XPATH, './/p//a')
                         for p in pns:
                              dict2['Air_filter'] = dict2.get('Air_filter', '') + p.text + '\n'
                         air_filters.append(dict2)
                              
     except:
          pass

oil_filters_str = json.dumps(oil_filters)
air_filters_str = json.dumps(air_filters)

with open('oil_filters.json', 'w', encoding='utf-8') as f:
     f.write(oil_filters_str)

with open('air_filters.json', 'w', encoding='utf-8') as f:
     f.write(air_filters_str)