from scripts._can_libs_ import *

class DataProcessing:
    def __init__(self) -> None:
        pass
    
    def dataset_transform(self, path):
        columns = ['Timestamp', 'Can_Interface', 'CAN_ID', 'Message', 'Label']
        files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
        dfs = [pd.read_csv(os.path.join(path, arquivo), sep=' ', 
                        names=columns, engine='python') for arquivo in files]
        
        df_concat = pd.concat(dfs, ignore_index=True)
        df_concat = df_concat.drop(['Timestamp', 'Can_Interface', 'CAN_ID'], axis=1)
        
        # Completar as mensagens com zeros à direita se forem menores que 16 caracteres (8 bytes)
        df_concat['Message'] = df_concat['Message'].apply(lambda x: x.ljust(16, '0') if len(x) < 16 else x)
        
        
        
        # Converter cada byte de cada mensagem CAN para seu valor decimal
        data_array = df_concat.iloc[:,0].values
        
        tam = len(df_concat.columns)
        target = df_concat.iloc[:,(tam-1)].values

        
        data_numeric = []
        for data in data_array:
            numeric_values = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
            data_numeric.append(numeric_values)

        data_numeric = np.array(data_numeric)
        
        return df_concat, data_numeric, target

    def encode_dataframe(self, path, classify_to_binary=True):
        df, data_numeric, target = self.dataset_transform(path)
        datas = df.copy ( deep = True )
        tam = len(df.columns)

        # Dicionário para armazenar os codificadores de rótulos
        label_encoders = {}
        # Substituir 'benign' por 0 e outras labels por 1
        if classify_to_binary:
            df['Label'] = df['Label'].apply(lambda x: 0 if x == 'benign' else 1)
        else:
            # mapeamento de strings para números
            label_mapping = {
                'benign': 0,
                'dos_attck': 1,
                'fuzzy_attck': 2,
                'masquerade_attck': 3,
                'spoofed_attck':4,
                'supress_attck':5
                }
            
            # substituição usando o mapeamento
            df['Label'] = df['Label'].apply(lambda x: label_mapping.get(x, x))
            
        # Verifica se há uma coluna chamada 'Timestamp' e a remove temporariamente
        columns_to_encode = df.columns.difference(['Timestamp'])
        
        # Transforma os dados categóricos em numéricos para todas as colunas, exceto 'Timestamp'
        label_encoder = LabelEncoder()
        for column in columns_to_encode:
            df[column] = label_encoder.fit_transform(df[column])
            label_encoders[column] = label_encoder
        predicted = df.iloc[:, 0:(tam-1)].values
        if classify_to_binary:
            target  = df.iloc[:, (tam-1)].values
        return datas, predicted, data_numeric, target


    def escalation(self, path):
        predicted, target = self.encode_dataframe(path)
        scaler = StandardScaler()  # Instancia o StandardScaler
        df_escaled = scaler.fit_transform(predicted)  # Aplica o fit_transform aos valores do DataFrame
        return df_escaled, target
    
    