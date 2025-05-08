from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import re

def scrape_books():
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get("http://books.toscrape.com/")
        print("Browser opened successfully!")

        books = []
        page = 1
        
        while True:
            print(f"Scraping page {page}...")
            book_elements = driver.find_elements(By.CSS_SELECTOR, "article.product_pod")
            
            if not book_elements:
                print("No books found on this page. Stopping.")
                break

            for book in book_elements:
                try:
                    title = book.find_element(By.TAG_NAME, "h3").find_element(By.TAG_NAME, "a").get_attribute("title")
                    price_text = book.find_element(By.CSS_SELECTOR, "p.price_color").text
                    clean_price = re.sub(r'[^\d.]', '', price_text)
                    price = float(clean_price)
                    rating = book.find_element(By.CSS_SELECTOR, "p.star-rating").get_attribute("class").split(" ")[-1]
                    availability = book.find_element(By.CSS_SELECTOR, "p.availability").text.strip()
                    
                    books.append({
                        "title": title,
                        "price": price,
                        "rating": rating,
                        "availability": availability
                    })
                except NoSuchElementException as e:
                    print(f"Error scraping a book: {e}")
                    continue

            try:
                next_button = driver.find_element(By.CSS_SELECTOR, "li.next a")
                next_button.click()
                page += 1
            except NoSuchElementException:
                print("No more pages. Stopping.")
                break

        # Save CSV
        df = pd.DataFrame(books)
        df.to_csv("books.csv", index=False, encoding='utf-8-sig')
        print(f"CSV saved with {len(books)} books!")

    except Exception as e:
        print(f"Critical error: {e}")
    finally:
        driver.quit()
        print("Browser closed.")

if __name__ == "__main__":
    scrape_books()