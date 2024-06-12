from scripts._can_process import CanProcess
import can


def main():
    label_attck = True
    can_proc = CanProcess()
    # Inicializar o processamento de dados e o modelo
    # model_filepath = 'scripts/trained_models/classe_02/boost_model.pkl' #mono-classe
    model_filepath = 'scripts/trained_models/classe_03/boost_model.pkl' #multi-classe
    # model_filepath = '/home/rsb6/Desktop/LIVE/algorithms/scripts/trained_models/classe_02/mlp_model.weights.h5'
    input_dim = 8  
    name = input('if mlp model, write: mlp: ')
    model = can_proc.load_trained_model(model_filepath, input_dim, model_name=name)
    
    # Configuração do barramento CAN (ajuste conforme necessário)
    bus = can.interface.Bus(bustype='socketcan', channel='vcan0', bitrate=500000)
    
    print("Listening on CAN bus...")
    while True:
        msg = bus.recv()  # Recebe uma mensagem CAN
        if msg is not None:
            # Processar a mensagem e fazer a previsão
            predict = can_proc.process_message(msg)
            prediction = model.predict(predict)
            try:
                # Classificar como ataque ou benigno
                if prediction >= 0.5 and not label_attck:
                    print(f"ALERT: Potential attack detected! Message: {msg}")
        
                # Classificar o tipo de ataque
                elif prediction == 0 and label_attck:
                    print(f"Message is benign: {msg}")
                elif prediction == 1 and label_attck:
                    print(f"Message is dos_attck: {msg}")
                    
                elif prediction == 2 and label_attck:
                    print(f"Message is fuzzy_attck: {msg}")
                    
                elif prediction == 3 and label_attck:
                    print(f"Message is masquerade_attck: {msg}")
                    
                elif prediction == 4 and label_attck:
                    print(f"Message is spoofed_attck: {msg}")
                    
                elif prediction == 5 and label_attck:
                    print(f"Message is supress_attck: {msg}")
                else:
                    print(f"Message is unknown attack: {msg}")
                    
                    
                    
            except TypeError:
                # Classificar o tipo de ataque
                if prediction == 'benign' \
                    or prediction == 0:
                    print(f"Message is benign: {msg}")
                    
                elif prediction == 'dos_attck' \
                    or prediction == 1:
                    print(f"Message is dos_attck: {msg}")
                    
                elif prediction == 'fuzzy_attck' \
                    or prediction == 2:
                    print(f"Message is fuzzy_attck: {msg}")
                    
                elif prediction == 'masquerade_attck' \
                    or prediction == 3:
                    print(f"Message is masquerade_attck: {msg}")
                    
                elif prediction == 'spoofed_attck' \
                    or prediction == 4:
                    print(f"Message is spoofed_attck: {msg}")
                    
                elif prediction == 'supress_attck':
                    print(f"Message is supress_attck: {msg}")
                
                    
                
                
                

if __name__ == "__main__":
    main()
