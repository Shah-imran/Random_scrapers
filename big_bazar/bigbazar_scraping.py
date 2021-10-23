# Import required modules
from selenium import webdriver
import time
import pandas as pd
import numpy as np




# Block browser notification
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications":2}
chrome_options.add_experimental_option("prefs", prefs)

# Run in headless
chrome_options.headless = True



# Function to extract data
def get_info(urls):
    driver = webdriver.Chrome("/home/faysal/Desktop/big_bazar/chromedriver", options=chrome_options) # Set the path accordingly if windows machine
    # Initialize empty list of variables to scrape
    product_name = []
    img_link = []
    offer_price = []
    original_price = []
    size = []
    cover_page = []
    savings = []
    
    for url in urls:
        driver.get(url)
        time.sleep(5)
        
        try:
            driver.find_element_by_class_name("loginCross").click()
        except:
            pass
        
        try:
            for _ in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
        except:
            break

        main_cont = driver.find_elements_by_class_name("col-xs-4.col-sm-4.similar")
        for cont in main_cont:
            try:
                cont.find_element_by_class_name("size.remove-arrow").click()
                time.sleep(2)
                for el in range(len(driver.find_elements_by_css_selector(".details.quick-view-variant"))):
                    driver.find_elements_by_css_selector(".details.quick-view-variant")[el].click()
                    time.sleep(4)
                    try:
                        brand = driver.find_element_by_css_selector("h5.brand").text.strip()
                        name = driver.find_element_by_css_selector("h5.name").text.strip()
                        product_name.append(f"{brand} {name}")
                    except:
                        product_name.append(np.nan)
                    
                    try:
                        img_link.append(driver.find_element_by_class_name("slick-slide.slick-active.slick-current img").get_attribute("src"))
                    except:
                        img_link.append(np.nan)
                        
                    try:
                        size.append(driver.find_element_by_css_selector(".details.quick-view-variant.skubg").text.strip())
                    except:
                        size.append(np.nan)
                    
                    try:
                        offer_price.append(driver.find_element_by_class_name("quickView-memberPrice").text.strip())
                    except:
                        offer_price.append(np.nan)
                    
                    try:
                        original_price.append(driver.find_element_by_class_name("quickView-discount").text.strip())
                    except:
                        original_price.append(np.nan)
                    
                    cover_page.append(url)
                    
                driver.find_element_by_css_selector("span.QuikClose").click()

                
                
            except:
                try:
                    product_name.append(cont.find_element_by_class_name("product-name").text.strip())
                except:
                    product_name.append(np.nan)

                try:
                    img_link.append(cont.find_element_by_css_selector("div.plpimage img").get_attribute("src"))
                except:
                    img_link.append(np.nan)

                try:
                    offer_price.append(cont.find_element_by_css_selector("div.member-prices").text.strip())
                except:
                    offer_price.append(np.nan)

                try:
                    size.append(cont.find_element_by_css_selector("div.size").text.strip())
                except:
                    size.append(np.nan)

                try:
                    original_price.append(cont.find_element_by_css_selector("div.list-price").text.strip())
                except:
                    original_price.append(np.nan)
                
                cover_page.append(url)
                    
    # Create a df off scraped variables
    df = pd.DataFrame({
        "product_name":product_name,
        "img_link":img_link,
        "offer_price":offer_price,
        "original_price":original_price,
        "size":size,
        "cover_page":cover_page
    })
    return df



# Read in csv data of category links
link_df = pd.read_csv("bigbazar_cat_link.csv")
link_df["sub_cat1"]= np.where(link_df.sub_cat1.isna(),
         link_df.link.str.split("/").str[-1].str.split("-").str[:-1].str.join(" "),
         link_df.sub_cat1)


# Save the the data
TODAY = pd.to_datetime("today").strftime("%d_%b_%y")
df = get_info(link_df.link) # Increase/decrease the category link as required
df.offer_price = df.offer_price.str.split("\n").str[0]
m = pd.merge(df, link_df, left_on="cover_page", right_on="link")
m["sub_cat2"] = m.link.str.split("/").str[-1].str.split("-").str[:-1].str.join(" ")
m = m[["cover_page", "product_name", "size", "offer_price", "original_price",
       "img_link", "broad_cat", "sub_cat1", "sub_cat2"]]

# Asave the output as csv
m.to_csv(f"{TODAY}_bigbazar_data.csv", index=None)

