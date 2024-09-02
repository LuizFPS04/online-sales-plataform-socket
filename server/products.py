class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Catalog:
    def __init__(self):
      self.products_list = []
      pass
    
    def add_product(self, product):
       assert isinstance(product, Product), "Insert an product."
       self.products_list.append(product)

    def show_catalog(self):
       index = 1
       for product in self.products_list:
          print(f'{index}. {product.name}')
          index += 1
    
    def select_product(self, code):
        return self.products_list[code]