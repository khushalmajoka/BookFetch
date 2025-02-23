import json
import time
import random
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key securely
API_KEY = os.getenv("SCRAPER_API_KEY")

def get_amazon_image(novel_name):
    """Fetch high-resolution book cover image from Amazon with ScraperAPI."""
    time.sleep(random.uniform(2, 5))  # Reduced delay since ScraperAPI handles rate limits
    search_url = f"https://www.amazon.in/s?k={novel_name.replace(' ', '+')}"
    scraper_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={search_url}"

    response = requests.get(scraper_url)
    if response.status_code != 200:
        print(f"Amazon request failed: {response.status_code}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    img_element = soup.select_one("img.s-image")
    
    if img_element:
        srcset = img_element.get("srcset")
        if srcset:
            images = srcset.split(", ")
            highest_res_image = images[-1].split(" ")[0]
            return highest_res_image
        return img_element.get("src")
    return None

def get_amazon_price(novel_name):
    """Fetch book price and MRP from Amazon India using ScraperAPI."""
    time.sleep(random.uniform(2, 5))  # Reduced delay
    search_url = f"https://www.amazon.in/s?k={novel_name.replace(' ', '+')}"
    scraper_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={search_url}"

    response = requests.get(scraper_url)
    if response.status_code != 200:
        print(f"Amazon request failed: {response.status_code}")
        return {"MRP": "Not found", "Discounted Price": "Not found"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    price_whole = soup.select_one("span.a-price > span.a-offscreen")
    discounted_price = price_whole.text.strip() if price_whole else "Not found"
    
    mrp_element = soup.select_one("span.a-text-price > span.a-offscreen")
    mrp = mrp_element.text.strip() if mrp_element else "Not found"
    
    return {"MRP": mrp, "Discounted Price": discounted_price}

def fetch_novel_data(novel_list, file_path, start_row):
    """Fetch image, MRP, and discounted price for novels and update Excel file."""
    results = {}
    df = pd.read_excel(file_path, header=None)  # Read entire Excel sheet

    for index, novel in enumerate(novel_list):
        row_index = start_row - 1 + index  # Calculate Excel row index
        print(f"Fetching data for: {novel}")
        
        image_url = get_amazon_image(novel)
        price_data = get_amazon_price(novel)
        
        results[novel] = {
            "image_url": image_url,
            "MRP": price_data["MRP"],
            "Discounted Price": price_data["Discounted Price"]
        }

        # Update DataFrame without modifying first column (Book Name)
        df.at[row_index, 1] = price_data["Discounted Price"]  # Column B
        df.at[row_index, 2] = price_data["MRP"]  # Column C
        df.at[row_index, 3] = image_url  # Column D

    # Save results to output.json
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    # Write back to the Excel file without modifying Book Names
    df.to_excel(file_path, index=False, header=False)

    print("✅ Data saved to output.json and updated in BookSheet.xlsx")
    return results

def read_books_from_excel(file_path, start_row, num_rows):
    """Read book names from an Excel sheet without modifying the first column."""
    df = pd.read_excel(file_path, usecols=[0], skiprows=start_row - 1, nrows=num_rows, header=None)
    return df[0].dropna().tolist()

if __name__ == "__main__":
    file_path = "BookSheet.xlsx"
    start_row = int(input("Enter the start row number: "))
    num_rows = int(input("Enter the number of rows to read: "))
    
    novels = read_books_from_excel(file_path, start_row, num_rows)
    print(f"Books to fetch: {novels}")
    
    data = fetch_novel_data(novels, file_path, start_row)
    print(json.dumps(data, indent=4))
