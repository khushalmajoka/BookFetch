import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests

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
        # Extract srcset for highest resolution image
        srcset = img_element.get("srcset")
        if srcset:
            images = srcset.split(", ")
            highest_res_image = images[-1].split(" ")[0]  # Get the last (highest resolution) URL
            return highest_res_image
        return img_element.get("src")  # Fallback to src if no srcset found
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

    # Extracting Discounted Price
    price_whole = soup.select_one("span.a-price > span.a-offscreen")
    discounted_price = price_whole.text.strip() if price_whole else "Not found"

    # Extracting MRP (original price before discount)
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

    # Save results to output.json
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)

    print("✅ Data saved to output.json")
    return results

# Example usage
novels = ["The Alchemist", "Harry Potter and the Philosopher's Stone"]
data = fetch_novel_data(novels)
print(data)
