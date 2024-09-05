from socket import *
import json

server_port = 12000
server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', server_port))
server_socket.listen(1)

products = [
    {'name': "Diamante Negro", 'price': 10},
    {'name': 'Sufflair', 'price': 50},
    {'name': 'Crocante', 'price': 25}
]

while True:
    connection_socket, addr = server_socket.accept()
    
    print('Server is running.')
    
    connection_socket.send(json.dumps(products).encode())

    attempts = 3
	
    while attempts > 0:
        
        offer_receive = connection_socket.recv(1024).decode()
        
        if not offer_receive:
            break
        
        try:
            offer_receive = json.loads(offer_receive)
            
            product_index = int(offer_receive['code'])

            if product_index < 0 or product_index >= len(products):
                connection_socket.send("Invalid index".encode())
                continue
            
            selected_product = products[product_index]
            
            if 0 < selected_product['price'] <= 25:
                if 1 < attempts <= 2:
                    calc = 0.12
                elif attempts == 1:
                    calc = 0.14
                elif attempts == 0:
                    calc = 0.16
                else:
                    calc = 0.1
            elif 25 < selected_product['price'] <= 75:
                if 1 < attempts <= 2:
                    calc = 0.165
                elif attempts == 1:
                    calc = 0.18
                elif attempts == 0:
                    calc = 0.2
                else:
                    calc = 0.15
            else:
                if 1 < attempts <= 2:
                    calc = 0.21
                elif attempts == 1:
                    calc = 0.23
                elif attempts == 0:
                    calc = 0.25
                else:
                    calc = 0.2

            
            print("Calc: ", calc)
            
            offer_value = selected_product['price'] * calc
            
            if offer_receive['price'] >= (selected_product['price'] - offer_value):
                response = "Your offer has been accepted! You ordered the product {} for {}".format(selected_product['name'], offer_receive['price'])
                connection_socket.send(response.encode())
                break
            else:
                attempts -= 1
                response = "Offer refused! You have {} more bid(s)".format(attempts)

                counterproposal = "Counterproposal: You can take {} for {:.2f}. Deal closed?".format(selected_product['name'], selected_product['price'] - offer_value)
                connection_socket.send(counterproposal.encode())

                answer = connection_socket.recv(1024).decode().strip().lower()
                
                if answer in ["yes", "sim", "ss", "si", "s"]:
                    response = "Proposal accepted! You ordered the product {} for {:.2f}".format(selected_product['name'], selected_product['price'] - offer_value)
                    connection_socket.send(response.encode())
                    break
                elif answer in ["no", "não", "nn", "nao", "n"]:
                    response = "Proposal refused! Please make another offer."
                    connection_socket.send(response.encode())
            
        except ValueError:
            connection_socket.send("Invalid entry. Please send a valid number.".encode())
    
    connection_socket.close()