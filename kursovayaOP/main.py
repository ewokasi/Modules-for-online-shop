import client_hub
import branch_hub

print("Добро пожаловать в терминал покупки печенья")
print("1. Регистрация\n2. Вход")

decide = int(input())
if decide == 1:
    login = input("Enter login")
    psw = input("Enter password")
    client_hub.registrate(login, psw)
    user = {
        "login": login,
        "password": psw
    }

elif decide == 2:
    user = client_hub.sign_in()

if user:

    branch_hub.branch_render("mainmenu", user)
    while 1:

        branch = input()
        branch_hub.branch_render(branch, user)
