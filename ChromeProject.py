import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
import smtplib
import datetime
import xlrd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import urllib
import os
from selenium.webdriver.firefox.options import Options



#wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb

twosecSleep = 2
fivesecSleep = 5
tensecSleep = 10
twominSleep = 120
twohourSleep = 7200
playStoreURL=r'https://play.google.com/store'
playStoreSearch=r'https://play.google.com/store/search?q='
recoveryOptionsString2 = r'myaccount'
verify2String = 'https://accounts.google.com'
signIDbutton = r'gb_70'
resultsClassname = r'poRVub'
identifierIDbutton = r'identifierId'
searchIDbutton = 'gbqfq'
hardpassword = r'vip5vip5'
recoveryOptionsString = r'recovery-options-collection'
outputName = r'reviewdb.xlsx'
installButtonxpath4 = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div/c-wiz/c-wiz/div/span/button'
installButtonxpath3 = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div/c-wiz/c-wiz/div/span/button'
installButtonxpath2 = r'//*[@id="fcxH9b"]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div[2]/c-wiz/c-wiz/div/span/button'
installButtonxpath = r'/html/body/div[1]/div[4]/c-wiz[3]/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div/c-wiz/c-wiz/div/span/button'
installButtonxpath5 = r'//*[@id="fcxH9b"]/div[4]/c-wiz[3]/div/div[2]/div/div[1]/div/c-wiz[1]/c-wiz[1]/div/div[2]/div/div[2]/div/div[2]/div/c-wiz/c-wiz/div/span/button'
reviewAlreadyWrittenxpath=r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/c-wiz/div/div[2]/div/div[2]/div[1]/div[2]/div/div[2]/span/span/span'
reviewButtonxpath = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[1]/span/button'
reviewButtonxpath2 = r'/html/body/div[1]/div[4]/c-wiz[2]/div/div[2]/div/div[1]/div/div/div[1]/div[1]/span/button'
nodeviceString = r'You don\'t have any devices'
nodeviceString2 = r'remote_install_error'
uploadfileCommand =  r'curl -u sugarderryfire:bit5bit5 -X POST https://api.bitbucket.org/2.0/repositories/sugarderryfire/reviewsproject/src/ -F reviewdb.xlsx=@reviewdb.xlsx'
#uploadfileCommand1 = r'curl -u '
#uploadfileCommand2 = r' -X POST https://api.bitbucket.org/2.0/repositories/sugarderryfire/reviewsproject/src/ -F '
bitpass = r'vip5vip5'
fullFilenameDB = r'https://bitbucket.org/sugarderryfire/reviewsproject/raw/master/reviewdb.xlsx'
#bitbucket upload a file command - #curl -u sugarderryfire:bit5bit5 -X POST https://api.bitbucket.org/2.0/repositories/sugarderryfire/reviewsproject/src/ -F reviewdb.xlsx=@reviewdb.xlsx
outputFileName="reviewdb.xlsx"
settingsIDButton = "settings"  # the id string of the settings button.
usernameAuth = "admin"  # configuration details for the mobile wifi.
passwordAuth = "admin123" #configuration details for the mobile wifi.
rebootPageurl = "http://192.168.8.1/html/reboot.html"
rebootFirstApplyButtonID = "undefined"
rebootPopupConfirmButtonID = "pop_confirm"
time2Reboot = 45
mobileWIFIurl = "http://192.168.8.1/"  # the url of the mobile wifi device.
settingsIDButton = "settings"  # the id string of the settings button.
usernameInputButtonID = "username"  # the id string of the username input button.
passwordInputButtonID = "password"  # the id string of the password input button.
usernameAuth = "admin"  # configuration details for the mobile wifi.
passwordAuth = "admin123" #configuration details for the mobile wifi.
rebootPageurl = "http://192.168.8.1/html/reboot.html"
rebootFirstApplyButtonID = "undefined"
rebootPopupConfirmButtonID = "pop_confirm"
fullappurl = r'https://play.google.com/store/apps/details?id='


