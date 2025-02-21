# 📚 BookFetch - Amazon Book Price & Image Scraper

**BookFetch** is a Python-based web scraper that fetches **book cover images, MRP, and discounted prices** from **Amazon India** using **BeautifulSoup & Requests**. The extracted data is stored in both **JSON and Excel formats** for easy reference. 📚✨

## 🚀 Features
- ✅ **Scrapes Amazon** for book details (image, MRP, discounted price).
- ✅ **Reads book names** from an Excel sheet.
- ✅ **Writes results** back to the same Excel file.
- ✅ **Saves data in JSON format** for quick access.
- ✅ **Fully automated** – just provide the Excel file, and it does the rest!

## 💂️ Project Structure
```
📁 BookFetch/
 ├── 📄 scraper.py       # Main script
 ├── 📄 BookSheet.xlsx   # Excel file containing book names
 ├── 📄 output.json      # JSON file with fetched book data
 ├── 📄 README.md        # Project documentation
```

## 🛠 Installation
1⃣ Clone the repo:
```sh
git clone https://github.com/yourusername/BookFetch.git
cd BookFetch
```
2⃣ Install dependencies:
```sh
pip install -r requirements.txt
```

## 🔥 Usage
1⃣ Ensure your **Excel file (`BookSheet.xlsx`)** contains book names in **column A** (A1, A2, A3...).  
2⃣ Run the script:
```sh
python scraper.py
```
3⃣ Enter the starting row and number of rows when prompted.  
4⃣ The script will:
   - Scrape **Amazon** for book details.
   - Save the results in **JSON (`output.json`)**.
   - Update **BookSheet.xlsx**:
     - 📌 **Column B** → Discount Price  
     - 📌 **Column C** → MRP  
     - 📌 **Column D** → Image URL  

## ⚠️ Notes
- Ensure **BookSheet.xlsx is closed** before running the script (to avoid permission errors).
- Uses **Amazon search results**, so accuracy depends on search ranking.
- Modify **User-Agent** in `headers` if Amazon blocks requests.

## 🏆 Future Enhancements
- 📌 Add support for **Flipkart & other book stores**.
- 📌 Improve **search accuracy** with better filters.
- 📌 Convert JSON data into an interactive **web dashboard**.

---

🔥 **Made with ❤️ by [Your Name]**  
🚀 Happy Scraping! 🖥️✨
