from socket import *
import json

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

products = json.loads(clientSocket.recv(1024).decode())

attempts = 3

while attempts > 0:
    print("\nSelect product: (Enter number)")
    
    for index, product in enumerate(products):
        print("{}. {} - R${:.2f}".format(index + 1, product['name'], product['price']))
    
    try:
        product_code = int(input("Enter product number: ")) - 1
        offer_price = float(input("Place your bid: "))
        
        if product_code < 0 or product_code >= len(products):
            print("Invalid code. Please enter a valid product number.")
            continue
        
        if offer_price <= 0:
            print("Invalid bid price. Please enter a positive value.")
            continue

        offer_client = {
            'code': product_code,
            'price': offer_price
        }
        
        clientSocket.send(json.dumps(offer_client).encode())
        
        server_response = clientSocket.recv(1024).decode()
        print(server_response)
        
        attempts -= 1

    except ValueError:
        print("Invalid input. Please enter a valid number.")

print("Bid limit reached. Closing connection.")

clientSocket.close()