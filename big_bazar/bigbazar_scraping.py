# Import required modules
from selenium import webdriver
import time
import pandas as pd
import numpy as np



# Block browser notification
options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications":2}
options.add_experimental_option("prefs", prefs)


# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)


# Run in headless
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument('--no-sandbox')
options.add_argument('--log-level=3')



# Create an empty csv with todays date
TODAY = pd.to_datetime("today").strftime("%d_%b_%y")

pd.DataFrame({
    "product_name":np.nan,
    "img_link":np.nan,
    "offer_price":np.nan,
    "original_price":np.nan,
    "size":np.nan,
    "cover_page":np.nan
}, index=[0]).to_csv(f"{TODAY}_bigbazar_scraped_data.csv", index=None)




def scrape_info(url):
    # Initialize empty list of variables to scrape
    product_name = []
    img_link = []
    offer_price = []
    original_price = []
    size = []
    cover_page = []
    savings = []
    
    try:
        driver = webdriver.Chrome("/home/faysal/Documents/utilities/chromedriver",
                             options=options)
        driver.get(url)
        
        # time.sleep(5) 
        # Will required without headless
        
#         try:
#             driver.find_element_by_class_name("loginCross").click()
#         except:
#             pass
        # Will required without headless

        try:
            for _ in range(10):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(4)
        except:
            pass

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

        driver.close()
        df = pd.DataFrame({
        "product_name":product_name,
        "img_link":img_link,
        "offer_price":offer_price,
        "original_price":original_price,
        "size":size,
        "cover_page":cover_page
        })
        with open(f"{TODAY}_bigbazar_scraped_data.csv", "a") as f:
            df.to_csv(f, header=False, index=None)
    except:
        driver.close()
        df = pd.DataFrame({
                "product_name":np.nan,
                "img_link":np.nan,
                "offer_price":np.nan,
                "original_price":np.nan,
                "size":np.nan,
                "cover_page":url}, index=[0])
        
        with open(f"{TODAY}_bigbazar_scraped_data.csv", "a") as f:
            df.to_csv(f, header=False, index=None)




# Read in csv data
link_df = pd.read_csv("bigbazar_cat_link.csv")
link_df["sub_cat1"]= np.where(link_df.sub_cat1.isna(),
         link_df.link.str.split("/").str[-1].str.split("-").str[:-1].str.join(" "),
         link_df.sub_cat1)



# Scrape data
for lnk in link_df.link.iloc[:3]:  # Increase or decrease the size of link. This is very time consuming
    scrape_info(lnk)



# Read in the file
df = pd.read_csv(f"{TODAY}_bigbazar_scraped_data.csv")
df.dropna(how="all")
df.offer_price = df.offer_price.str.split("\n").str[0]
m = pd.merge(df, link_df, left_on="cover_page", right_on="link")
m["sub_cat2"] = m.link.str.split("/").str[-1].str.split("-").str[:-1].str.join(" ")
m = m[["cover_page", "product_name", "size", "offer_price", "original_price",
       "img_link", "broad_cat", "sub_cat1", "sub_cat2"]]

# Overwrite the current file
m.to_csv(f"{TODAY}_bigbazar_scraped_data.csv", index=None)