def SendEmail(msg):
	try:
		mailFrom="sugarderryfire@gmail.com"
		mailTO="sugarderryfire@gmail.com"
		passLogin="sugderfir5sugderfir5"
		server=smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(mailFrom,passLogin)
		server.sendmail(mailFrom,mailTO,msg)
		server.quit()
	except Exception as e:
		#print(e)
		print ("Failed to send email")


def readDB():
	try:
		df = pd.read_excel(fullFilenameDB, sheet_name='Sheet1')  # open the db
		if(df is not None):
			IDlist=df['appid']
			keywordsList = df['keyword']
			emailList = df['email']
			recoveryList = df['recovery']
			timeList = df['time']
			reviewList = df['review']
			doneList = df['done']
			return IDlist, keywordsList, emailList, recoveryList, timeList, reviewList, doneList
		else:
			SendEmail("Object is null - check your internet connectivity")
			exit()
	except Exception as e:
		print(e)
		SendEmail("Problem with excel review file or with internet")
		exit()




# check if review has been already written. compare inputdb with outputdb.
def checkReviewAudit(email2check, appid):
	df = pd.read_excel(fullFilenameDB, sheet_name='Sheet1')  # open the db
	emailList = df['email']
	IDlist = df['appid']
	for index, currEmail in enumerate(emailList):
		if email2check == currEmail:
			if appid == IDlist[index]:
				return False  # the email and the app id already exist.
	return True  # the email and app id does not exist - can write a review.


def loadMoreResults(browser,pages):
	for i in range(1,pages):
		jumpDown(browser)
		time.sleep(3)


def jumpDown(browser):
	browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def jumpUp(browser):
	browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")


#check if it is time to post a new review. (every review has its time to post.)
def checkTime(time):
	gettimestring=time.split()
	getdate=gettimestring[0]  # get the date in string
	gettime=gettimestring[1]  # get the time in string
	timeCurr=gettime.split(":")  # get the time split
	hour=int(timeCurr[0])
	mins=int(timeCurr[1])
	ddate=getdate.split("/")  #get the date split
	day=int(ddate[0])
	month=int(ddate[1])
	year=int(ddate[2])
	datetimeCurr=datetime.datetime(year, month, day, hour, mins)
	currentDT = datetime.datetime.now()
	if(currentDT > datetimeCurr):  # if review can be published
		return True
	else:
		return False



def confirmEmail(browser, currentEmail, currentRecovery):
	try:
		confirmButton = browser.find_elements_by_class_name('vxx8jf')   # last id - vdE7Oc; ; INl6Jd
		confirmButton[-2].click()  # click on email verification button.
		time.sleep(2)
		inputButton = browser.find_element_by_id('knowledge-preregistered-email-response')  # last id - ; identifierId
		inputButton.send_keys(currentRecovery)
		inputButton.send_keys(Keys.RETURN)  # send email verification string.
		pageURL = browser.current_url
		if (verify3String in pageURL):  # skip the verifying page
			actions = ActionChains(browser)
			actions.send_keys(Keys.TAB * 2)
			actions.send_keys(Keys.ENTER)
			actions.perform()
	except: # if something went wrong
		SendEmail("cant confirm recovery email " + currentEmail)  # send email


def checkRecoveryRequest(browser, currEmail, currentRecovery):
	try:
		confirmEmail(browser, currEmail, currentRecovery)
	except: # if something went wrong
		SendEmail("cant confirm recovery request email ")  # send email




def checkRecoveryOptionsURL(browser):
	get_url=browser.current_url
	if(recoveryOptionsString2 in get_url):
		browser.get(playStoreURL)
		#ALTTABFUNC(browser)
		return True
	return False



