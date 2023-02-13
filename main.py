import hashlib
from random import uniform, choice

store_list = ['Посох', 'Булава', 'Дубинка', 'Кинжал', 'Копье', 'Палица', 'Серп', 'Арбалет', 'Дротик', 'Лук', 'Праща',
              'Алебарда', 'Кирка', 'Молот', 'Топор', 'Глефа', 'Двуручный меч', 'Кнут', 'Меч', 'Моргенштерн', 'Пика',
              'Рапира', 'Секира', 'Скимитар', 'Трезубец', 'Серп', 'Цеп', 'Духовая трубка']

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
    def __init__(self, password):
        self.hash_password = self.get_hash(password)

    @staticmethod
    def password_valid(password):
        password_list = []
        for p in password:
            if not p.isalpha() and not p.isdigit():
                raise TypeError("Пароль должен состоять из букв и цифр")
            password_list.append(p)
        if len(password_list) < 8:
            raise ValueError("Длина пароля не менее 8 символов")

    def get_hash(self, password):
        self.password_valid(password)
        return hashlib.sha256(password.encode()).hexdigest()

    def check(self, password):
        return True if self.hash_password == self.get_hash(password) else False


class Product:
    _id_counter = IdCounter()

    def __init__(self, name=None, price=None, rating=None):
        self._name = name
        self._id = self._id_counter.get_id()
        self.price = price
        self.rating = rating

    def __str__(self):
        return f"id: {self._id}, Товар: {self._name}"

    def __repr__(self):
        return f"Product(id: {self._id}, Товар: {self._name}, Цена: {self.price}, Рейтинг: {self.rating})"

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

    def del_from_cart_by_index(self, index):
        del self.cart[index-1]


class User:
    _id_counter = IdCounter()

    def __init__(self, username, password):
        self._user_id = self._id_counter.get_id()
        self.valid_username(username)
        self._username = username
        self._password = Password(password).get_hash(password)
        self._user_cart = Cart().get_cart()

    def __str__(self):
        return f"id: {self._user_id}, Логин: {self._username}"

    def __repr__(self):
        return f"User(id: {self._user_id}, Логин: {self._username}, Пароль: ********, Корзина: {self._user_cart})"

    @property
    def user_cart(self):
        return self._user_cart

    @staticmethod
    def valid_username(username):
        for letter in username:
            if not letter.isalpha():
                TypeError("Имя должно состоять из букв")

    def get_username(self):
        return self._username


class GunStore:
    _id_counter = IdCounter()

    def __init__(self, enter_username=None, enter_password=None):
        if enter_username is None:
            enter_username = input("Введите имя пользователя: ")
        if enter_password is None:
            enter_password = input("Введите пароль: ")

        self.password = Password(enter_password).get_hash(enter_password)
        del enter_password
        self.user = User(enter_username, self.password).get_username()
        self.cart = Cart().get_cart()

    def add_random(self, val=1):
        for n in range(val):
            prod = Product(choice(store_list), str(round(uniform(1, 100), 2)) + '$', round(uniform(0, 5), 2))
            self.cart.append(prod)


class ProductGenerator:
    _id_counter = IdCounter()

    def __iter__(self):
        return self

    def __next__(self):
        product = Product(choice(store_list), str(round(uniform(1, 100), 2)) + '$', round(uniform(0, 5), 2))
        return product


if __name__ == '__main__':
    print("Проверяю класс Password:")
    pass1 = Password("Пароль123")
    print(pass1.check("Пароль123"), pass1.check("Пароль124"))
    print("--------------------------------------")
    print("Проверяю класс Product:")
    prod1 = Product("Пистолет", "10$", "5")
    print(prod1.__str__())
    print("--------------------------------------")
    print("Проверяю класс Cart:")
    cart1 = Cart()
    cart1.add_in_cart(prod1)
    print(cart1.__dict__)
    print("--------------------------------------")
    print("Проверяю класс User:")
    user1 = User("Логин", "Пароль123")
    print(user1.__repr__())
    print("--------------------------------------")
    print("Проверяю класс GunStore:")
    store = GunStore("Логин", "Пароль123")
    store.add_random(3)
    print(store.cart)
    print("--------------------------------------")
    print("Проверяю класс ProductGenerator:")
    prod_gen = ProductGenerator()
    for n in range(3):
        print(prod_gen.__next__())