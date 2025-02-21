import json
import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_amazon_image(novel_name):
    """Fetch high-resolution book cover image from Amazon."""
    search_url = f"https://www.amazon.in/s?k={novel_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
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
    """Fetch book price and MRP from Amazon India."""
    search_url = f"https://www.amazon.in/s?k={novel_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36"
    }
    
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print(f"Amazon request failed: {response.status_code}")
        return {"MRP": "Not found", "Discounted Price": "Not found"}
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    price_whole = soup.select_one("span.a-price > span.a-offscreen")
    discounted_price = price_whole.text.strip() if price_whole else "Not found"
    
    mrp_element = soup.select_one("span.a-text-price > span.a-offscreen")
    mrp = mrp_element.text.strip() if mrp_element else "Not found"
    
    return {"MRP": mrp, "Discounted Price": discounted_price}

def fetch_novel_data(novel_list):
    """Fetch image, MRP, and discounted price for a list of novels."""
    results = {}
    for novel in novel_list:
        print(f"Fetching data for: {novel}")
        image_url = get_amazon_image(novel)
        price_data = get_amazon_price(novel)
        results[novel] = {
            "image_url": image_url,
            "MRP": price_data["MRP"],
            "Discounted Price": price_data["Discounted Price"]
        }
    
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    
    print("✅ Data saved to output.json")
    return results

def read_books_from_excel(file_path, start_row, num_rows):
    """Read book names from an Excel sheet."""
    df = pd.read_excel(file_path, usecols=[0], skiprows=start_row - 1, nrows=num_rows, header=None)
    return df[0].dropna().tolist()

if __name__ == "__main__":
    file_path = "BookSheet.xlsx"
    start_row = int(input("Enter the start row number: "))
    num_rows = int(input("Enter the number of rows to read: "))
    
    novels = read_books_from_excel(file_path, start_row, num_rows)
    print(f"Books to fetch: {novels}")
    
    data = fetch_novel_data(novels)
    print(json.dumps(data, indent=4))