#this function just do one tab press and one enter press to skip the recovery options update of google play. and then refresh the page for starting over.
def ALTTABFUNC(browser):
	actions = ActionChains(browser)
	actions.send_keys(Keys.TAB)
	actions.send_keys(Keys.TAB)
	actions.perform()
	actions.send_keys(Keys.SPACE).perform()
	actions.reset_actions()
	time.sleep(fivesecSleep)
	browser.refresh()
	time.sleep(fivesecSleep)



def signin(browser, currEmail):
	print("trying to signin")
	signinButton = browser.find_element_by_id(signIDbutton)
	signinButton.click()  # click on sign in
	time.sleep(8)
	identifierInput = browser.find_element_by_id(identifierIDbutton)
	identifierInput.send_keys(currEmail)
	identifierInput.send_keys(Keys.RETURN)  # enter password and continue.
	time.sleep(4)
	#inputs = browser.find_elements_by_tag_name('input')
	#passwordInput = inputs[2]
	passwordInput = browser.find_element_by_name('password')
	passwordInput.send_keys(hardpassword)  # enter password
	passwordInput.send_keys(Keys.RETURN)
	time.sleep(6)
	print("you are log in")


def FindDeviceExist(browser, currEmail):
	htmlSource = browser.page_source
	if(nodeviceString in htmlSource or nodeviceString2 in htmlSource):
		SendEmail("No devices Found" + currEmail)
		return False
	return True



# try to click parent tag and pparent
def clickParent(browser,childTag):
	try:
		parentTag=childTag.find_element_by_xpath('..')
		parentTag.click()
		return True
	except:
		try:
			parentTag=childTag.find_element_by_xpath('..')
			parentTag.click()
		except:
			print ("cant click on the link. exit")
			SendEmail("cant click on the link. exit")   #send email and quit.
	return False

def goDirectly(browser, appid):
	directappurl = fullappurl + str(appid)
	browser.get(directappurl)
	time.sleep(twosecSleep)

def goDirectlyInstall(browser, url):
	browser.get(url)
	time.sleep(fivesecSleep)

#search the current app id in the results.
def searchapp(browser, key, appid):
	time.sleep(8)
	search=browser.find_element_by_id(searchIDbutton)
	search.send_keys(key)
	search.send_keys(Keys.RETURN)
	time.sleep(tensecSleep)
	loadMoreResults(browser, 5)
	results = browser.find_elements_by_class_name(resultsClassname)
	appExists=False
	for res in results:
		href = res.get_attribute("href")
		if appid in href:
			appExists=True
			try:
				res.click()  # click on the app
			except Exception as e:
				print(e)
				clickParent(browser, res)  # try to click parent tag and pparent
			# after the click
			time.sleep(2)
	if not appExists:
		goDirectly(browser, appid)
		return True
	return appExists


def auditReviewDone(outputName, appid, email, key, currReview):
	sitesResultsCounter=0
	dframe = pd.read_excel(outputName)
	sitesResultsCounter=len(dframe)+1
	currentTime = str(datetime.datetime.now())
	dic={'Review': [currReview], 'currentTime': [currentTime], 'AppID': [appid], 'AccountID': [email]}
	#df = pd.DataFrame({appid: [], currentTime: [], email: [], currReview: []})  # construct the record to write to excel if a click happened. # keyword,site,pageCounter
	df = pd.DataFrame(dic)
	writer = pd.ExcelWriter(outputName)  # write to the given excel file
	dframe.to_excel(writer, 'Sheet1', index=False)  # writing the existing content
	df.to_excel(writer, 'Sheet1', index=False, startrow=sitesResultsCounter, header=False)  # write to a specific sheet in the excel file.
	writer.save()  # save the changes


def ChangeCellExcel(rowIndex,colName, newValue):
	dframe = pd.read_excel(outputName)
	dframe.iloc[rowIndex,dframe.columns.get_loc(colName)]=newValue
	writer = pd.ExcelWriter(outputName)  # write to the given excel file
	dframe.to_excel(writer, 'Sheet1', index=False)  # writing the existing content
	writer.save()  # save the changes


