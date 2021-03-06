#### coding=utf8
import csv
import time
import requests # ไม่ได้ใช้ #
import datetime
from random import randint
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
# block notification #
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
##สามารถเปลี่ยนได้ถ้าใช้คำสั่งดุงมาจากตัวเว็ปมาเก็บใน list แต่ตอนดึงมาแสดงไม่ครบจึงเขียนขึ้นมาเอง ##
b = ['1.prepared-for-covid-19','2.express-delivery','3.big-pack','4.fresh-food-frozen-vegetable-fruit','5.dryfood-and-cooking-ingredients', '6.beverages-snacks','7.health-beauty','8.mom-baby-kids','9.household-pets','10.home-appliances-electronic-products','11.home-and-lifestyle','12.stationaries-office-accessories','13.clothing-and-accessories','14.pure','15.besico','16.all_item_group']
print('All group item is : ') 
print('\n'.join(map(str, b))) 
a = input("Enter number of group to scraping  : ")  # รับค่าตัวเลข #
url = ("https://www.bigc.co.th/")

driver.get(url)  # คำสั่งในการเปิดเว็ป #

driver.maximize_window()
    
time.sleep(randint(10,30))
try:
    
    driver.find_element_by_xpath('/html/body/div[4]/div/div[1]/div[2]/button[1]').click() # accept cookies #
except Exception:
    
    pass
time.sleep(10)
try:
    
    driver.find_element_by_xpath('//*[@id="pge_5km-FXot5"]/div[1]/span').click() #ปิด popup ที่เด้งขึ้นมา #
except Exception:
    
    pass

time.sleep(randint(10,20))
#หาสิ่งที่สนใจเช่นชื่อ รูปภาพ กลุ่ม มาเก็บในตัวแปรเพื่อรอใช้งานต่อ #
def extract_record(item):
    atag_2 = item.div.a
    atag = item.div.p
    name_product = atag.text
    url_product = 'https://www.bigc.co.th' + atag_2.get('href') # url #
    image_parent = item.find('div', 'image-card-block')
    image = image_parent.find('img')['src'] #รูปภาพ#
   
 
    price_parent = item.find('div', 'product-price')
    price = price_parent.find('p', 'promotion').text #ราคา#
   
   
    
    group = driver.find_element_by_xpath('//*[@id="product-list"]/div[1]/ol').text #ชื่อกลุ่ม#
    group = group.replace('\n', '_')
    group = group.replace('/', '.')
    group = group.replace(' ', '')
    
    result = (group, image, name_product, price, url_product)
    return result
# ฟังก์ชันการเก็บข้อมูลแล้วกดคลิกหน้าถัดไปวนซ้ำไปเรื่อยๆ #
def scrap_page ():
    while True:
        soup = BeautifulSoup(driver.page_source, 'html.parser') #คำสั่งดึงตัวhtmlทั้งหน้าเว็ปมา
        results = soup.find_all('div', {'class':'product-list-item col-md-3'}) #กรองตัวที่สนใจ
        page_bot = []  #เก็บค่าจำนวดปุ่มทั้งหมด
        page = driver.find_element_by_class_name("col-lg-5")
        items_page = page.find_elements_by_tag_name("li")
        for page_1 in items_page:
            link_page = page_1
            page_bot.append(link_page)
            num_page = len(page_bot)
        time.sleep(12)

        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, f'//*[@id="close-button-1545222288830"]'))).click() ## close popup

        except Exception:
            pass

        try:
            for item in results:
                record = extract_record(item)
                if record:
                    records.append(record)
                    # คำสั่งในการหาปุ่มนั้นจากนั้นเปลี่ยนค่าตรงตำแหน่งสุดท้ายลบด้วยจำนวนหน้าที่ได้เก็บค่าไว้ตอนแรกจะได้ตำแหน่งที่ปุ่ม next อยู่ จากนั้นทำการคลิกและทำเช่นนี้จนไม่สามารถคลิกได้หรือวนไปดึงurlตัวถัดไป
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, f'#product-list > div:nth-child(3) > div.col-md-9 > div.row > div.col-lg-5 > ul > li:nth-child({num_page-1}) > button'))).click()
            time.sleep(randint(15,30))

        except TimeoutException:
            break
