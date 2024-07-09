# cart.py
from decimal import Decimal
from store.models import Product, Size

class Cart():
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, product_qty, product_size):
        product_id = str(product.id)
        size_name = product_size.name
        key = f'{product_id}_{size_name}'
        if key in self.cart:
            self.cart[key]['qty'] += product_qty
        else:
            self.cart[key] = {'price': str(product.price), 'qty': product_qty, 'size': size_name}
        self.session.modified = True

    def delete(self, product, size):
        product_id = str(product)
        key = f'{product_id}_{size}'
        if key in self.cart:
            del self.cart[key]
        self.session.modified = True

    def update(self, product, qty, size):
        product_id = str(product)
        key = f'{product_id}_{size}'
        if key in self.cart:
            self.cart[key]['qty'] = qty
        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        product_keys = self.cart.keys()
        products = Product.objects.filter(id__in=[key.split('_')[0] for key in product_keys])
        cart = self.cart.copy()
        for product in products:
            for key in list(cart.keys()):
                product_id, size_name = key.split('_', 1)
                if str(product.id) == product_id:
                    cart[key]['product'] = product
                    cart[key]['size'] = size_name
                    cart[key]['price'] = Decimal(cart[key]['price'])
                    cart[key]['total'] = cart[key]['price'] * cart[key]['qty']
                    yield cart[key]

    def get_total(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())
