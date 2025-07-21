import csv
import requests
import time
from product import Product

class Scraper:
    def __init__(self, l1_category, l1_category_id, l2_category, l2_category_id, coordinates):
        self.l1_category = l1_category
        self.l1_category_id = l1_category_id
        self.l2_category = l2_category
        self.l2_category_id = l2_category_id
        self.coordinates = coordinates
        self.base_url = "https://blinkit.com/"
        self.url = self.base_url + f"v1/layout/listing_widgets?l0_cat={self.l1_category_id}&l1_cat={self.l2_category_id}&offset=0&limit=15"
        self.headers = {
            'lat': str(self.coordinates['lat']),
            'lon': str(self.coordinates['lon']),
            'user-agent': 'undefined'
        }
        self.products = []
        self.output_csv = "products.csv"
    
    def get_product_details(self, product):
        data = product['data']
        attributes = product['tracking']['common_attributes']

        product_name = data['name']['text']
        variant_id = data['product_id']
        variant_name = product_name + " " + data['variant']['text'] 
        store_id = data['merchant_id']
        group_id = data['group_id']
        image_url = data['image']['url']
        is_sponsored = attributes['badge'] == 'AD'
        mrp = attributes['mrp']
        selling_price = attributes['price']
        inventory = attributes['inventory']
        brand = attributes['brand']
        type_id = attributes['type_id']
        in_stock = inventory > 0

        return Product({
            'variant_id': variant_id,
            'variant_name': variant_name,
            'image_url': image_url,
            'store_id': store_id,
            'group_id': group_id,
            'brand': brand,
            'type_id': type_id,
            'is_sponsored': is_sponsored,
            'in_stock': in_stock,
            'mrp': mrp,
            'selling_price': selling_price,
            'inventory': inventory,
            'l1_category': self.l1_category,
            'l2_category': self.l2_category,
            'l1_category_id': self.l1_category_id,
            'l2_category_id': self.l2_category_id
        })

    def scrape_products(self, snippets):
        for product in snippets[1:]:
            variants = []

            if 'variant_list' not in product['data']:
                product = self.get_product_details(product)
                variants.append(product)
            else:
                for variant in product['data']['variant_list']:
                    product = self.get_product_details(variant)
                    variants.append(product)

            self.products.extend(variants)
        self.write_to_csv()

    def get_response(self, url=None):
        if url is None:
            url = self.url
        response = requests.post(url, headers=self.headers)
        if response.status_code == 429:
            time.sleep(5)
            print("Rate limit exceeded")
            return self.get_response(url)
        return response.json()['response']

    def start(self):
        res = self.get_response()

        snippets = res['snippets']
        self.scrape_products(snippets)

        while 'pagination' in res:
            time.sleep(0.5)
            next_url = self.base_url + res['pagination']['next_url']
            res = self.get_response(next_url)

            snippets = res['snippets']
            self.scrape_products(snippets)

    def write_to_csv(self):
        with open(self.output_csv, 'a') as f:
            writer = csv.writer(f)
            for product in self.products:
                writer.writerow(product.to_dict().values())
