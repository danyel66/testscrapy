# import only the necessary libraries, for interacting with the website
from selenium.webdriver import Chrome, ChromeOptions
import os.path
from os import path
from selenium.webdriver.common.by import By
import pandas as pd


# Takes a URL as input and returns a list of data as output
def get_data(url)->list:
    browser_options = ChromeOptions()
    browser_options.add_argument("--headless=new")
    driver = Chrome(options=browser_options)
    driver.get(url)

    # finds the element on the page that corresponds to the "Humor" link and clicks it
    element = driver.find_element(By.LINK_TEXT, "Humor")
    element.click()

    # finds all of the elements on the page that correspond to the "product_pod" CSS selector
    books = driver.find_elements(By.CSS_SELECTOR, ".product_pod")
    data = []

    # iterates over all of the book products on the page and extracts the title, price, and stock for each product then, closes the Selenium driver and returns the data list
    for book in books:
        title = book.find_element(By.CSS_SELECTOR, "h3 > a")
        price = book.find_element(By.CSS_SELECTOR, ".price_color")
        stock = book.find_element(By.CSS_SELECTOR, ".instock.availability")

        book_item = {
            'title':title.get_attribute("title"),
            'price':price.text,
            'stock':stock.text
        }
        data.append(book_item)

    driver.quit()
    return data

# export data to CSV files
def csv_export(data):
    df = pd.DataFrame(data)
    df.to_csv("scraped_books.csv", index=False)
    print(df)

# main() function calls the get_data() function to fetch the data from the website
def main():
    data = get_data("https://books.toscrape.com/")
    csv_export(data)

if __name__ == '__main__':
    main()
