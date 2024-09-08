from socket import *
import json

server_port = 12000  # Define a porta do servidor
server_socket = socket(AF_INET, SOCK_STREAM)  # Cria o socket do servidor usando o protocolo TCP
server_socket.bind(('', server_port))  # Associa o socket a todas as interfaces de rede locais e à porta definida
server_socket.listen(1)  # Coloca o servidor em modo de escuta, aguardando conexões

# Lista de modelos de carros com seus códigos e preços
car_models = [
    {'code': 101, 'name': "Toyota Corolla", 'price': 95000},
    {'code': 102, 'name': "Honda Civic", 'price': 100000},
    {'code': 103, 'name': "Ford Mustang", 'price': 280000},
    {'code': 104, 'name': "Chevrolet Camaro", 'price': 300000},
    {'code': 105, 'name': "BMW 320i", 'price': 200000},
    {'code': 106, 'name': "Audi A4", 'price': 220000},
    {'code': 107, 'name': "Mercedes-Benz C-Class", 'price': 250000},
    {'code': 108, 'name': "Volkswagen Golf", 'price': 120000},
    {'code': 109, 'name': "Nissan Sentra", 'price': 90000},
    {'code': 110, 'name': "Hyundai Elantra", 'price': 85000},
    {'code': 111, 'name': "Jeep Compass", 'price': 180000},
    {'code': 112, 'name': "Tesla Model 3", 'price': 350000},
    {'code': 113, 'name': "Land Rover Discovery", 'price': 400000},
    {'code': 114, 'name': "Volvo XC60", 'price': 300000},
    {'code': 115, 'name': "Porsche 911", 'price': 900000},
]

# Loop principal do servidor, que permanece ativo enquanto houver conexões
while True:
    connection_socket, addr = server_socket.accept()  # Aceita uma conexão de um cliente
    print('Server is running.')  # Exibe uma mensagem informando que o servidor está ativo
    
    # Envia a lista de carros para o cliente
    connection_socket.send(json.dumps(car_models).encode())

    attempts = 3  # Define o número de tentativas que o cliente tem para fazer ofertas
	
    # Loop que processa as ofertas do cliente enquanto houver tentativas restantes
    while attempts > 0:
        offer_receive = connection_socket.recv(1024).decode()  # Recebe a oferta do cliente
        
        if not offer_receive:  # Verifica se a oferta recebida é vazia (fim de conexão)
            break
        
        try:
            offer_receive = json.loads(offer_receive)  # Decodifica a oferta JSON do cliente
            car_index = int(offer_receive['index'])  # Obtém o índice do carro escolhido pelo cliente

            # Verifica se o índice está dentro do intervalo válido
            if car_index < 0 or car_index >= len(car_models):
                connection_socket.send("Invalid index".encode())
                continue
            
            selected_car = car_models[car_index]  # Seleciona o carro com base no índice

            # Define a taxa de desconto com base no preço do carro e nas tentativas restantes
            if 0 < selected_car['price'] <= 150000:
                if 1 < attempts <= 2:
                    calc = 0.1
                elif attempts == 1:
                    calc = 0.12
                elif attempts == 0:
                    calc = 0.14
                else:
                    calc = 0.08
            elif 150000 < selected_car['price'] <= 300000:
                if 1 < attempts <= 2:
                    calc = 0.15
                elif attempts == 1:
                    calc = 0.16
                elif attempts == 0:
                    calc = 0.175
                else:
                    calc = 0.13
            else:
                if 1 < attempts <= 2:
                    calc = 0.19
                elif attempts == 1:
                    calc = 0.2
                elif attempts == 0:
                    calc = 0.22
                else:
                    calc = 0.18
            
            offer_value = selected_car['price'] * calc  # Calcula o valor da contraoferta

            # Caso a oferta do cliente seja maior que o preço do carro
            if offer_receive['price'] > selected_car['price']:
                response = "Your offer was greater than the value of the car {} (#{})! So you just got it for R${:.2f}".format(selected_car['name'], selected_car['code'], selected_car['price'])
                connection_socket.send(response.encode())  # Envia a resposta de aceitação
                break
            
            # Verifica se a oferta do cliente está dentro da contraoferta calculada
            if offer_receive['price'] >= (selected_car['price'] - offer_value):
                response = "Your offer has been accepted! You ordered the car {} (#{}) for R${:.2f}".format(selected_car['name'], selected_car['code'], offer_receive['price'])
                connection_socket.send(response.encode())  # Envia resposta de aceitação
                break
            else:
                attempts -= 1  # Diminui o número de tentativas restantes
                response = "Offer refused! You have {} more bid(s)".format(attempts)

                # Envia uma contraoferta para o cliente
                counterproposal = "Counterproposal: You can take {} (#{}) for R${:.2f}. Deal closed?".format(selected_car['name'], selected_car['code'], selected_car['price'] - offer_value)
                connection_socket.send(counterproposal.encode())

                # Recebe a resposta do cliente à contraoferta
                counterproposal_accept = connection_socket.recv(1024).decode().strip().lower()
                
                # Verifica se o cliente aceitou ou recusou a contraoferta
                if counterproposal_accept in ["yes", "sim", "ss", "si", "s"]:
                    response = "Proposal accepted! You ordered the car {} (#{}) for R${:.2f}".format(selected_car['name'], selected_car['code'], selected_car['price'] - offer_value)
                    connection_socket.send(response.encode())
                    break
                elif counterproposal_accept in ["no", "não", "nn", "nao", "n"]:
                    response = "Proposal refused! Please make another offer."
                    connection_socket.send(response.encode())
            
        except ValueError:
            connection_socket.send("Invalid entry. Please send a valid number.".encode())  # Trata a exceção
    
    connection_socket.close()  # Fecha a conexão com o cliente após as tentativas