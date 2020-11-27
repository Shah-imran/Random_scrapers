import os
import time
from selenium import webdriver
import csv
import requests
import secrets
from links_handler import LinkHelper
import requests

def connected_to_internet(url='http://www.google.com/', timeout=5):
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("No internet connection available.", end="\r")
        pass
    return False

l = LinkHelper()
total_products = l.linkNumber()

driver = webdriver.Chrome()
driver.set_page_load_timeout(1000)  # 1000 seconds

i = 30077
field_names = ["item_url", "category","sub_category","item_group", "brand", "item_name", "title", "about", "package", "mrp", "thumbnail", "other_images"]
with open("result.csv", 'a', newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = field_names)
    writer.writeheader()
    while i <= total_products:
        url = l.readExactLink(i)
        while not connected_to_internet():
            time.sleep(1)
            # print("no connection...", end="\r")
        driver.get(url)
        print(i, end="\r")
        time.sleep(1)

        try:
            try:
                item_name = ''
                category = ''
                sub_category = ''
                item_group = ''
                brand_name = ''
                about = ''
                item_name = driver.find_element_by_css_selector("._3moNK").get_attribute('textContent').split(">")[-1]
                category = driver.find_element_by_css_selector("._3moNK").get_attribute('textContent').split(">")[-4]
                sub_category = driver.find_element_by_css_selector("._3moNK").get_attribute('textContent').split(">")[-3]
                item_group = driver.find_element_by_css_selector("._3moNK").get_attribute('textContent').split(">")[-2]
                brand_name = driver.find_element_by_class_name("_2zLWN").text
                temp = []
                for item in driver.find_elements_by_class_name("_3ezVU"):
                    temp.append(item.text)
                about = "\n".join(temp)
            except:
                print(url)
            item_title = []
            item_package = []
            item_mrp = []
            item_thumbnail = []
            other_images = []
            try:
                if driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[2]/div[3]/section[2]/div[1]/span").text == "Pack Sizes":
                    for item, item1 in zip( driver.find_elements_by_class_name("_2j_7u"), driver.find_elements_by_class_name("_3Yybm")):
                        item.click()
                        item_title.append(driver.find_element_by_css_selector(".GrE04").get_attribute('textContent'))
                        item_package.append(item1.text)
                        item_mrp.append(item.text)
                        item_thumbnail.append(driver.find_element_by_css_selector("div._2FbOx:nth-child(1) > img:nth-child(1)").get_attribute('src'))
                        links = []
                        for item2 in driver.find_element_by_class_name("_1lzMu").find_elements_by_tag_name("div"):
                            links.append(item2.find_element_by_tag_name("img").get_attribute('src'))

                        other_images.append(" | ".join(links))
            except:
                item_title.append(driver.find_element_by_css_selector(".GrE04").get_attribute('textContent'))
                item_package.append(driver.find_element_by_css_selector(".GrE04").get_attribute('textContent').split(",")[-1])
                item_mrp.append(driver.find_element_by_css_selector(".IyLvo").get_attribute('textContent'))
                item_thumbnail.append(driver.find_element_by_css_selector("div._2FbOx:nth-child(1) > img:nth-child(1)").get_attribute('src'))
                links = []
                for item2 in driver.find_element_by_class_name("_1lzMu").find_elements_by_tag_name("div"):
                    links.append(item2.find_element_by_tag_name("img").get_attribute('src'))

                other_images.append(" | ".join(links))

            for title, package, mrp, thumbnail, o_image in zip(item_title, item_package, item_mrp, item_thumbnail, other_images):
                data = {
                    "category": category,
                    "sub_category": sub_category,
                    "item_group": item_group,
                    "brand": brand_name,
                    "item_name": item_name,
                    "title": title,
                    "about": about,
                    "package": package,
                    "mrp": mrp,
                    "thumbnail": thumbnail,
                    "other_images": o_image,
                    "item_url": url
                }
                # print(data)
                try:
                    writer.writerow(data)
                except Exception as e:
                    print('Error while saving report - {}'.format(e))
        except:
            print(url)
        i += 1

    time.sleep(10)
    driver.quit()