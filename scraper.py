import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(soup, products):

    products = soup.find_all(
        'div', class_='a-section a-spacing-small a-spacing-top-small')

    for product in products:
        Product_URL = product.find(
            'a', class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')

        Product_Name = product.find(
            'span', class_='a-size-medium a-color-base a-text-normal')

        Product_Price = product.find('span', class_='a-price')

        Rating = product.find('span', class_='a-size-base')

        Number_of_reviews = product.find('span', class_='aria-label')

        products.append(
            {
                'Product_URL': Product_URL,
                'Product_Name': Product_Name,
                'Product_Price': Product_Price,
                'Rating': Rating,
                'Number_of_reviews': Number_of_reviews,


            }
        )


base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1'


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}


page = requests.get(base_url, headers=headers)


soup = BeautifulSoup(page.text, 'html.parser')


products = []


scrape_page(soup, products)


next_li_element = soup.find('span', class_='s-pagination-strip')

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    page = requests.get(base_url + next_page_relative_url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, products)

    next_li_element = soup.find('span', class_='s-pagination-strip')

csv_page_detail_file = open('products.csv', 'w', encoding='utf-8', newline='')

writer = csv.writer(csv_page_detail_file)

writer.writerow(['Product_Name', 'Product_Price',
                'Rating', 'Number_of_reviews'])

for product in products:
    writer.writerow(product.values())

csv_page_detail_file.close()
