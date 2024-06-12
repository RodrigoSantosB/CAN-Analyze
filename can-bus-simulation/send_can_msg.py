import os

def read_data_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    can_messages = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 3:
            can_id = parts[2].split('#')[0]
            data = parts[2].split('#')[1]
            can_messages.append((can_id, data))
    return can_messages

def send_can_messages(can_messages, interface='vcan0'):
    for can_id, data in can_messages:
        command = f'cansend {interface} {can_id}#{data}'
        os.system(command)
        print(f'Sent: {command}')

PATH = '/home/rsb6/Desktop/LIVE/algorithms/CAN-Analyze/can-bus-simulation/'

fuzzy_path = PATH + 'fuzzy_atack.txt'
dos_path   = PATH + 'dos_atack.txt'
all_path   = PATH + 'all_atack.txt'

choice = input('choice one attck type:(fuzzy | dos | all): ')
if choice.upper() == 'FUZZY':
    file_path = fuzzy_path
elif choice.upper() == 'DOS':
    file_path = dos_path
elif choice.upper() == 'ALL':
    file_path = all_path
    
can_messages = read_data_file(file_path)
send_can_messages(can_messages, interface='vcan0')
