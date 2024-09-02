from socket import *
import json

serverPort = 12000
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)

products = [
    {
        'name': "Diamante Negro", 'price': 10
    },
    {
        'name': 'Sufflair', 'price': 50
    },
    {
        'name': 'Crocante', 'price': 25
    }
]

while True:
    connectionSocket, addr = serverSocket.accept()
    
    print('Server is running.')
    
    connectionSocket.send(json.dumps(products).encode())

    attempts = 3
	
    while (attempts > 0):
        
        offer_receive = connectionSocket.recv(1024).decode()
        
        if not offer_receive:
            break
        
        try:
            offer_receive = json.loads(offer_receive)
            
            product_index = int(offer_receive['code'])
            print(product_index)
            if product_index < 0 or product_index >= len(products):
                connectionSocket.send("Invalid index".encode())
                continue
            
            selected_product = products[product_index]
            
            calc = 0
            
            if 0 < selected_product['price'] <= 25:
                calc = 0.1
            elif 25 < selected_product['price'] <= 75:
                calc = 0.15
            else:
                calc = 0.2
        
            offer_value = selected_product['price'] * calc
            
            if (offer_receive['price'] >= (selected_product['price'] - offer_value)):
                response = "Your offer has been accepted! You ordered the product {} for {}".format(selected_product['name'], offer_receive['price'])
            else:
                attempts -= 1
                response = "oOfer refused! You have more {} bids".format(attempts)
                
            connectionSocket.send(response.encode())
        
        except ValueError:
            connectionSocket.send("Invalid entry. Please send a number".encode())
    
        connectionSocket.close()