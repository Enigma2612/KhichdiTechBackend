from .data import *

def create_user(user_data:dict):
    Users.append(user_data)

def get_all_users():
    return Users

def get_user(user_id):
    for u in Users:
        if 'id' == user_id:
            return u
    
def create_item(item_data):
    Items.append(item_data)

def get_all_items():
    return Items

def create_inventory_entry(inv_data):
    Inventory.append(inv_data)

