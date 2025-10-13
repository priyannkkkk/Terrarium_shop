import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# --- Configuration ---
PINTEREST_URL = "https://in.pinterest.com/search/pins/?q=terrarium&rs=typed"
# We aim for ~20, so we set a higher limit to ensure we get enough unique, high-quality images.
TARGET_IMAGE_COUNT = 30
# --- End Configuration ---

def scrape_pinterest_images(url, target_count):
    print(f"Starting Selenium scrape for Pinterest: {url}")
    
    options = Options()
    
    # Using non-headless mode for maximum stability with complex sites like Pinterest
    options.add_argument('--start-maximized') 
    
    # Anti-detection and stability arguments
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--no-sandbox') 
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu") 
    options.add_argument('--log-level=3')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36')
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"ERROR: Could not initialize WebDriver. Error: {e}")
        return []
    
    image_urls = set()

    try:
        driver.get(url)
        print("Browser initialized. Waiting for pins to load...")
        
        # Initial wait targeting a common element on the page (more stable)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-grid-item="true"]'))
        )
        print("Initial pins loaded. Starting scroll to fetch more...")
        
        scroll_count = 0
        max_scrolls = 10 
        
        while len(image_urls) < target_count and scroll_count < max_scrolls:
            # Scroll to the bottom to load new pins
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3) # Increased wait for the slow Pinterest image loading

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # --- CRITICAL FIX: Target all <img> tags and filter them ---
            img_elements = soup.find_all('img')
            
            initial_count = len(image_urls)
            
            for img in img_elements:
                src = img.get('src')
                # Filter criteria: must be an external URL and contain size info (like 236x or 474x)
                if src and src.startswith('https') and any(s in src for s in ['236x', '474x']):
                    image_urls.add(src)

            # Check if we made progress
            if len(image_urls) == initial_count and scroll_count > 1:
                print("No new unique images found after scrolling. Stopping.")
                break

            print(f"  > Scrolled {scroll_count + 1} times. Found {len(image_urls)} unique image URLs.")
            scroll_count += 1

        # Finalize the list
        final_list = list(image_urls)[:target_count]
        
        print(f"\nSUCCESS: Extracted {len(final_list)} image URLs.")
        
        # Convert to DataFrame and save to CSV
        df = pd.DataFrame(final_list, columns=['image_url'])
        df.to_csv("terrarium_image_urls.csv", index=False, encoding='utf-8')
        
        print(f"Data saved to terrarium_image_urls.csv")
        return final_list

    except Exception as e:
        print(f"\nCRITICAL FAILURE: An error occurred during page interaction: {e}")
        return []
    finally:
        driver.quit()

# ... (The if __name__ == "__main__": block remains the same)

# --- Execution ---
if __name__ == "__main__":
    scrape_pinterest_images(PINTEREST_URL, TARGET_IMAGE_COUNT)