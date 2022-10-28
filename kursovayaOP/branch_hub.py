import catalog_hub
import client_hub


def branch_render(call, user):
    call_kw = {'mainmenu': "mainmenu",
               'catalog': "catalog",
               'cart': "cart"
               }

    makers_kw = {}
    tastes_kw = {}
    q=1
    for item in catalog_hub.catalog_get():
        tastes_kw[f'taste{q}']=f"{item['maker']}, {item['taste']}"
        q+=1

    q = 1
    for key in catalog_hub.get_makers():
        makers_kw[f'{str("maker") + str(q)}'] = key
        call_kw[f'{str("maker") + str(q)}'] = key
        q = q + 1


    answer = "Error, try again"
    if call == call_kw['mainmenu']:
        answer = "Главное меню\n-catalog перейти в каталог\n-cart посмотреть корзину\n\n"

    elif call == call_kw['catalog']:
        answer = f"Выбери производителя\n"
        for maker in makers_kw.values():
            answer = answer + str(maker) + "\n"

    elif call in makers_kw.values():
        answer = "Товары проиводителя в наличии:\n"
        products = catalog_hub.get_products(call)
        count = 1
        for product in products:

            answer = answer + product['maker'] + ", " + product["taste"] + " " + str(product['price']) + '\n'
            count += 1
        answer = answer + "\n-catalog назад"
    elif call == call_kw["cart"]:
        cart = client_hub.get_cart(user["login"])
        if cart:
            answer = ''
            for item in cart:
                answer = answer + item['maker']+" "+ item['taste'] +"\n"
        else:
            answer = "Ваша корзина пуста"

    elif call in tastes_kw.values():

        call = call.split(sep=", ")
        product_call = {
            "maker": call[0],
            "taste": call[1]
        }

        product= catalog_hub.find_product(product_call["maker"], product_call["taste"])
        if product!="Not Found":
            answer = f"{product['taste']} \nЦена: {product['price']}\nКоличество: {product['count']}"

    elif "to cart" in call:
        call= call.replace("to cart ", '',1)
        client_hub.add_to_cart(user['login'], call)
        answer = f"Добавлено в вашу корзину {call}"

    elif call == "book":
        info = client_hub.add_book(user['login'])
        for item in info['cart']:
            maker = item['maker']
            taste = item['taste']
            catalog_hub.catalog_change_count(maker, taste, -1)

        answer = f"Ваш номер заказа {info['key']}"

    elif call =="clear cart":
        if client_hub.get_cart():
            client_hub.clear_cart(user['login'])
            answer = "Ваша корзина очищена"
        else:
            answer = "Ваша корзина уже пуста"


    elif "cancel book" in call :
        call = call.replace("cancel book ", '', 1)
        info= client_hub.cancel_book(call)
        print(info)

        for item in info['cart']:
            maker = item['maker']
            taste = item['taste']
            catalog_hub.catalog_change_count(maker, taste, 1)

        answer=f"Ваш заказ {call} отменен"

    elif call == "show books":
        info = client_hub.get_books(user['login'])
        answer ="Заказы\n"
        for i in info:
            answer = answer+ i+"\n"

    print(answer)



