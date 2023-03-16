from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
 
folder = "lex-shop-images"
os.makedirs(folder, exist_ok=True)
os.chdir("D:/Eu/info/Python/scraper")  #D:\Eu\info\Python\scraper\main.py
root_folder = os.getcwd()
 
all_urls = []
product_items_list = []
 
for i in range(1, 2): # max 21
    all_urls.append(f'https://www.lexshop.ro/?page=produse&categorie=20&n={i}')
 
product_links = []
 
for url in all_urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
 
    div = soup.find_all('div', class_='prod_title_container')
    for item in div:
        for link in item.find_all('a', href=True, class_='prod_nou_title'):
            correct_link = 'https://www.lexshop.ro' + link['href']
            product_links.append(correct_link)
 
d = {}
j = 0
 
for link in product_links:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
 
    # Title field
    title = soup.find('div', class_='podus-detail-title').text.strip()
 
    # Description field
    desc = soup.find('div', class_='prod_tabbed_desc').text.strip()
 
    # Price field
    # 659.58
    price_float = soup.find('h3', class_='main_price').text.strip()[:-4]
    price = f"{round(float(price_float))} RON"
 
    # Details
    details = ''
    details_fields = soup.find('div', class_='description-talbe')
    # print('DEBUG : ' + str(details_fields.find_all('li')))
    for item in details_fields.find_all('li'):
        # print('DEBUG : item - > ' + str(item))
        details = details + item.text.strip() + ', '
    # details = details + list.find('li')
 
 
    print(f"{title} : {price}\n {desc}\n {details}\n")
 
    downloaded = []
    os.chdir(folder)
    images = soup.select('.pic_inner_container img')
 
    for image in images:
        img_link = image['src']
        # If it was found in 'd', that means already downloaded, we append it to downloads
        if img_link in d:
            name = d[img_link]
            downloaded.append(name)
        else:
            j = j + 1
            name = f"{j}img.jpg"
            d[img_link] = name
            print('link: ', link)
            print('name: ', name)
            print('------')
            # Saving the images as .jpg
            with open(name, 'wb') as f:
                im = requests.get(img_link)
                f.write(im.content)
            downloaded.append(name)
    
    img_str = ''
    # If more items have been downloaded
    if len(downloaded) > 1:
        for index, img in enumerate(downloaded):
            if index == len(downloaded) - 1:
                img_str = img_str + img
            else:
                img_str = img_str + img + '/'
    else: 
       img_str = downloaded[0]
 
    product = {
        'Game Title':title,
        'Price':price,
        'Description':desc,
        'Details':details,
    } 
    product_items_list.append(product)
 
    os.chdir(root_folder)
df = pd.DataFrame(product_items_list)
print(df)
df.to_csv('lex-shop.csv', index=False)