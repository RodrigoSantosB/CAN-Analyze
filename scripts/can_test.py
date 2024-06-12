from scripts._can_libs_ import *
# from scripts._datas import DataProcessing

# Carregar o modelo treinado
def load_trained_model(filepath, input_dim):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])
    model.load_weights(filepath)
    return model

# Função para converter a mensagem CAN em uma representação numérica
def encode_can_message(data):
    # Converter cada byte da mensagem CAN para seu valor decimal
    data_numeric = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
    return np.array(data_numeric).reshape(1, -1)

# Função para processar uma mensagem CAN
# Função para processar uma mensagem CAN
def process_message(msg):
    # Extrair e processar a mensagem CAN
    data = msg.data.hex().upper()  # Converte os dados para hexadecimal
    data_numeric = encode_can_message(data)
    print(data_numeric)
    # data_scaled = scaler.transform(data_numeric)  # Escalar os dados
    return data_numeric

# Função principal para escutar o barramento CAN e classificar as mensagens
def main():
    # # Inicializar o processamento de dados e o modelo
    # model_filepath = 'mlp_model.weights.h5'
    # input_dim = 1  # Ajuste conforme necessário
    # model = load_trained_model(model_filepath, input_dim)
    
    # Configuração do barramento CAN (ajuste conforme necessário)
    # bus = can.interface.Bus(bustype='socketcan', channel='can0', bitrate=500000)
    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
    
    
    print("Listening on CAN bus...")
    while True:
        msg = bus.recv()  # Recebe uma mensagem CAN
        if msg is not None:
            # Processar a mensagem e fazer a previsão
            predict = process_message(msg)
            # time.sleep(0.1)  # Pequeno atraso antes de tentar enviar novamente
            # print(predict)
            # model = joblib.load('/home/rsb6/Desktop/LIVE/algorithms/naive_model.pkl')
            # prediction = model.predict(predict)
            
            # # # Classificar como ataque ou benigno
            # if prediction >= 0.5:
            #     print(f"ALERT: Potential attack detected! Message: {msg}")
            # else:
            #     print(f"Message is benign: {msg}")

if __name__ == "__main__":
    main()