def validateInstall2(browser):
	try:
		ReviewButton=browser.find_element_by_xpath(reviewButtonxpath)
		return True
	except NoSuchElementException:
		try:
			ReviewButton = browser.find_element_by_xpath(reviewButtonxpath2)
		except NoSuchElementException:
			return False
	return False


def BuildInstallURL(appid):
	fullInstallURL= r'https://play.google.com/store/apps/details?id=' + appid + '&rdid=' + appid + '&feature=md&offerId'
	return fullInstallURL


#https://accounts.google.com/signin/v2/sl/pwd?service=googleplay&authuser=0&hl=iw&rart=ANgoxccnaCMNTEZpOWXgp0cjyHkPwxqnEcgBFkgbVFs8E7j1XUEcCFxZR7Ojt1eFezTABe2wGtw12SgIScrCTt2XKNtxEvL-_A&continue=https%3A%2F%2Fplay.google.com%2Fweb%2Fstore%2Fapps%2Fdetails%3Fid%3Dblock.chain.technology%26raii%3Dblock.chain.technology%26raboi%3DCAE%253D&iar=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin
#https://accounts.google.com/signin/v2/sl/pwd?service=googleplay&authuser=0&hl=iw&rart=ANgoxcfcDbh8Xt7DfHtogPi_6Xwd-07BIpYFLcYQOSFiZvioZ0WF3PdrAzmzwgFRIpRS9m7eE22LB4L-ERDgkj325jeQxNpslw&continue=https%3A%2F%2Fplay.google.com%2Fweb%2Fstore%2Fapps%2Fdetails%3Fid%3Dcom.Seriously.Phoenix%26raii%3Dcom.Seriously.Phoenix%26raboi%3DCAE%253D&iar=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin


def installapp(browser, appid, currEmail):
	try:
		installButton=browser.find_element_by_xpath(installButtonxpath)
		installButton.click()
		time.sleep(tensecSleep)
		return True
	except NoSuchElementException:  # no mobile attached or already installed
		return InstallAppXpath2(browser, currEmail)
	except:
		goDirectlyInstall(browser,BuildInstallURL(appid))  # if cant click the button so install directly
		#return clickParent(browser, installButton)
	return False

#copy of installapp function just with different xpath button.
def InstallAppXpath2(browser, currEmail):
	try:
		installButton=browser.find_element_by_xpath(installButtonxpath2)
		installButton.click()
		time.sleep(tensecSleep)
		return True
	except NoSuchElementException:  # no mobile attached or already installed
		SendEmail("cant click on install button - no mobile or already installed." + currEmail)  # send email.
		return InstallAppXpath3(browser, currEmail)
	except:
		return clickParent(browser, installButton)
	return False


#copy of installapp function just with different xpath button.
def InstallAppXpath3(browser, currEmail):
	try:
		installButton=browser.find_element_by_xpath(installButtonxpath3)
		installButton.click()
		time.sleep(tensecSleep)
		return True
	except NoSuchElementException:  # no mobile attached or already installed
		SendEmail("cant click on install button - no mobile or already installed." + currEmail)  # send email.
		return InstallAppXpath4(browser, currEmail)
	except:
		return clickParent(browser, installButton)
	return False


#copy of installapp function just with different xpath button.
def InstallAppXpath4(browser, currEmail):
	try:
		installButton=browser.find_element_by_xpath(installButtonxpath4)
		installButton.click()
		time.sleep(tensecSleep)
		return True
	except NoSuchElementException:  # no mobile attached or already installed
		SendEmail("cant click on install button - no mobile or already installed." + currEmail)  # send email.
		return InstallAppXpath5(browser, currEmail)
	except:
		return clickParent(browser, installButton)
	return False



