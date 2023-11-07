import os
import json
import requests 
import streamlit as st

def get_token():
    if os.path.exists('auth_user'):
        with open("auth_user", "r") as json_file:
            data = json.load(json_file)
            token = data["token"]
            return token

def check_status():
    if os.path.exists('auth_user'):
        with open("auth_user_data", "r") as json_file:
            output = json.load(json_file)

        data = {
            "email": output['email'],
            "password": output['password']
        }
 
        response = requests.post('https://mockapi.up.railway.app/user/login', json=data)

        if response.status_code == 200:
            output = response.json()
            with open("auth_user", "w") as json_file:
                json.dump(output, json_file)
        return True
    else:
        return False
    
