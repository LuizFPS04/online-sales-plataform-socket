# online-sales-plataform-socket

O objetivo deste trabalho é desenvolver uma plataforma de vendas online com negociação de preço, utilizando Python e comunicação via socket.

**Redes de Computadores II**

## Estratégia de Negociação

A estratégia de negociação no código envolve uma interação entre o cliente e o servidor, onde o cliente tenta fazer uma oferta de compra de um carro. O servidor responde de acordo com certas regras, incluindo aceitar a oferta, rejeitá-la ou fazer uma contraproposta.

### 1. Listagem de Carros

- O cliente solicita ao servidor a lista de carros. O servidor envia uma lista de carros, cada um com código, nome e preço.  
- O cliente seleciona um carro e inicia o processo de negociação.

### 2. Primeira Oferta

- O cliente faz uma oferta para um carro selecionado, informando o preço que está disposto a pagar. Ele possui 3 chances para fechar o negócio.

### 3. Respostas do Servidor

- O servidor analisa a oferta feita pelo cliente e pode responder de três formas:

#### a) Aceitação da Oferta

- Se o lance do cliente for alto o suficiente (acima do mínimo calculado pelo servidor), o servidor aceita o lance e encerra a negociação.

#### b) Rejeição da Oferta e Contraproposta

- Se a oferta do cliente for considerada muito baixa, o servidor irá rejeitá-la. No entanto, o servidor faz uma contraproposta, oferecendo o carro por um preço um pouco inferior ao preço original, mas ainda superior à oferta do cliente.  
- O valor da contraproposta depende de uma fórmula baseada no número de tentativas restantes. Quanto menor o número de tentativas restantes, maior será o desconto oferecido.

#### c) Rejeição

- Se a oferta do cliente for muito baixa e ele tiver esgotado todas as tentativas, o servidor se recusa a negociar sem dar outra chance, encerrando o processo.

### 4. Decisão do Cliente

Quando o cliente recebe uma contraproposta, ele tem a opção de aceitar ou rejeitar:

- **Aceitar**: Caso o cliente aceite a contraproposta, o servidor confirma a negociação e encerra a sessão, vendendo o carro pelo valor oferecido.
- **Rejeitar**: Caso o cliente rejeite a contraproposta, ele poderá fazer uma nova oferta até que todas as tentativas se esgotem.

### 5. Estratégia de Desconto por Tentativa

O servidor aplica diferentes porcentagens de desconto com base no número de tentativas restantes, incentivando os clientes a concluir a transação mais cedo. Os descontos oferecidos aumentam a cada nova tentativa.