records = []
#เก็บค่า url จากหน้าเว็ปหลัก #
url_1 = []
html_list_1 = driver.find_element_by_class_name("swiper-wrapper")
items_1 = html_list_1.find_elements_by_tag_name("a")
for item_1 in items_1:
    link_1 = item_1.get_attribute('href')
    url_1.append(link_1)
#ต้องเปลี่ยนเพราะ url ที่ดึงมาบาง url เป็น url หน้าหลักของหมวดนั้นจึงเปลี่ยนให้เป็นหน้าทั่วไปที่แสดงสินค้าทั้งหมดเพื่อดูดข้อมูล #
url_1 = [item.replace("shop/", "") for item in url_1] 
url_1 = [item.replace("-pharmacy", "") for item in url_1]
url_1 = [item.replace("mum-kids", "mom-baby-kids") for item in url_1]
url_1 = [item.replace("-pharmacy", "") for item in url_1]
url_1.remove("https://www.bigc.co.th/import.html")
#สร้างเงื่อนไขจากการรับค่าตัวเลขตอนแรกเพื่อนำเข้าเงื่อนไขในการดึงข้อมูลแต่ละหมวดแสดงตอนแรก หากตัวเว็ปมีหมวดหมู่ใหม่เข้ามาสามารถเพิ่มเงื่อนไขได้#
if a == "16" : ##ดึงข้อมูลทั้งหมด
    #การทำงานของส่วนนี้คือถ้าพิมพ์เลข16เข้ามาในตัวแปรส่วนนี้จะทำงานโดยดึง urlของหน้าหลักทั้งหมดแล้วเข้าไปหน้า url แรกจากนั้นดึง url หมวดหมู่ทั้งหมด ทำการดึงข้อมูลด้วยเงื่อนไขถ้า มีคำดังกล่าวในตัวแปร url_2 ให้ทำการดึงข้อมูลได้เลยนอกจากนั้นต้องทำการลูปใน url_2 เพื่อเก็บหมวดหมู่ เหตุผลเพื่อถ้าหน้านั้นไม่มีหมวดหมู่เลยจึงดึงข้อมูลได้ทันทีไม่ต้องไปหาหมวดหมู่ทำเช่นเดียวกันในหมวดหมู่ที่ลึกขึ้น
    url_2 = []
    group_name = b[15]
    for index,url in enumerate(url_1):
        driver.get(url) 
        time.sleep(randint(12,20)) 
        html_list_2 = driver.find_element_by_class_name("list-unstyled")
        items_2 = html_list_2.find_elements_by_tag_name("a")
        for item_2 in items_2:
            link_2 = item_2.get_attribute('href')
            url_2.append(link_2)
        url_5 = url_2.copy()        #ตัวแปรนี้ทำการก็อป list ข้างในไว้ #
        url_2.clear() # ลบตัวเก่าทิ้งเพื่อรอตอนวนซ้ำทำการเก็บค่าใหม่ #
        if "https://www.bigc.co.th/about-bigc-shopping-online" in url_2   :  
            scrap_page ()
        else :
            for index,url in enumerate(url_5):
                driver.get(url) 
                time.sleep(12)
                html_list_3 = driver.find_element_by_class_name("list-unstyled")
                items_3 = html_list_3.find_elements_by_tag_name("a")
                for item_3 in items_3:
                    link_3 = item_3.get_attribute('href')
                    url_3.append(link_3)
                url_4 = url_3.copy()        #ตัวแปรนี้ทำการก็อป list ข้างในไว้ #
                url_3.clear() # ลบตัวเก่าทิ้งเพื่อรอตอนวนซ้ำทำการเก็บค่าใหม่ #
                if "https://www.bigc.co.th/about-bigc-shopping-online" in url_4  :  
                    scrap_page ()
                else :
                    for index,url in enumerate(url_4):
                        driver.get(url) 
                        time.sleep(12)
                        scrap_page ()
        
                                
    driver.close()
