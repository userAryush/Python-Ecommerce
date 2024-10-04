import json 

def register():
    
    print("Registration")
    user_username= input("Username: ")
    user_password= input("Password: ")
    user_type =input("seller or buyer: ").lower()
    if user_type not in ("seller", "buyer"): #checks is the user_type input is correct
        print("Invalid type ")
        return
   
    user_dict = {user_username:{ "password": user_password, "type": user_type}}#nested dictionary to access type 
    
    write_into_files("login.txt",user_dict) #passing filename, dictoinary to write in files
    
    print("Registration successful!")
    ask = input("Do you want to login?(y/n) ").lower()
    if ask =='y':
        print("To login type login ")
        main()
    

def login(): 
     
    logined = False      
    print("\nLogin")
    user_username = input("Username: ")
    user_password = input("Password: ")
    
    try:
        with open("login.txt","r") as f:
            user_data = f.read()
            if not user_data:
                print("No registered users found!")
                
                ask = input("Do you want to register?(y/n) ").lower()
                if ask =='y':
                    register()
                else:
                    return
    except FileNotFoundError:
        print("Error! File not found")   
        return
    
    user_data_list= user_data.split("|")

    for i in user_data_list:
        if i: 
            try:
                user_dict_data = json.loads(i) 
                if user_username in user_dict_data and user_password == user_dict_data[user_username]["password"]:
                    print('Login Successfull')
                    typed = user_dict_data[user_username]["type"]
                    
                    logined = True
                    return logined, typed, user_username
            except json.JSONDecodeError:
                continue
            
    print("Login failed! Invalid username or password. Type login to try again")
    main()
    
    
def write_into_files(filename,write_dict):
    
    try:
        with open(filename, "r") as f:
            existing_data = f.read()
            
            if existing_data:
                existing_data_list = existing_data.split("|")
            
            else:
                existing_data_list = []
                    
    except FileNotFoundError:
        existing_data_list = []

    with open(filename, "a") as f:
        user_data_json = json.dumps(write_dict)
        if len(existing_data_list) > 0:
            f.write("|")  
        f.write(user_data_json)

        
def add_product(user):
    
    p_name = input("Enter the Product name: ").capitalize()
    p_description = input("Enter the description of the product: ")
    p_price = int(input("Enter the price of the product: "))
    
    product_dict = {"name":p_name, "description":p_description, "Price" : p_price, "seller":user}
    
    write_into_files("product.txt", product_dict)  
    print("Product added successfully!")


def view_product():
    with open("product.txt") as f:
        content = f.read()
    
    content_list = content.split("|")
    for i in content_list:
        
        print(i)
        
def view_product_seller(user):
    with open("product.txt") as f:
        content = f.read()
    
    content_list = content.split("|")
    for i in content_list:
        if i: 
            
            user_dict_data = json.loads(i) 
            if user_dict_data["seller"] == user:
                print(i)
  
        
def buy_product(user):
    
    with open("product.txt") as f:
        content = f.read()
    
    content_list = content.split("|")
    for idx, i in enumerate(content_list):
        if i != '':
            print(str(idx)+'.'+i)

    user_purchase_product = int(input('Enter the id of product you want to buy: '))

    if user_purchase_product <= idx:
        user_purchase_quantity = int(input('Enter the quantity of purchase : '))
        product_data = content_list[user_purchase_product]
        product_dict_data = json.loads(product_data)
        product_price = product_dict_data.get('Price')
        product_name = product_dict_data.get('name')
        total = float(product_price) * user_purchase_quantity
        
        bill_dict = {"product_name": product_name, "quantity": user_purchase_quantity, "total": total, 'customer': user}
        print(f"{user} have successfully purchased {user_purchase_quantity} {product_name} at Rs {total}")
        write_into_files("bill.txt", bill_dict)

    else:
        print('Invalid product')
 
            
def view_bill(user):
    with open("bill.txt") as f:
        content = f.read()
        
        if not content:
            print("You haven't purchased anything yet!")
        else:
            content_list = content.split("|")
            for i in content_list:
                if i: 
                    
                    user_dict_data = json.loads(i) 
                    if user_dict_data["customer"] == user:
                        print(i)
                
           
def seller(user):
    print(f"  |Seller|\nHello {user} Welcome to ecommerce. You can perform following things.")
    while True:
        print("1. Add product\n2. View product\n3. q to exit")
        choice = input("Enter your choice 1/2/q: ")
        if choice == "1":
            add_product(user)
        elif choice == "2":
            view_product_seller(user)
        elif choice == "q":
            break
 
    
def buyer(user):
    print(f"  |Buyer| \nHello {user} Welcome to ecommerce.You can perform following things.")
    while True:
        print("1. View product\n2. Purchase product\n3.View the bill\n4.q to exit")
        choice = input("Enter your choice 1/2/q: ")
        if choice == "1":
            view_product()
        elif choice == "2":
            buy_product(user)
        elif choice == "3":
            view_bill(user)
        
        elif choice == "q":
            break
         
       
def main():   
    
    user_choice = input("Do you want to login or register ").lower()          
    if user_choice == "register":  
        register()
    elif user_choice == "login":
        logined, typed, user = login()
        
    else:
        print("You can only login or register here.")

    if logined:
        if typed == "seller":
            seller(user)
            
        elif typed == "buyer":
            buyer(user)
            
            
main()