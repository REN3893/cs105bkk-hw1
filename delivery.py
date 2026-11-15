"""HW1: a Bangkok food-delivery order. Practises Sessions 1-3: aliasing and defaults, comprehensions,
classes with a guarded property, __repr__ and __eq__, inheritance with super(), composition and duck typing."""


class MenuItem:

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price

    @property
    def price(self) -> int:
        return self._price

    @price.setter
    def price(self, value: int) -> None:
        if value <= 0:
            raise ValueError(f'price must be more than 0 baht, got {value}')
        self._price = value
    
    def __repr__(self) -> str:
        return f'{type(self).__name__}({self.name!r}, {self._price})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, MenuItem):
            return NotImplemented
        return self._price == other._price and self.name == other.name

    def cost(self, quantity: int) -> int:
        return self.price * quantity

class PromoItem(MenuItem):

    def cost(self, quantity: int) -> int:
        return super().cost(quantity - quantity//3)

class Order:

    delivery_fee = 30  # Provided: baht added to every order with food in it
    free_delivery_from = 300  # Provided: food worth this much or more is delivered free

    def __init__(self, customer: str, lines: list[tuple[MenuItem, int]] | None = None):
        self.customer = customer
        if lines :
            self.lines = list(lines)
        else:
            self.lines = []

    def add(self, item: MenuItem, quantity: int = 1) -> None:
        if quantity < 1:
            raise ValueError(f'quantity must be at least 1, got {quantity}')
        self.lines.append((item, quantity))
        
    def total(self) -> int:
        if not self.lines:
            return 0
        food_cost = sum(item.cost(quantity) for item, quantity in self.lines)
        if food_cost >= self.free_delivery_from:
            return food_cost
        return food_cost + self.delivery_fee
    
    def summary(self) -> list[str]:
        nli = []
        for item, quantity in self.lines:
            st = ''
            st+=str(quantity)+' x '+item.name
            nli.append(st)
        return nli

def cheapest(options: list) -> object | None:
    if not options:
        return None
    return min(options, key=lambda option: option.total())