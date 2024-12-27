from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

try:
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get('https://www.yearupalumni.org/s/1841/interior.aspx?sid=1841&gid=2&pgid=440')

    results = []

    content = driver.page_source
    soup = BeautifulSoup(content, 'html.parser')

    driver.quit()

    for element in soup.findAll(attrs='title'):
        name = element.find('a')
        if name and name.text not in results:  # Check if name exists and not already in results
            results.append(name.text)

    df = pd.DataFrame({'Names': results})
    df.to_csv('names.csv', index=False, encoding='utf-8')

    print("Data has been successfully scraped and saved to 'names.csv'")

except Exception as e:
    print(f"An error occurred: {e}")