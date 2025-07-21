from datetime import datetime

class Product:
    def __init__(self, data=None):
        self.date = datetime.today().date()
        
        self.l1_category = None
        self.l1_category_id = None
        self.l2_category = None
        self.l2_category_id = None
        self.store_id = None
        self.variant_id = None
        self.variant_name = None
        self.group_id = None
        self.selling_price = None
        self.mrp = None
        self.in_stock = None
        self.inventory = None
        self.is_sponsored = None
        self.image_url = None
        self.brand_id = None
        self.brand = None
        
        # Initialize from dictionary if provided
        if data and isinstance(data, dict):
            for key, value in data.items():
                if hasattr(self, key):
                    setattr(self, key, value)

    def to_dict(self):
        return {
            'date': str(self.date),
            'l1_category': self.l1_category,
            'l1_category_id': self.l1_category_id,
            'l2_category': self.l2_category,
            'l2_category_id': self.l2_category_id,
            'store_id': self.store_id,
            'variant_id': self.variant_id,
            'variant_name': self.variant_name,
            'group_id': self.group_id,
            'selling_price': self.selling_price,
            'mrp': self.mrp,
            'in_stock': self.in_stock,
            'inventory': self.inventory,
            'is_sponsored': self.is_sponsored,
            'image_url': self.image_url,
            'brand_id': self.brand_id,
            'brand': self.brand
        }
