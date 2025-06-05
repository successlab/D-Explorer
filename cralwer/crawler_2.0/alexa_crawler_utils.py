from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
import os
import time
import json
import random


def ensure_nested_directory_structure(path):
    # Check if the directory structure exists, and create it if missing
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created nested directory structure: {path}")
    else:
        print(f"Nested directory structure already exists: {path}")


def get_review(url, driver):
	"""Get skill reviews. This function is not currently used, but should gather reviews from the skill's review page.
	Due to the overhead required, we did not use this function and it may no longer work. This function should return an array of json 
	files, each standing for a single review."""

	review_count = 0
	HasNext = True
	reviewdriver = driver
	result = []
	try:
		reviewdriver.get(url)
	except:
		reviewdriver.quit()
		return result
	while HasNext == True:
		wait = WebDriverWait(reviewdriver, 5)
		try:
			# Find a review. if none present, skip
			token = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'a-section review aok-relative')]")))
		except:
			reviewdriver.quit()
			return result
		soup=BeautifulSoup(reviewdriver.page_source, 'lxml')
		# find all the review boxes, and gather data.
		reviewboxes = soup.findAll("div", {"class": "a-section review aok-relative"})
		for reviewbox in reviewboxes:
			data = {}
			print((">>> review number : " + str(review_count)))
			reviewrate = reviewbox.find("span", {"class" : "a-icon-alt"}) # Rating
			data["rate"] = reviewrate.get_text().split("out",1)[0]
			reviewcontent = reviewbox.find("span", {"data-hook" : "review-body"}) # content
			data["content"] = reviewcontent.get_text()
			try:
				reviewscore = reviewbox.find("span", {"data-hook" : "helpful-vote-statement"}) # score (helpfulness)
				data["helpness"] = reviewscore.get_text().split("people",1)[0]
			except:
				data["helpness"] = str(0)
			result.append(data)
			review_count += 1
			time.sleep(0.2)
		try:
			# go to next page
			clicknext = reviewdriver.find_element("xpath","//*[@id='cm_cr-pagination_bar']/ul/li[2]")
			clicknext.click()
			print("try clicking")
		except:
			HasNext = False
	reviewdriver.quit()
	return result

def failed_vapp_cralwing(name, url, path):
	#save to a saperate file with link and cate info for later check
	try:
		print("empty vapp page")
		data = {}
		data['url'] = str(url)
		data['name'] = name
		data['info'] = "Crawling of this application is likely crushed"
		file_path = path+ str(name) +".json"
		aff= open(file_path,"w+")
		aff.write(str(data))
		aff.close()
	except:
		print("Failed")

def vapp_cralwing(vapp, cate, total_custom_permission, total_default_permission, driver):
	"""App crawler. We pass in the driver to prevent crawler protections from triggering."""

	#assume directory ./result/[category] is already created
	#total_customer_permission,total_default_permission,totalapp are for logistics

	name = vapp["name"]
	url = vapp["url"]

	subdriver = driver

	path = "./result/"
	path = path + str(cate) + '/'
	ensure_nested_directory_structure(path)
	time.sleep(0.1 * random.randint(1,10))
	subdriver.get(url)
	try:
		#collect information for screen print out and json file
		#detail_name is the name of the app
		print(url)
		# detail_name = subdriver.find_element(By.XPATH,"//div[contains(@class, 'sc-iMfspA sc-jgUSZD ghwsWj loUJYn')]").text # broken path
		detail_name = subdriver.find_element(By.XPATH,"//div[contains(@class, 'sc-jeGSBP sc-fkubWd flIjkX kGIvBK')]").text
		detail_name = re.sub(r'\ |\?|\.|\!|\/|\;|\:', '', detail_name)
		detail_publisher = subdriver.find_element(By.XPATH,"//div[contains(@class, 'sc-jeGSBP sc-fkubWd hSfqYU kGIvBK')]").text
		file_path = path+ str(detail_name) + "_" + str(url).split("/")[5] + ".json" # we split and unclude block 6 to get the string UUID.
		file_path = file_path[:255]

		if os.path.exists(file_path):
			vapp["completion"] = True
			raise Exception(file_path + ' already exist')
		if not os.path.exists(path):
			raise Exception(path + ' (directory)does not exist')
	except Exception as inst:
		print(inst)
		return total_custom_permission, total_default_permission
	try:
		appdata = {}
		appdata["url"] =  url
		print("now crawling " + detail_name)
		print(detail_publisher)
		appdata["publ"] = detail_publisher
		appdata["name"] = detail_name
		# find three voice commands
		utter_count = 0
		wait = WebDriverWait(subdriver, 5)
		tempel = subdriver.find_elements(By.XPATH, "//div[contains(@class, 'sc-kNPvCX fPAqvR')]") # voice commands
		print(tempel)
		for temp in tempel:
			print(('voice command: ' + str(utter_count)))
			print(temp.text)#utter_text
			appdata[str(utter_count)] = temp.text
			utter_count += 1
		# find rate
		try:
			wait = WebDriverWait(subdriver, 5)
			rate_text = wait.until(EC.presence_of_element_located((By.XPATH,  "//span[contains(@class,'a-size-medium a-color-base')]"))) # rating
			appdata["apprate"] = rate_text.text
			print(rate_text.text)
		except:
			print("NO rating")
			appdata["apprate"] = str(0)
		# find skill detail
		try:
			tempel = subdriver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[4]/ul') # skill detail pane
			text = ""
			for temp in tempel:
				text = text + temp.text
				print(temp.text)

			appdata["skdetail"] = text
		except:
			print("NO rating")
			appdata["skdetail"] = ""
		# reviewers number
		try:
			wait = WebDriverWait(subdriver, 5)
			review_num = wait.until(EC.presence_of_element_located((By.XPATH,  "//div[contains(@class,'sc-jeGSBP hWnrMh')]")))
			appdata["reviewnum"] = review_num.text
			print(review_num.text)
		except:
			print("no review number")
			appdata["reviewnum"] = str(0)
		# find description
		try:
			wait = WebDriverWait(subdriver, 5)
			desbox = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-eHfQar fpyVWQ')]")))
			#~ print desbox.text
			appdata["des"] = desbox.text
		except:
			print("[no] description")
			appdata["des"] = "N"
		try:
			tempel = subdriver.find_elements(By.XPATH, '//*[@id="__next"]/div/div[2]/div[5]/ul')
			text = ""
			for temp in tempel:
				text = text + temp.text
				print(temp.text)

			appdata["priv"] = text
		except:
			print("[no] privacy info")
			appdata["priv"] = "N"
	except:
		failed_vapp_cralwing(name,url,path)
		vapp["completion"] = True
		return total_custom_permission, total_default_permission
	# review. Disabled due to overhead
	# try:
	# 	review_page_url = review_num.find_element("xpath","//a[contains(@class,'sc-jfSnVq gBAEOU')]").get_attribute('href')
	# 	review_data = get_review(review_page_url)
	# 	appdata['review'] = review_data
	# except:
	# 	print("{error}\n no review")
	with open(file_path, 'w') as outfile:
		json.dump(appdata, outfile)
	vapp["completion"] = True
	return total_custom_permission, total_default_permission

