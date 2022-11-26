import json
from random import randint

def registrate(login, password):

    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']

    new_user = {
        "login": str(login),
        "password": str(hash(password)),
        "cart": []
    }

    is_found = 0
    for client in clients:
        if new_user["login"] == client["login"]:
            is_found = 1


    if is_found:
        print("User is already registred")
        return new_user
    else:
        clients.append(new_user)
        db['clients']=clients
        with open("databases/clients.json", 'w') as file:
            json.dump(db, file, indent=2)

    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']

    registred = 0
    for client in clients:
        if new_user["login"] == client["login"]:
            registred = 1
            break

    if registred:
        print("Registration is succesful")

    return new_user

def sign_in():
    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']
    login = input("Enter your login: ")
    registred = 0
    for client in clients:
        if login == client["login"]:
            registred = 1
            break

    if registred:
        print(f"Enter the password for {login}: ")
        password = input()
        password = hash(password)
        for client in clients:
            if login == client["login"]:
                if password == client["password"]:
                    print("You are signed in")
                    return {'login': login, 'password': password}
                else:
                    print("password is incorrect")
    else:
        print("No such user. Try one more time")


def get_cart(login):
    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']

    for client in clients:
        if login == client["login"]:
            return client['cart']

def clear_cart(login):

    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']

    for client in clients:
        if client["login"] == login:
            client["cart"] = []
            db["clients"] = clients
            with open("databases/clients.json", 'w') as file:
                json.dump(db, file, indent=2)
            break

def add_to_cart(login, call):

    with open("databases/clients.json", 'r') as file:
        db = json.load(file)
        clients = db['clients']

    maker = call.split(sep=", ")[0]
    taste = call.split(sep=", ")[1]

    offer = {
        "login": login,
        "cart": [
            {
                "maker": maker,
                "taste": taste
            }
        ]

    }

    # Если заказ первый, и если второй
    is_found = 0
    for client in clients:
        if offer["login"] == client["login"]:
            client["cart"].append(offer["cart"][0])
            db["clients"] = clients
            with open("databases/clients.json", 'w') as file:
                json.dump(db, file, indent=2)

            is_found = 1
            break

    if is_found == 0:
        clients.append(offer)
        db["clients"] = clients
        with open("databases/clients.json", 'w') as file:
            json.dump(db, file, indent=2)

    return offer

def add_book(login):
    # сделать бронь товара - перенести карт юзера из клинт в букс

    with open("databases/books.json", 'r') as file:
        books_db = json.load(file)

    with open("databases/clients.json", 'r') as file:
        clients_db = json.load(file)
        clients = clients_db["clients"]

    for client in clients:
        if login == client["login"]:
            cart = client["cart"]
            break

    client = {
        "login": login,

        "key": str(login[0].upper()) + "-" + str(randint(100, 999)),
        "cart": cart
    }

    with open("databases/books.json", "w") as file:
        books_db["books"].append(client)
        json.dump(books_db, file, indent=2)
    clear_cart(login)
    return client

def cancel_book(key):
    with open("databases/books.json", 'r') as file:
        db = json.load(file)
        books = db['books']

    for book in books:
        if key == book['key']:
            deleted = book
            books.remove(book)
            db["books"] = books
            with open("databases/books.json", 'w') as file:
                json.dump(db, file, indent=2)

            return deleted


def get_books(login):
        with open("databases/books.json", 'r') as file:
            db = json.load(file)
            books = db['books']

        output = []
        for book in books:
            key = str(book['key'])
            username = str(book["login"])
            cart = str(book['cart'])
            data = username + "\n" + key + "\n" + cart + "\n"
            if username == login:
                output.append(data)

        return output