#copy of installapp function just with different xpath button.
def InstallAppXpath5(browser, currEmail):
	try:
		installButton=browser.find_element_by_xpath(installButtonxpath5)
		installButton.click()
		time.sleep(tensecSleep)
		return True
	except NoSuchElementException:  # no mobile attached or already installed
		SendEmail("cant click on install button - no mobile or already installed." + currEmail)  # send email.
	except:
		return clickParent(browser, installButton)
	return False


def ReviewAlreadyIN(browser, currEmail, currReview):
	htmlSource = browser.page_source
	if(currReview in htmlSource):
		return True
	else:
		try:
			browser.find_element_by_xpath(reviewAlreadyWrittenxpath)
			return True
		except NoSuchElementException:  # if not review element - return false
			return False



def readOutputDB():
	df = pd.read_excel(outputName, sheet_name='Sheet1')  # open the db
	IDlist = df['AppID']
	emailList = df['AccountID']
	return emailList, IDlist



# check if review has been already written. compare inputdb with outputdb.
def checkReviewAudit(email2check, appid):
	emailList, IDlist=readOutputDB()
	for index, currEmail in enumerate(emailList):
		if email2check == currEmail:
			if appid == IDlist[index]:
				return False  # the email and the app id already exist.
	return True  # the email and app id does not exist - can write a review.



def InstallPopup2(browser):
	try:
		time.sleep(twosecSleep*5)
		actions = ActionChains(browser)
		#actions.send_keys(Keys.TAB * 2)  # firefox need this command. chrome does not.
		actions.send_keys(Keys.SPACE)
		actions.perform()
		#browser.refresh()
		actions.reset_actions()
		return True
	except:
		SendEmail("cant click on install popup button.")
		return False


def SendPass(browser):
	passwordInput = browser.find_element_by_name('password')
	#passwordInput = inputs[0]
	passwordInput.send_keys(hardpassword)  # enter password
	passwordInput.send_keys(Keys.RETURN)
	time.sleep(fivesecSleep)


def findReviewButton(browser):
	try:
		ReviewButton=browser.find_element_by_xpath(reviewButtonxpath)
		ReviewButton.click()
		return True
	except NoSuchElementException:
		try:
			ReviewButton = browser.find_element_by_xpath(reviewButtonxpath2)
			ReviewButton.click()
		except NoSuchElementException:
			SendEmail("cant click on review button. exit")  # send email and quit.
			time.sleep(twominSleep)
	except:
		clickParent(ReviewButton)
	time.sleep(20)
	return False


def firstReviewConfirm(browser):
	time.sleep(tensecSleep/2)
	actions = ActionChains(browser)
	actions.send_keys(Keys.TAB)
	actions.send_keys(Keys.ENTER)
	actions.perform()
	actions.reset_actions()
	return True


def writeReview2(browser, currentReview):
	actions = ActionChains(browser)
	#actions.send_keys(Keys.TAB)  # GO TO review text-area
	actions.send_keys(currentReview)
	actions.perform()
	#actions.reset_actions()
	print (currentReview)


def writeReview(browser, currentReview):
	actions = ActionChains(browser)
	#actions.reset_actions()
	time.sleep(fivesecSleep)
	#actions.send_keys(Keys.TAB)  # GO TO review text-area
	time.sleep(twosecSleep)
	for i in range(len(currentReview)):
		actions.send_keys(currentReview[i])
	actions.send_keys(Keys.SPACE)
	actions.perform()
	time.sleep(twosecSleep)
	#actions.reset_actions()
	pressStar(browser)
	print (currentReview)


def pressStar(browser):
	time.sleep(tensecSleep)
	actions = ActionChains(browser)
	actions.reset_actions()
	actions.send_keys(Keys.TAB)
	actions.send_keys(Keys.ARROW_DOWN)
	actions.send_keys(Keys.ARROW_DOWN)
	actions.send_keys(Keys.ARROW_DOWN)
	actions.send_keys(Keys.ARROW_DOWN)
	#actions.send_keys(Keys.ARROW_DOWN)
	actions.send_keys(Keys.SPACE)
	actions.perform()
	actions.reset_actions()


