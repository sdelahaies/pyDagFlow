def user(input:dict) -> dict:
    print("user: get user data")
    print(input)
    return input

def username(input:dict) -> str:
    username = input['User']['email'].split('@')[0]
    print("username: get username from email")
    return username

def phone(input:dict) -> str:
    print("phone: get country code from phone number")
    return input['User']['phone'].split('-')[0]

def customer(input:dict) -> dict:
    print("customer: get customer data")
    print(input)
    #custormer_data = {'username': input['Username']['username'], 'phone': input['Phone'][]}
    return {'username': input['Username'], 'country_code': input['Phone']}

def product(input:dict) -> dict:
    print(input)
    print("product: get product data")
    return input

def order(input:dict) -> dict:
    print(input)
    print("order: get order data")
    return {'customer': input['Customer']['username'], 'product': input['Product']['product'], 'price': input['Product']['price'], 'status': 'pending'}

def purchase(input:dict) -> dict:
    print(input)
    print("purchase: get purchase data")
    return {'customer': input['Order']['customer'], 'product': input['Order']['product'], 'price': input['Order']['price'], 'status': 'completed'}
