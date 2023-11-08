import os
import json

# Ter acesso ao token para conseguir acessar os metofdos da api
def get_token():
    if os.path.exists('auth_user'):
        with open("auth_user", "r") as json_file:
            data = json.load(json_file)
            token = data["token"]
            return token

#Checar se o usuário logou nessa seção 
def check_status():
    if os.path.exists('auth_user'):
        return True
    else:
        return False
    
