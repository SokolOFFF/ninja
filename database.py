import json

isRegistration = {}
isSettingAmount = {}

def get_database_json():
    f = open('database.json', 'r')
    data = f.read()
    users = json.loads(data)
    return users

def get_users():
    return get_database_json()['users']

def get_subscribers():
    return get_database_json()['subscribers']

def get_moneyamount(id):
    return get_database_json()['moneyamount'][str(id)]

def get_threshold(id):
    return get_database_json()['threshold'][str(id)]

def get_all_moneyamount():
    return get_database_json()['moneyamount']


def set_money_amount(user, mamount):
    data = get_database_json()
    money = data['moneyamount']
    money[user] = mamount
    data['moneyamount'] = money
    f = open("database.json", "w")
    f.write(json.dumps(data))

def set_threshold(user, threshold):
    data = get_database_json()
    th = data['threshold']
    th[user] = threshold
    data['threshold'] = th
    f = open("database.json", "w")
    f.write(json.dumps(data))

def add_user(new_user):
    data = get_database_json()
    users = data['users']
    users.append(new_user)
    data['users'] = users
    f = open("database.json", "w")
    f.write(json.dumps(data))

def delete_user(user):
    data = get_database_json()
    users = data['users']
    users.remove(user)
    data['users'] = users
    f = open("database.json", "w")
    f.write(json.dumps(data))

def add_subscriber(new_sub):
    data = get_database_json()
    subs = data['subscribers']
    subs.append(new_sub)
    data['subscribers'] = subs
    f = open("database.json", "w")
    f.write(json.dumps(data))

def delete_subscriber(sub):
    data = get_database_json()
    subs = data['subscribers']
    subs.remove(sub)
    data['subscribers'] = subs
    f = open("database.json", "w")
    f.write(json.dumps(data))