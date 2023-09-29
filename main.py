from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import requests
from io import BytesIO
from PIL import Image

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds...")
    time.sleep(seconds)
    print("Timer expired!")

def download_image(url, save_path):
    try:
        # Send an HTTP request to the URL
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Open the image using the PIL library
            image = Image.open(BytesIO(response.content))
            
            # Save the image to the specified path
            image.save(save_path)
            print(f"Image downloaded and saved to {save_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    
    except Exception as e:
        print(f"Error: {e}")

def get_img_frm_google(wd, url, thmb_cl, img_cl, delay, max_imgs):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(delay)
 
    wd.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_imgs:
        scroll_down(wd)
        thumbnails = wd.find_elements(By.CLASS_NAME, thmb_cl)

        for img in thumbnails[len(image_urls) + skips:max_imgs]:
            try:
                img.click()
                time.sleep(delay)
            except:
                continue
            
            images = wd.find_elements(By.CLASS_NAME, img_cl)
            #r48jcc pT0Scc iPVvYb
            for image in images:
                if image.get_attribute('src') in image_urls:
                    max_imgs += 1
                    skips += 1
                    break
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    image_urls.add(image.get_attribute('src'))
                    print("Found Image", len(image_urls))

    return image_urls
                


if __name__ == "__main__":

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    #chrome to stay open
    options.add_experimental_option("detach", True)

    wd = webdriver.Chrome(options=options)
    wd.get("https://www.google.com/")

    WebDriverWait(wd, 20).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="W0wltc"]/div'))).click()

    # Change the url, and classes according to the search by inspecting the browser
    url = "https://www.google.com/search?sca_esv=569281890&rlz=1C1YTUH_deDE1061DE1062&sxsrf=AM9HkKl4dK6hCkFAxiK2BXnqxS4qrnym8Q:1695940472165&q=cats&tbm=isch&source=lnms&sa=X&ved=2ahUKEwj495zLrs6BAxXsXEEAHUEgA-8Q0pQJegQIChAB&biw=1280&bih=651&dpr=1.5#imgrc=eAP244UcF5wdYM"
    thmb_class = "Q4LuWd"
    img_class = "r48jcc"

    img_urls = get_img_frm_google(wd, url, thmb_class, img_class,1, 20)
    
    for i, uri in enumerate(img_urls):
        print(i+1)
        print(uri)
        response = requests.get(uri, stream=True)
        folder = "./imgs"
        isExist = os.path.exists(folder)
        if not isExist:
        # Create a new directory because it does not exist
            os.makedirs(folder)
        fname = "image_" + str(i+1) + ".jpg"
        path = os.path.join(folder,fname).replace('\\','/')
        print(path)
        download_image(uri, path)

    wd.quit()