def pressSubmit(browser):
	actions = ActionChains(browser)
	actions.send_keys(Keys.TAB)
	actions.send_keys(Keys.TAB)
	actions.send_keys(Keys.ENTER)
	actions.perform()
	actions.reset_actions()
	return True


def ChangeCellExcel(rowIndex,colName, newValue):
	global outputFileName
	#outputName = r'reviewdb.xlsx'
	dframe = pd.read_excel(fullFilenameDB)
	dframe.iloc[rowIndex,dframe.columns.get_loc(colName)]=newValue
	writer = pd.ExcelWriter(outputFileName)  # write to the given excel file
	dframe.to_excel(writer, 'Sheet1', index=False)  # writing the existing content
	writer.save()  # save the changes


def bit_upload():
	os.system(uploadfileCommand)


def downloadFiletoLocalDB(urlFileName):
	urllib.urlretrieve(urlFileName, outputFileName)


def AuditReviewBitbucket(urlFileName, rowIndex, colName, newValue):
	print("auditreview")
	downloadFiletoLocalDB(urlFileName)  # download the file from DB and save it in local current directory
	ChangeCellExcel(rowIndex, colName, newValue)  # change cell of auditing review and save the file
	bit_upload()  # upload the new file to bitbucket.


def changeIP(browser):
	if browser is not None:
		browser.execute_script("window.open('');") # open a new tab.
		Window_List = browser.window_handles # get list of all open tabs
		browser.switch_to_window(Window_List[-1]) #move to the next tab.
		browser.get(mobileWIFIurl)  # go to the mobile wifi url - to change ip.
		pageSource=browser.page_source # get the page source of the page
		settingsLink=browser.find_element_by_id(settingsIDButton) # get the link of the settings button
		settingsLink.click()
		settingsLink.click()
		Window_List = browser.window_handles # get list of all open tabs again
		browser.switch_to_window(Window_List[-1]) #move to the pop up window.
		userNameInput=browser.find_element_by_id(usernameInputButtonID) # get the username input button of the popup authentication window.
		userNameInput.send_keys(usernameAuth)   # send username string to the input button.
		passwordInput=browser.find_element_by_id(passwordInputButtonID) # get the password input button of the popup authenticated window
		passwordInput.send_keys(passwordAuth)   #send password string to the input button.
		passwordInput.send_keys(Keys.RETURN)    # hit RETURN
		time.sleep(5)  # sleep a little bit for the authentication to affect.
		browser.get(rebootPageurl)  # go to the reboot page
		rebootFirstButton=browser.find_element_by_id(rebootFirstApplyButtonID) # get the reboot button
		time.sleep(2)
		rebootFirstButton.click()
		Window_List = browser.window_handles  # get list of all open tabs again
		browser.switch_to_window(Window_List[-1]) #move to the pop up window.
		rebootconfirmButton=browser.find_element_by_id(rebootPopupConfirmButtonID) # get the reboot popup window confirm button
		rebootconfirmButton.click()
		time.sleep(time2Reboot)  # sleep 45 seconds - elapsed time to reboot
		browser.close()  # close the current tab.
		browser.quit()


