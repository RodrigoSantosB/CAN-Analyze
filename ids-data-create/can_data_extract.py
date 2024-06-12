class DataExtract:
    
    def __init__(self):
        pass
    
    def extract_data_ids(self, data_file):
        with open(data_file, 'r') as file:
            lines = file.readlines()
        
        data_dict = {}
        
        for line in lines:
            parts = line.split()
            if len(parts) < 3:
                continue
            
            data_id = parts[2]
            data_dict[data_id] = None
        return data_dict


    def save_dict(self, output_file, data_dict):
        with open(output_file, 'w') as file:
            file.write("{\n")
            for key in data_dict:
                file.write(f"'{key}',\n")
            file.write("}\n")
            
    
    # script_rotulador.py
    def label_data(self, input_data, attack_type='dos'):
        with open(input_data, 'r') as file:
            lines = file.readlines()
        
        labeled_data = []
        
        for line in lines:
            parts = line.split()
            if len(parts) < 4:
                continue
    
            id_data = parts[3]  # seleciona a parte do id e campo de dados
            if id_data == 'T':
                parts[3] = attack_type
            else:
                parts[3] = 'benign'
                
            labeled_line = ' '.join(parts)
            labeled_data.append(labeled_line)
        
        # Separar ID e Dados
        separated_data = []
        for labeled_line in labeled_data:
            parts = labeled_line.split()
            id_data = parts[2]
            if '#' in id_data:
                id_part, data_part = id_data.split('#')
                new_line = f"{parts[0]} {parts[1]} {id_part} {data_part} {parts[3]}"
                separated_data.append(new_line)
            else:
                separated_data.append(labeled_line)  # caso não tenha '#', adicionar a linha como está
        
        return separated_data


    def save_labeled_data(self, output_file, labeled_data):
        with open(output_file, 'w') as file:
            for line in labeled_data:
                file.write(f"{line}\n")


    def read_file_to_variable(self, file_path):
        with open(file_path, 'r') as file:
            content = file.read().strip()
        return content
