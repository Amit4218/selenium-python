from selenium import webdriver   # allows to launch browser
from selenium.webdriver.common.by import By    # allow search with parameters
from selenium.webdriver.support.ui import WebDriverWait     # allow waiting for page to load
from selenium.webdriver.support import expected_conditions as EC    # determine whether the web page has loaded
from selenium.common.exceptions import TimeoutException      # handling timeout situation
from pymongo import MongoClient  # importing Database 
import pandas as pd # importing pandas to help write csv file
import datetime



# Function to send data to database

def database(book_names, book_price, image_urls, stock, rating):

    client = MongoClient()

    client = MongoClient("your connection string")

    db = client.selenium_test_database

    post = {
        "Book Names": book_names,
        "Book Prices": book_price,
        "Image Links": image_urls,
        "Availability": stock,
        "Book Rating": rating
    }

    posts = db.posts
    post_id = posts.insert_one(post).inserted_id

    print(f"Data written succefully")
    
    return post_id

    

# Function to write data into a csv file

def dataToCsv(book_names, book_price, image_urls, stock, rating):
    # Creating a structure
    Title_columns = {
        "Book Names": book_names,
        "Book Prices": book_price,
        "Image Links": image_urls,
        "Availability": stock,
        "Book Rating": rating
    }
    
    data = pd.DataFrame(Title_columns)
    print(data)

    # Save the data into a CSV file
    data.to_csv("books_data.csv", index=False)
    print("Data has been successfully written to 'books_data.csv'")



try:
    link = "https://books.toscrape.com/"
    
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")  # making the browser run in private mode 
    option.add_argument("--headless")  # stopping the application from opening a browser

    driver = webdriver.Chrome(options=option)
    driver.get(link)  # getting data from the link

    wait = WebDriverWait(driver, 10)  # making the automation wait for a certain moment of time

    books_element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "h3 > a")))
    books_names = [book.text for book in books_element]

    price_element = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "price_color")))
    book_price = [price.text for price in price_element]

    image_element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".image_container img")))
    image_urls = [img.get_attribute("src") for img in image_element]

    stock_element = wait.until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".instock.availability")))
    stock = [stock.text.strip() for stock in stock_element]

    rating_element = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "star-rating")))
    rating = [rating.get_attribute("class").split()[-1] for rating in rating_element]  # Extract only the rating class

    driver.quit()  # Close the browser after the task is done

    # Call the function to save the data into a CSV file
    dataToCsv(books_names, book_price, image_urls, stock, rating)

    #calling the database funcion
    database(books_names, book_price, image_urls, stock, rating)

except TimeoutException:
    print(f"Loading the page took too much time!")
except Exception as e:
    print(f"An error occurred: {str(e)}", 500)


