import hashlib
from faker import Faker
from random import randint
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
    def __init__(self, password):
        self.password = self.get_hash(password)

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

    def check(self, enter_pass):
        if self.password == self.get_hash(enter_pass):
            return True
        else:
            return False


class Product:
    _id_counter = IdCounter()

    def __init__(self, name=None):
        self._name = ''.join(fake.color_name()).title()
        if name != None:
            self._name = name
        self._id = self._id_counter.get_id()
        self.price = str(randint(1, 100)) + '$'
        self.rating = randint(1, 100)

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

        # добавить проверки

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

class User(Password):
    _id_counter = IdCounter()
    _user_cart = Cart()

    def __init__(self, username, password):
        super().__init__(password)
        self._user_id = self._id_counter.get_id()
        self._username = self.valid_username(username)
        self.password = self.get_hash(password)
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


class Store(User, Cart):
    _user_cart = Cart()

    def __init__(self, username=None, password=None):
        self._username = self.valid_username(input("Введите имя пользователя: "))
        if username is not None:
            self._username = username
        self._password = self.get_hash(input("Введите пароль: "))
        if password is not None:
            self._username = password
        self.cart = self._user_cart.get_cart()

    def add_random(self):
        self.add_in_cart(''.join(fake.color_name()).title())

if __name__ == '__main__':
    product1 = Product()
    print(product1.__repr__())
    product2 = Product()
    print(product2.__repr__())
    product3 = Product()
    print(product3.__repr__())

    cart1 = Cart(['Красный', 'Синий', 'Зелёный'])
    print(cart1.cart)
    cart1.add_in_cart('Чёрный')
    print(cart1.cart)
    cart1.del_from_data(2)
    print(cart1.cart)

    user = User(str(fake.name()), '1234abcd')
    print(user.__repr__())

    store = Store()
    store.add_random()
    print(store.get_cart())