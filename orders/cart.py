# orders/cart.py
from decimal import Decimal
from products.models import Product

CART_SESSION_KEY = "cart"

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session[CART_SESSION_KEY] = {}
        self.cart = cart

    def add(self, product_id: int, qty: int = 1, replace: bool = False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {"qty": 0}
        if replace:
            self.cart[product_id]["qty"] = max(1, qty)
        else:
            self.cart[product_id]["qty"] = max(1, self.cart[product_id]["qty"] + qty)
        self.save()

    def remove(self, product_id: int):
        pid = str(product_id)
        if pid in self.cart:
            del self.cart[pid]
            self.save()

    def clear(self):
        self.session[CART_SESSION_KEY] = {}
        self.session.modified = True

    def save(self):
        self.session[CART_SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = {str(p.id): p for p in Product.objects.filter(id__in=product_ids)}
        for pid, item in self.cart.items():
            p = products.get(pid)
            if not p:
                continue
            qty = int(item["qty"])
            price = p.price
            yield {
                "product": p,
                "qty": qty,
                "price": price,
                "line_total": price * qty,
            }

    def total_qty(self):
        return sum(int(v["qty"]) for v in self.cart.values())

    def total_price(self):
        total = Decimal("0.00")
        for x in self:
            total += x["line_total"]
        return total
