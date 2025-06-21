import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_info_web(url: str) -> list:
	'''
	This function uses Selenium and BeautifulSoup to scrape all artist links from a Live Nation promotion page.
	It scrolls to the bottom of the page to ensure all dynamic content is loaded, then parses the HTML to extract
	the artist name and link for each artist card. It returns a list
	'''
	options = Options()
	options.add_argument("--headless") 
	driver = webdriver.Chrome(options=options)
	driver.get(url)
	time.sleep(3)
	try:
		last_height = driver.execute_script("return document.body.scrollHeight")
		while True:
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)  
			new_height = driver.execute_script("return document.body.scrollHeight")
			if new_height == last_height:
				break
			last_height = new_height
		html = driver.page_source
		soup = BeautifulSoup(html, "html.parser")
		links = []
		for a in soup.find_all("a", class_="chakra-linkbox__overlay"):
			href = a.get("href")
			nome = a.find("h3").text.strip() if a.find("h3") else ""
			if href:
				if not href.startswith("http"):
					href = "https://www.livenation.com" + href
				links.append((nome, href))
		return links
	finally:
		driver.quit()