def cate_crawl(cate, totalapp, driver):
	"""This function will:
	1. crawl the entire category
	2. store all skills under said category in a json file
	3. store said json file.

	cate : {'name':cate_name,'url':"www.xxx.xxx",'completion':False}
	"""

	subdriver = driver
	#login code, currently not necessary
	# subdriver = webdriver.Chrome(ChromeDriverManager().install(), options = chrome_options)
	# subdriver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Falexa-skills%2Fb%3Fie%3DUTF8%26node%3D13727921011%26ref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
	# subdriver.find_element("id","ap_email").send_keys(username)
	# subdriver.find_element("id","continue").click()
	# subdriver.find_element("id","ap_password").send_keys(password)
	# subdriver.find_element("id","signInSubmit").click()
	
	name = cate['name']
	url = cate['url']
	apps = []
	cate_page_count = 1
	print("now crawling category: " + name)
	subdriver.get(url)

	#jump to "all result" page
	# see_all_result = subdriver.find_element("xpath","//div[contains(@class, 'a-box a-text-center apb-browse-searchresults-footer')]")
	# see_all_result.click()

	path = "./result/metadata/"
	ensure_nested_directory_structure(path)
	file_path = path + name + '_app.json'
	#following codes extract the last page
	last_page = 1
	tempel = subdriver.find_elements(By.XPATH,'//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[18]/div/div/span/ul/span[3]')
	print(tempel)
	for tem in tempel:
		if tem.text.isnumeric():
			last_page = int(tem.text)
			break
	print(last_page)
	next_button = 3
	while cate_page_count < last_page:
		#retain token to make sure we got all our stuff
		wait = WebDriverWait(subdriver, 5)
		try:
			# This is looking for the skill panes in the category page.
			token = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class, 'sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')]")))

			soup = BeautifulSoup(subdriver.page_source, 'lxml')
			subelement = soup.find_all("div", class_="sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16")
			#noted, at this point subelement contain entire div box
			for subel in subelement:
				# initialize the checklist for each page
				# Find the link to the skill
				# print(subel.find("a",class_ = 'a-link-normal s-no-outline').get('href'))
				app_name = subel.find("h2",class_ = 'a-size-medium a-spacing-none a-color-base a-text-normal').get("aria-label")
				app_url = "https://www.amazon.com" + subel.find("a",class_ = 'a-link-normal s-no-outline').get('href')
				apps.append({"name":app_name,"url":app_url,"completion":False})
				totalapp += 1
			print(("total number of app crawled: " + str(len(apps))))
			try:
				# find the next page. Sometimes this doesn't work immediately, give it time.
				nextButton = subdriver.find_element("xpath","//a[contains(@class,'s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator')]")
				print(nextButton.text)
				nextButton.click()
				#subdriver.get(nextlink)
				next_button += 1
				cate_page_count += 1
				print(cate_page_count)
			except:
				print("<< no next page >>")
				print("finish crawling following category:" + name)
				print(cate_page_count)
				print(last_page)
		except TimeoutException:
			print("<< Cannot find apps >>")
			print(last_page)
			print(cate_page_count)
	with open(file_path, 'w') as outfile:
		json.dump(apps, outfile)
		print("information stored at " + file_path)
	cate["completion"] = True
	return cate, totalapp