elif a == '1' :  
    driver.get(url_1[0]) #ตัวอย่างเช่นถ้าพิมพ์เลข 1 ระบบจะดึง url มาจาก list ตำแหน่งที่ 1 ในตัวแปล url_1 ที่เก็บค่าในตอนแรก #
    time.sleep(10)
elif a == '2' :  
    driver.get(url_1[1]) 
    time.sleep(10)
elif a == '3' :  
    driver.get(url_1[2]) 
    time.sleep(10)
elif a == '4' :  
    driver.get(url_1[3]) 
    time.sleep(10)
elif a == '5' :  
    driver.get(url_1[4]) 
    time.sleep(10)
elif a == '6' :  
    driver.get(url_1[5]) 
    time.sleep(10)
elif a == '7' :  
    driver.get(url_1[6]) 
    time.sleep(10)
elif a == '8' :  
    driver.get(url_1[7]) 
    time.sleep(10)
elif a == '9' :  
    driver.get(url_1[8]) 
    time.sleep(10)
elif a == '10' :  
    driver.get(url_1[9]) 
    time.sleep(10)
elif a == '11' :  
    driver.get(url_1[10]) 
    time.sleep(10)
elif a == '12' :  
    driver.get(url_1[11]) 
    time.sleep(10)
elif a == '13' :  
    driver.get(url_1[12]) 
    time.sleep(10)
elif a == '14' :  
    driver.get(url_1[13]) 
    time.sleep(10)
elif a == '15' :  
    driver.get(url_1[14]) 
    time.sleep(10)  
elif a == '' :  
    print('คุณไม่ได้ใส่หมวดหมู่สินค้า')
    time.sleep(7)
    driver.close()  
else :
    print('ไม่มีหมวดหมู่สินค้านี้')
    time.sleep(7)
    driver.close()
#ในการตั้งชื่อไฟล์ใช้ตามกลุ่มหลักที่เราดึง บางตัวอักษรไม่สามารถตั้งได้จึงต้องเปลี่ยน#
group_name = driver.find_element_by_xpath('//*[@id="product-list"]/div[1]/ol/li[2]/span').text 
group_name = group_name.replace('\n', '_')
group_name = group_name.replace('/', '.')
group_name = group_name.replace(' ', '') 
# ทำงานคล้ายการดึงข้อมูลทั้งหมดเพียงแต่ทำการดึงหมวดหมู่ url แค่หมวดเดียวแล้วนำมาทำการหาหมวดย่อยในการดึงข้อมูล #
url_3 = []
url_2 = [] 
html_list_2 = driver.find_element_by_class_name("list-unstyled")
items_2 = html_list_2.find_elements_by_tag_name("a")
for item_2 in items_2:
    link_2 = item_2.get_attribute('href')
    url_2.append(link_2)
    
if "https://www.bigc.co.th/about-bigc-shopping-online" in url_2 or not url_2  :  
    scrap_page ()
else :
    for index,url in enumerate(url_2):
        driver.get(url) 
        time.sleep(12)
        html_list_3 = driver.find_element_by_class_name("list-unstyled")
        items_3 = html_list_3.find_elements_by_tag_name("a")
        for item_3 in items_3:
            link_3 = item_3.get_attribute('href')
            url_3.append(link_3)
        url_4 = url_3.copy()
        url_3.clear()
        if "https://www.bigc.co.th/about-bigc-shopping-online" in url_4 or not url_4  :  
            scrap_page ()
        else :
            for index,url in enumerate(url_4):
                driver.get(url) 
                time.sleep(12)
                scrap_page ()
            
driver.close()
# คำสั่งในการเก็บไฟล์ที่ได้เป็นนามสกุล .csv และแปลงเป็น utf 8 เพื่อให้อ่านค่าภาษาไทยในตัวไฟล์ได้#
file_name = (f'{group_name}-'+str(datetime.datetime.now())+'.csv')
file_name = file_name.replace('-', '_')
file_name = file_name.replace(':', '.')
file_name = file_name.replace(' ', '_')
with open(f'{file_name }','w+', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['group', 'image', 'name_product', 'price', 'url_product'])
    writer.writerows(records)            