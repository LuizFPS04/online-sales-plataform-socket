from socket import *
import json

server_name = 'localhost'
server_port = 12000

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_name, server_port))

products = json.loads(client_socket.recv(1024).decode())

attempts = 3

while attempts > 0:
    print("Select a product: (Enter number)")
    
    for index, product in enumerate(products):
        print(f"{index + 1}. {product['name']} - R${product['price']:.2f}")
    
    try:
        product_code = int(input("Enter product number: ")) - 1
        
        if product_code < 0 or product_code >= len(products):
            print("Invalid code. Please enter a valid product number.")
            continue

        offer_price = float(input("Place your bid: "))
        
        if offer_price <= 0:
            print("Invalid bid price. Please enter a positive value.")
            continue
        
        offer_client = {
            'code': product_code,
            'price': offer_price
        }
        
        client_socket.send(json.dumps(offer_client).encode())
        
        server_response = client_socket.recv(1024).decode()
        print(server_response)
        
        if "accepted" in server_response.lower():
            print("Offer accepted! Closing connection.")
            break
        
        elif "Counterproposal" in server_response:
            response_client = input("Do you accept the counterproposal? (yes/no): ").lower()
            
            client_socket.send(response_client.encode())
            
            final_response = client_socket.recv(1024).decode()
            print(final_response)
            
            if "accepted" in final_response.lower():
                print("Counterproposal accepted! Closing connection.")
                break
            else:
                attempts -= 1
                print(f"Attempts remaining: {attempts}")
        
        else:
            attempts -= 1
            print(f"Attempts remaining: {attempts}")
    
    except ValueError:
        print("Invalid input. Please enter a valid number.")

print("Closing connection.")
client_socket.close()