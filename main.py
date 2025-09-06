import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import itertools

# Set up ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Navigate to catalogue page
driver.get('https://www.hiflofiltro.com/catalogue')
time.sleep(5)

# Extract options
manufacturers = driver.find_elements(By.XPATH, '//select[@name="sel_manufacture"]/option')
start_index_manufacturer = 1
manufacturer_indices = list(range(start_index_manufacturer, len(manufacturers)))

types = driver.find_elements(By.XPATH, '//select[@name="sel_type"]/option')
start_index_type = 2
type_indices = list(range(start_index_type, len(types)))

ccs = driver.find_elements(By.XPATH, '//select[@name="sel_cc"]/option')
cc_indices = list(range(start_index_type, len(ccs)))

# Generate combinations
combinations = list(itertools.product(manufacturer_indices, type_indices))
print(f"Manufacturer options: {len(manufacturer_indices)}")
print(f"Type options: {len(type_indices)}")
print(f"CC options: {len(cc_indices)}")
print(f"Total combinations: {len(combinations)}")

# Initialize data storage
data = []

# Iterate over combinations
for combination in manufacturer_indices:
     selection_dict = {}
     # time.sleep(1)

     # Select manufacturer
     try:
          manufacturers = driver.find_elements(By.XPATH, '//select[@name="sel_manufacture"]/option')
          manufacturer_element = manufacturers[combination]
          selection_dict['Manufacturer'] = manufacturer_element.get_attribute('value')
          manufacturer_element.click()
          # time.sleep(1)
     except:
          pass

     # Select type
     try:
          types = driver.find_elements(By.XPATH, '//select[@name="sel_type"]/option')
          type_element = types[1]
          selection_dict['Type'] = type_element.get_attribute('value')
          type_element.click()
          # time.sleep(1)
     except:
          pass

     # Select CC
     try:
          ccs = driver.find_elements(By.XPATH, '//select[@name="sel_cc"]/option')
          cc_element = ccs[1]
          selection_dict['CC'] = cc_element.get_attribute('value')
          cc_element.click()
     except:
          pass

     # Click search button
     try:
          search_button = driver.find_element(By.XPATH, '//button[contains(text(), "Find Bikes")]')
          search_button.click()
     except:
          pass
     # time.sleep(1)
     try:
          # Extract model data
          model_elements = driver.find_elements(By.XPATH, '//div[@id="search-results"]//li//a')
          for model_element in model_elements:
               model_name = model_element.find_element(By.XPATH, './/span[@class="model"]').text
               model_dict = selection_dict.copy()
               model_dict['Model'] = model_name
               model_dict['Link'] = f"{model_element.get_attribute('href')}"
               data.append(model_dict)
     except:
          pass
     # time.sleep(1)


# Save data to JSON file
driver.quit()
with open('data_unf.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
