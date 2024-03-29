# Install required libraries
# pip install beautifulsoup4 requests

# myapp/utils.py
import requests, base64
from bs4 import BeautifulSoup
from io import BytesIO

# from myapp.models import ScrapedItem

def scrape_items():
    url = 'https://www.google.com/search?tbm=shop&q=white+nike+t+shirt'
    header={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    data = requests.get(url, headers=header)
    soup = BeautifulSoup(data.content, 'html.parser')
     
    scrapped_items=[]
    for div in soup.find_all('div', class_='sh-dgr__content'):
        link1="https://www.google.com/"
        link_tag = div.find('a', class_='xCpuod')
        link = link1+link_tag['href'] if link_tag else None
        print(link)
        # Extracting image source
        img_div = div.find('div', class_='ArOc1c')
        img_src = img_div.find('img')
        if img_src:
            img_source = img_src.get('src')

        
        # Extracting header text
        h3_tag = div.find('h3', class_='tAxDx')
        header_text = h3_tag.text.strip() if h3_tag else None
        
        # Extracting price
        span_tag = div.find('span', class_='a8Pemb OFFNJ')
        price_text = span_tag.text.strip() if span_tag else None
        
        scrapped_items.append({
            'link': link,
            'img_link': img_source,
            'name': header_text,
            'price': price_text
        })
    # print (scrapped_items)
    return scrapped_items

# Run this function to perform web scraping and populate the database
scrape_items()


# TShirt= {
#         'red': 18,
#         'dark red': 18,
#         'white': 18,
#         'black': 20,
#         'blue': 18,
#         'dark-blue': 20,
#         'yellow': 10,
#         'green': 14,
#         'sky-blue': 15,
#         'light green': 12,
#         'pink': 16,
#         'purple': 17,
#         'orange': 15,
#         'brown': 15,
#         'grey': 18
#     }
    
# Shirt= {
#         'red': 17,
#         'white': 20,
#         'black': 20,
#         'blue': 18,
#         'dark-blue': 19,
#         'yellow': 10,
#         'green': 14,
#         'sky-blue': 18,
#         'light green': 16,
#         'pink': 17,
#         'purple': 15,
#         'orange': 15,
#         'brown': 17,
#         'grey': 18
#     }

# Pant= {
#         'red': 8,
#         'white': 17,
#         'black': 20,
#         'blue': 20,
#         'dark-blue': 20,
#         'yellow': 6,
#         'green': 15,
#         'sky-blue': 17,
#         'light green': 6,
#         'pink': 10,
#         'purple': 11,
#         'orange': 8,
#         'brown': 17,
#         'grey': 19,
#         'cream': 18
#     }

# Shoes= {
#         'red': 9,
#         'dark-blue': 15,
#         'white': 15,
#         'black': 15,
#         'yellow': 9,
#         'green': 1,
#         'sky-blue': 15,
#         'light green': 9,
#         'pink': 15,
#         'purple': 15,
#         'orange': 15,
#         'brown': 10,
#         'grey': 15
#     }

# Dress= {
#         'red': 19,
#         'dark-blue': 18,
#         'white': 20,
#         'black': 20,
#         'yellow': 17,
#         'green': 17,
#         'sky-blue': 19,
#         'light green': 17,
#         'pink': 18,
#         'purple': 19,
#         'orange': 17,
#         'brown': 16,
#         'grey': 19
#     }

# #pants on dress like kurta
# Dpants= {
#         'red': 8,
#         'dark-blue': 15,
#         'white': 18,
#         'black': 18,
#         'yellow': 7,
#         'green': 7,
#         'sky-blue': 15,
#         'light green': 6,
#         'pink': 7,
#         'purple': 14,
#         'orange': 9,
#         'brown': 9,
#         'grey': 15,
#         'blue': 18,
#         'cream': 18
#     }
        
# Jacket= {
#         'red': 12,
#         'dark blue': 20,
#         'white': 20,
#         'black': 20,
#         'yellow': 12,
#         'green': 14,
#         'sky blue': 18,
#         'light green': 11,
#         'pink': 15,
#         'purple': 17,
#         'orange': 11,
#         'brown': 15,
#         'grey': 18,
#         'cream': 15
#     }

# upper_color = upper.color
# lower_color = lower.color
# bottom_color = bottom.color
# upper_type = upper.name
# lower_type = lower.name
# bottom_type= bottom.name


# lower_color_scores= Pant
# bottom_color_scores=Shoes

# if(upper_type=='T-Shirt'):
#     upper_color_scores= TShirt
# elif(upper_type=='Dress'):
#     upper_color_scores= Dress
#     lower_color_scores= Dpants
# else:
#     upper_color_scores= Shirt


# #add_item.tml
# #recomm_ui
# #scrappin_all
    