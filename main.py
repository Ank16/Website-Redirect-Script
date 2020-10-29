from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
import time
import pandas as pd
import openpyxl
import re

#open data and create dataframe
df = pd.read_csv("data.csv")

#set path to chrome driver and open website
PATH = "chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://redirectdetective.com/")

time.sleep(1)

#create error log list
errorLog = ["Websites with errors:\n"]

#loop through every webpage in dataframe
for webpage in df['WebPage']:
	try:
		#create empty variable for results
		webpage_str = ""

		#clcik on Display redirects in full and search for webpage
		displayButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home-section"]/main/section/div[1]/form/div[2]/label/div/i')))
		displayButton.click()
		search = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'word')))
		search.send_keys(webpage)
		search.send_keys(Keys.RETURN)

		time.sleep(2)

		#find all links on page
		elems = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="result"]//*[contains(@type,"button")]')))

		time.sleep(2)

		#loop through links to fins actual results and add to results variable
		for elem in elems:
			#print(elem.text)
			txt = elem.text
			webpage_str += txt + ", "	

		#add results to dataframe
		data = [[webpage, webpage_str]]
		df2 = pd.DataFrame(data, columns = ['WebPage', 'Redirect'])
		df = df.append(df2, ignore_index=False)
		
		#refresh page
		driver.refresh()

		time.sleep(2)

	#handle exception
	except Exception:
		#prints eroor message
		print("There was an error for the website: " + webpage)
		#adds error to error log list
		errorLog.append(webpage + "\n")
		data2 = [[webpage, "There was an error"]]
		df3 = pd.DataFrame(data2, columns = ['WebPage', 'Redirect'])
		df = df.append(df3, ignore_index=False)
		#refresh page
		driver.refresh()
		#restart loop
		continue

#write error log list to error log file
logFile = open('error-log.txt', 'w')
logFile.writelines(errorLog)

#remove original empty data
df = df.dropna()
#print results
print(df)

#export results to excel and csv file
df.to_excel('result.xlsx')
df.to_csv('result.csv', index=False)

#close browser
driver.quit()