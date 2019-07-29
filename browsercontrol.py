#!/usr/bin/env python3

# Morgan Wilkinson
# 07/27/2019

#Selenium tutorial

import time
from selenium import webdriver

def className():
	browser = webdriver.Firefox()
	browser.get('http://inventwithpython.com')
	try:
		elem = browser.find_element_by_class_name("jumbotron")
		print('Found <%s> element with that class name!' % (elem.tag_name))
	except:
		print('Was not able to find an element with that name.')


def click():
	browser = webdriver.Firefox()
	browser.get('http://inventwithpython.com')
	linkElem = browser.find_element_by_link_text('Read Online for Free')
	type(linkElem)
	linkElem.click() # follows the "Read It Online" link

def forms():
	browser = webdriver.Firefox()
	browser.get('https://login.live.com') 
	emailElem = browser.find_element_by_id('i0116')
	emailElem.send_keys('morgan7000@hotmail.com')
	emailElem.submit()
	passwordElem = browser.find_element_by_id('i0118')
	time.sleep(10)
	passwordElem.send_keys("Outlook03")
	passwordElem.submit()
forms()

def form2():
	browser = webdriver.Firefox()
	browser.get('https://www.amazon.com/gp/sign-in.html') 
	emailElem = browser.find_element_by_id("ap_email")
	emailElem.send_keys("Email")
	passwordElem = browser.find_element_by_id('ap_password')
	passwordElem.send_keys("Password")
	passwordElem.submit()


