import csv
from product import Product
from scraper import Scraper

categories_csv = 'blinkit_categories.csv'
locations_csv = 'blinkit_locations.csv'
output_csv = 'products.csv'

categories = []
locations = []

with open(categories_csv, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        categories.append(row)

with open(locations_csv, 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        locations.append(row)

with open(output_csv, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(Product().to_dict().keys())

for (category, location) in zip(categories[1:], locations[1:]):
    l1_category = category[0]
    l1_category_id = category[1]
    l2_category = category[2]
    l2_category_id = category[3]
    coordinates = {
        'lat': location[0],
        'lon': location[1]
    }
    scraper = Scraper(l1_category, l1_category_id, l2_category, l2_category_id, coordinates)
    scraper.start()