"Main module."
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from alexa_crawler_utils import get_review,cate_crawl,vapp_cralwing
import re
import os
import json

driver = webdriver.Chrome()

overwrite = False # Overwrites existing files

#road map

#step 1:
#iterate through all existing categories

category = []
totalapp = 0
total_custom_permission = 0
total_default_permission = 0
logistic = {'totalapp':0,'total_custom_permission':0,'total_default_permission':0}

if os.path.exists('./result/metadata/logistic.json'):
    with open("./result/metadata/logistic.json", "r") as readfile:
        json_data = readfile.read()
        logistic = json.loads(json_data)
        print("./result/metadata/logistic.json, here is a snip")
        print(logistic)
    totalapp = logistic['totalapp']
    total_custom_permission = logistic['total_custom_permission']
    total_default_permission = logistic['total_default_permission']
if (not os.path.exists('cate.json')) or (overwrite):
    driver.get("https://www.amazon.com/alexa-skills/b?ie=UTF8&node=13727921011")
    driver.get("https://www.amazon.com/alexa-skills/b?ie=UTF8&node=13727921011")
    assert "Alexa" in driver.title
    wait = WebDriverWait(driver, 10)
    #for this portion of xpath filter, look for the class used by category in the index page of alexa skill(key word example: smart home, communication)
    category_raw = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//a[@class='a-color-base a-link-normal']")))
    for cate_raw in category_raw:
        cate_name = re.sub('\ |\?|\.|\!|\/|\;|\:', '', cate_raw.text)
        category.append({'name':cate_name,'url':cate_raw.get_attribute('href'),'completion':False})
        print(cate_raw.text)
        print(cate_raw.get_attribute('href'))
    
# Write the category and completion status to cate.json
    with open('cate.json', 'w') as outfile:
        json.dump(category, outfile)
        print("information stored at ./cate.json")

elif os.path.exists('cate.json') and overwrite == False:
    with open("cate.json", "r") as readfile:
        json_data = readfile.read()
        category = json.loads(json_data)
        print("cate.json loaded, here is a snip")
        print(category[0])

# Crawl the categoy list to get skill URLs. Each category will have a json file in /metadata.
for index in range(len(category)):
    crawl_happened = False
    if (not category[index]["completion"]):
        count = 0
        while not crawl_happened:
            category[index], totalapp = cate_crawl(category[index], totalapp, driver)
            crawl_happened = True

        logistic['totalapp'] = totalapp
    if crawl_happened:
        with open('cate.json', 'w') as outfile:
            json.dump(category, outfile)
            print("information stored at ./cate.json after crawling categories")
        with open('./result/metadata/logistic.json', 'w') as outfile:
            json.dump(logistic, outfile)
            print("logistic info stored at ./result/metadata/logistic.json")

#Crawl the skills written to metadata to get individual skill details

path = "./result/"
path_metadata = "./result/metadata/"

for index in range(len(category)):
    category[index]["all_app_crawled"] = False

crawl_anyway_cate = False # override completion values
crawl_anyway_app = False # override completion values

for cate_index in range(len(category)):
    if not category[cate_index]["all_app_crawled"] or crawl_anyway_cate:
        name = category[cate_index]['name']
        metadata_file_path = path_metadata + name + '_app.json'
        apps = []
        with open(metadata_file_path, "r") as readfile:
            json_data = readfile.read()
            print(metadata_file_path)
            apps = json.loads(json_data)
        if not os.path.exists(path + name):
            os.mkdir(path + name)
        for index in range(len(apps)):
            crawled = False
            if not apps[index]["completion"] or crawl_anyway_app:
                total_custom_permission,total_default_permission = vapp_cralwing(apps[index],name,total_custom_permission, total_default_permission, driver)
                logistic["total_custom_permission"] = total_custom_permission
                logistic["total_default_permission"] = total_default_permission
                crawled = True
            if crawled:
                with open(metadata_file_path, 'w') as outfile:
                    json.dump(apps, outfile)
                with open('./result/metadata/logistic.json', 'w') as outfile:
                    json.dump(logistic, outfile)
                    print("logistic info stored at ./result/metadata/logistic.json")
        category[cate_index]["all_app_crawled"] = True

driver.quit()