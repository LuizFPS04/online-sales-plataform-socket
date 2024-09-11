from socket import *
import json

server_name = 'localhost'  # Nome ou endereço do servidor (no caso, local)
server_port = 12000  # Porta na qual o servidor está escutando
print("---------- WELCOME TO CAR DEALERSHIP ----------")
# Solicita ao usuário que digite "SHOW CARS" para listar os carros
show_list = str(input("Type 'SHOW CARS' to list our cars: "))

# Verifica se o usuário digitou qualquer variação permitida para exibir a lista de carros
while show_list.lower() in ["show cars", "show", "list cars", "list", "show car", "car", "list car"]:

    # Cria um socket TCP para o cliente
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_name, server_port))  # Conecta ao servidor na porta e endereço especificados

    # Recebe a lista de carros do servidor e decodifica o JSON
    cars = json.loads(client_socket.recv(1024).decode())

    bids_number = 1
    attempts = 3  # Define o número de tentativas para ofertas do cliente

    # Exibe a lista de carros disponíveis
    print("\nSelect a car: ")
    for index, car in enumerate(cars):
        print(f"{index + 1}. {car['name']} (#{car['code']}) - R${car['price']:.2f}")
        
    # Solicita ao cliente que escolha o carro pelo índice
    car_index = int(input("Enter with number: ")) - 1

    # Verifica se o índice do carro é válido, caso contrário solicita um novo
    while car_index < 0 or car_index >= len(cars):
        print("Invalid code. Please enter a valid car number.")
        car_index = int(input("Enter with number: ")) - 1

    print(f"You selected the car {cars[car_index]['name']} (#{cars[car_index]['code']}) that costs R${cars[car_index]['price']:.2f}!") # Imprime o carro selecionado

    # Loop de tentativas de ofertas do cliente
    while attempts > 0:
        try:
            offer_price = float(input(f"Place your {bids_number}° bid: "))  # Solicita ao cliente que faça uma oferta
            
            if offer_price <= 0:  # Verifica se a oferta é válida (positiva)
                print("Invalid bid price. Please enter a positive value.")
                continue
            
            # Cria o dicionário que será enviado com o índice e o preço da oferta
            offer_client = {
                'index': car_index,
                'price': offer_price
            }
            
            # Envia a oferta codificada em JSON ao servidor
            client_socket.send(json.dumps(offer_client).encode())
            
            # Recebe a resposta do servidor e a decodifica
            server_response = client_socket.recv(1024).decode()
            print(server_response)  # Exibe a resposta do servidor
            
            # Se a oferta foi aceita, encerra o loop
            if "accepted" in server_response.lower():
                print("Offer accepted!")
                break
            
            # Caso o servidor envie uma contraproposta
            elif "Counterproposal" in server_response:
                # Pergunta ao cliente se ele aceita a contraproposta
                response_client = input("Do you accept the counterproposal? (yes/no): ").lower()
                while (not (response_client in ["yes", "sim", "ss", "si", "s", "no", "não", "nn", "nao", "n"])):
                    response_client = input("Do you accept the counterproposal? (yes/no): ").lower()
                
                # Envia a resposta do cliente ao servidor (aceita ou não a contraproposta)
                client_socket.send(response_client.encode())
                
                # Recebe a resposta final do servidor
                final_response = client_socket.recv(1024).decode()
                print(final_response)
                
                # Se o cliente aceitou a contraproposta, encerra a conexão
                if "accepted" in final_response.lower():
                    print("Counterproposal accepted!")
                    break
                else:
                    bids_number += 1 # Aumenta número de lances
                    attempts -= 1  # Diminui o número de tentativas caso a contraproposta seja recusada
            
            else:
                bids_number += 1 # Aumenta número de lances
                attempts -= 1  # Diminui o número de tentativas caso a oferta seja recusada
        
        except ValueError:
            print("Invalid input. Please enter a valid number.")  # Trata a exceção

    # Solicita novamente a listagem dos carros se o cliente quiser continuar após a oferta
    show_list = str(input("\nType 'SHOW CARS' to list our cars: "))

# Encerra a conexão com o servidor após o término do loop
print("Closing connection.")
client_socket.close()