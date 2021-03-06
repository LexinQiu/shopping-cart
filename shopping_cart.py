# shopping_cart.py
from datetime import datetime
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()

TAX_RATE = float(os.getenv("TAX_RATE"))

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: my_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


# TODO: write some Python code here to produce the desired output

#print(products)
subtotal_price = 0
product_ids=[]
while True:

# ask for user input
    product_id = input("Please input a product identifier, or 'DONE' if there are no more items:")
    if product_id == "DONE":
        break
    if not product_id.isnumeric() or int(product_id) not in list(map(lambda x: x["id"], products)):
        #print(list(map(lambda x: x["id"], products)))
        print("You entered an invalid identifier. Please try again.")
       

    
    product_ids.append(product_id)

# look up coresponding products

matching_products = []
for product_id in product_ids:
    for x in products:
        if str(x["id"])==str(product_id):
            matching_products.append(x)
            subtotal_price += x["price"]
            break
        
print("-----------------------------------")
print("Welcome to the Planet Grocery Store!")
print("www.planetgrocerystore.com")
print("-----------------------------------")
print("Check out at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S %p'))
print("-----------------------------------")
print("Selected products:")
for matching_product in matching_products:
    print("... "+ matching_product["name"]+" (" + str(to_usd(matching_product["price"]))+")")
print("-----------------------------------")
print("Subtotal: "+ str(to_usd(subtotal_price)))
tax = round(float(subtotal_price) * TAX_RATE, 2)
print("Tax: "+ str(to_usd(tax)))
total = round(tax + subtotal_price, 2)
print("Total price: "+ str(to_usd(total)))
print("-----------------------------------")
print("Thank you! See you again soon!")
print("-----------------------------------")

#send emails

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", default="OOPS, please set env var called 'SENDGRID_API_KEY'")
SENDER_ADDRESS = os.getenv("SENDER_ADDRESS", default="OOPS, please set env var called 'SENDER_ADDRESS'")

client = SendGridAPIClient(SENDGRID_API_KEY) #> <class 'sendgrid.sendgrid.SendGridAPIClient>
#print("CLIENT:", type(client))

subject = "Your Receipt from the Planet Grocery Store"

html_list_items = ""
for p in matching_products:
    html_list_items += f"<li>You ordered: {p['name']} -- {to_usd(p['price'])} </li>"

html_content = f"""
<h3>Hello this is your receipt</h3>
<p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S %p')}</p>
<ol>
    {html_list_items}
</ol>
<p>Subtotal: {str(to_usd(subtotal_price))}</p>
<p>Tax: {str(to_usd(tax))}
<p>Total price: {str(to_usd(total))}</p>

"""
# print("HTML:", html_content)
RECIPIENT_ADDRESS = input("If you would like to receive a receipt via email, please enter your email address here: ")
# FYI: we'll need to use our verified SENDER_ADDRESS as the `from_email` param
# ... but we can customize the `to_emails` param to send to other addresses
message = Mail(from_email=SENDER_ADDRESS, to_emails=RECIPIENT_ADDRESS, subject=subject, html_content=html_content)

try:
    response = client.send(message)

    # print("RESPONSE:", type(response)) #> <class 'python_http_client.client.Response'>
    # print(response.status_code) #> 202 indicates SUCCESS
    # print(response.body)
    # print(response.headers)

except Exception as err:
    print(type(err))
    print(err)