def browse(browser, appid, key,currEmail, currRecovery, reviewTime,currReview):
	browser.set_page_load_timeout(210)  # set a timeout for each page - if we need to wait more than 30 seconds - we want to proceed to other pages.
	browser.get(playStoreURL)
	print("the page is on")
	time.sleep(10)
	retValSubmit=False
	signin(browser, currEmail)  # signing in
	time.sleep(twosecSleep)
	pageURL = browser.current_url
	if (verify2String in pageURL):
		checkRecoveryRequest(browser, currEmail, currRecovery)
		checkRecoveryOptionsURL(browser) # this function has not been checked by developer
	if (searchapp(browser, key, appid)):  # search the current app id; no need else {} structure.
		if (FindDeviceExist(browser, currEmail)):
			if (not ReviewAlreadyIN(browser, currEmail, currReview)):  # if review is not in the page already.
				appurl = browser.current_url  # get current url
				if (not validateInstall2(browser)):  # check if already installed - returns true if already installed.
					installapp(browser, appid, currEmail) # try to install the app
					time.sleep(fivesecSleep)
					retValInstallpop = InstallPopup2(browser)  # click on the install button popup
					time.sleep(twosecSleep*3)
					if (verify2String in browser.current_url or "signin" in browser.current_url):
						SendPass(browser)
				#check if app has already been reviewed.
				time.sleep(twosecSleep*2)
				browser.refresh()
				reviewAnswer = findReviewButton(browser)  # find review button and click it
				if(reviewAnswer):  # if still there is a review button so we didnt write the review.
					#firstReviewConfirm(browser)
					writeReview(browser, currReview)  # write a review
					time.sleep(twosecSleep)
					retValSubmit = pressSubmit(browser)
					htmlsource = browser.page_source
				if (retValSubmit and currReview in htmlsource):  # check if review has been written
					return True
				else:
					SendEmail("Failed to write review")
			else:  # Review already written in the page.
				#auditReviewDone(outputName, appid, currEmail, key, currReview)  # Review already written - write the review log in excel.
				SendEmail("Already IN - " + currEmail + key)
				return True
		else:
			SendEmail("No device exist" + currEmail) # no device for the current email account.
	return False


def start_requests():
	print("start requests")
	#executable_path = {'executable_path': '/opt/google/chrome/google-chrome'}
	IDlist, keywordsList, emailList, recoveryList, timeList, reviewList, doneList = readDB()  #reading db with accounts
	for index, appid in enumerate(IDlist):
		reviewTime=timeList[index]
		if(reviewTime is not None and checkTime(reviewTime)):  # if current review can be published
			key = keywordsList[index]  # get current key
			currEmail = emailList[index]  # get current email
			#if(checkReviewAudit(currEmail, appid) and doneList[index]=="no"):
			if (doneList[index] == "no"):
				currRecovery = recoveryList[index]  # get current recovery email
				reviewTime = timeList[index]  #  get current review.
				currReview = reviewList[index]
				currDone = doneList[index]
				try:
					
					chrome_options = webdriver.ChromeOptions()
					chrome_options.add_argument("--incognito")
					chrome_options.add_argument('--headless')
					chrome_options.add_argument('--no-sandbox')
					chrome_options.add_argument('--disable-dev-shm-usage')
					#profile = webdriver.FirefoxProfile()
					#profile.set_preference("browser.privatebrowsing.autostart", True)
					#browser = webdriver.Firefox(firefox_profile=profile)
					#browser = webdriver.Firefox()
					browser = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options) 
					print("connecting to chrome")
				except Exception as e:
					print(e)
				reviewAnswer = browse(browser, appid, key, currEmail, currRecovery, reviewTime,currReview)  # make a review for the current details from db.
				if(reviewAnswer):
					doneList[index] = "yes"  # set the value of the current field to Yes. we finish with this index.
					AuditReviewBitbucket(fullFilenameDB, index, "done", "yes")  # audit in bitbucket (change, save and upload).
				time.sleep(tensecSleep*36)
				changeIP(browser)  # changeip using netstick - should be in comment if not using netstick with physical computer
				browser.close()
				time.sleep(twohourSleep/2)  # after publish, sleep for 1 hours.



def main():
	while(True):
		try:
			start_requests()
		except Exception as e:
			print(e)
			SendEmail("App crashed")
	time.sleep(twohourSleep/2)  # after publish, sleep for 1 hours.



if __name__ == "__main__":
	main()
