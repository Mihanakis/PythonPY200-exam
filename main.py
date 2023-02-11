import hashlib
from faker import Faker
from random import uniform
fake = Faker('ru')


class IdCounter:
    def __init__(self):
        self._id = 0

    def get_id(self):
        self._id += 1
        return self.id

    @property
    def id(self):
        return self._id


class Password:

    @staticmethod
    def get_hash(password):
        password_list = []
        for p in password:
            if not p.isalpha() and not p.isdigit():
                raise TypeError("Пароль должен состоять из букв и цифр")
            password_list.append(p)
        if len(password_list) < 8:
            raise ValueError("Длина пароля не менее 8 символов")
        return hashlib.sha256(password.encode()).hexdigest()


    @staticmethod
    def check(self, enter_pass):
        return True if enter_pass == self.get_hash(enter_pass) else False


class Product:
    _id_counter = IdCounter()

    def __init__(self, name, price, rating):
        self._name = name  # self._name = ''.join(fake.color_name()).title()
        self._id = self._id_counter.get_id()
        self.price = price   # str(randint(1, 100)) + '$'
        self.rating = rating   # randint(1, 100)

    def __str__(self):
        return f'{self._id}_{self._name}'

    def __repr__(self):
        return f"Product({self._id}, {self._name}, {self.price}, {self.rating})"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name


class Cart:
    def __init__(self, cart=None):
        if cart is None:
            cart = []
        if not isinstance(cart, list):
            raise TypeError("В корзине не список")
        self.cart = cart

    def get_cart(self):
        return self.cart

    def add_in_cart(self, new_product):
        self.cart.append(new_product)

    def del_from_data(self, index):
        del self.cart[index-1]


class User:
    _id_counter = IdCounter()
    _user_cart = Cart()
    _password = Password()

    def __init__(self, username, password):
        self._user_id = self._id_counter.get_id()
        self._username = self.valid_username(username)
        self._password = self._password.get_hash(password)
        self._user_cart = self._user_cart.get_cart()

    def __str__(self):
        return f'{self._user_id}_{self._username}'

    def __repr__(self):
        return f"Product({self._user_id}, {self._username}, {'password1'}, {self._user_cart})"

    @property
    def user_cart(self):
        return self._user_cart

    @staticmethod
    def valid_username(username):
        for letter in username:
            if not letter.isalpha():
                TypeError("Имя должно состоять из букв")
        return username


class Store:
    _user_cart = Cart()
    _id_counter = IdCounter()
    _password = Password()
    _user = User(input("Введите имя пользователя: "), input("Введите пароль: "))

    def __init__(self):
        self.cart = self._user_cart.get_cart()

    def add_random(self):
        self._user_cart.add_in_cart(''.join(fake.color_name()).title())


class ProductGenerator:

    def __iter__(self):
        return self

    def __next__(self):
        product = Product(''.join(fake.color_name()).title(),
                          str(round(uniform(1, 100), 2)) + '$',
                          round(uniform(0, 5), 2))
        return product


if __name__ == '__main__':
    prod = ProductGenerator()
    for n in range(5):
        print(prod.__next__().__dict__)