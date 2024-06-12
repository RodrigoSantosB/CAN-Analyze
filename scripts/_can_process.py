from scripts._can_libs_ import *

class CanProcess:
    def __init__(self) -> None:
        pass
        
    # Converter a mensagem CAN em uma representação numérica
    def __encode_can_message(self, data):
        # Converter cada byte da mensagem CAN para seu valor decimal
        data_numeric = [int(data[i:i+2], 16) for i in range(0, len(data), 2)]
        return np.array(data_numeric).reshape(1, -1)


    # Carregar o model treinado
    def load_trained_model(self, filepath, input_dim, model_name='others'):

        if model_name == 'mlp':
            model = Sequential()
            model.add(Dense(64, input_dim=input_dim, activation='relu'))
            model.add(Dense(32, activation='relu'))
            model.add(Dense(1, activation='sigmoid'))
            
            model.compile(  optimizer=Adam(learning_rate=0.001), 
                            loss='binary_crossentropy', 
                            metrics=['accuracy'])
            
            model.load_weights(filepath)
            return model
        else:
            model = joblib.load(filepath)
            return model
        
    # Plotar matriz de confusão    
    def plot_confusion_matrix(self, model, x_test, y_test, 
                            labels=['Benign', 'Attack']):
        ''' y_true: dados reais, y_pred: saida prevista pelo model'''
        # Fazer previsões
        predictions = model.predict(x_test)
        predictions = (predictions > 0.5).astype(int)  # Convertendo previsões para 0 ou 1

        # Gerar a matriz de confusão
        cm = confusion_matrix(y_test, predictions)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, 
                                        display_labels=labels)

        # Plotar a matriz de confusão
        disp.plot()
        plt.show()
        # Mostrar figura

    # Plotar distribuićão de classe
    def plot_class_distribution(self, datas):
        hist1 =  px.histogram (datas,  x = "Label", nbins=60) 
        hist1.update_layout(width=800,
                            height=500,
                            title_text='Distribuição dos attcks') 
        hist1.show()
        
        
    # Verificar overfitting e plotar a curva ROC
    def evaluate_overfitting_and_plot_roc(self, model_path, X_train, 
                                          y_train, X_test, y_test):
        
        # Carregar o model
        model = joblib.load(model_path)
        
        # Previsões no conjunto de treino
        y_train_pred = model.predict(X_train)
        y_train_prob = model.predict_proba(X_train)[:, 1]
        
        # Previsões no conjunto de teste
        y_test_pred = model.predict(X_test)
        y_test_prob = model.predict_proba(X_test)[:, 1]
        
        # Avaliar a acurácia
        acuracia_train = accuracy_score(y_train, y_train_pred)
        acuracia_test = accuracy_score(y_test, y_test_pred)
        
        print(53*'*')
        print(f'Acurácia no conjunto de treino: {acuracia_train}')
        print(53*'*')
        print()
        print(53*'*')
        print(f'Acurácia no conjunto de teste: {acuracia_test}')
        print(53*'*')
        print()
        
        # Relatórios de classificação
        print('Relatório de classificação - Conjunto de Treino:')
        print(53*'*')
        print(53*'-')
        print(classification_report(y_train, y_train_pred))
        print()
        print(53*'-')
        print(53*'*')
        print('Relatório de classificação - Conjunto de Teste:')
        print(classification_report(y_test, y_test_pred))
        print(53*'-')
        
        # Calcular as curvas ROC
        curve = input('Plote ROC curve? (yes | no): ')
        if curve.upper() == 'YES':
            fpr_train, tpr_train, _ = roc_curve(y_train, y_train_prob)
            roc_auc_train = auc(fpr_train, tpr_train)
            
            fpr_test, tpr_test, _ = roc_curve(y_test, y_test_prob)
            roc_auc_test = auc(fpr_test, tpr_test)
            
            # Criar as curvas ROC com Plotly
            fig = go.Figure()

            fig.add_trace(go.Scatter(x=fpr_train, y=tpr_train,
                                    mode='lines',
                                    name=f'Curva ROC Treino (área = {roc_auc_train:.2f})',
                                    line=dict(color='blue', width=2)))

            fig.add_trace(go.Scatter(x=fpr_test, y=tpr_test,
                                    mode='lines',
                                    name=f'Curva ROC Teste (área = {roc_auc_test:.2f})',
                                    line=dict(color='red', width=2)))

            fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1],
                                    mode='lines',
                                    line=dict(color='gray', width=2, dash='dash'),
                                    showlegend=False))

            fig.update_layout(title='Curva ROC',
                            xaxis_title='Taxa de Falsos Positivos',
                            yaxis_title='Taxa de Verdadeiros Positivos',
                            xaxis=dict(range=[0, 1], constrain='domain'),
                            yaxis=dict(range=[0, 1.05], constrain='domain'),
                            legend=dict(x=0.4, y=0.1),
                            width=700, height=500)
            
            # Mostrar a figura
            fig.show()
        matrix = input('Plot confuse matix? (yes | no): ')
        if matrix.upper() == 'YES':
            self.plot_confusion_matrix(model, X_test, y_test)
        else:
            pass
            
    
    # Processar uma mensagem CAN
    def process_message(self, msg):
        # Extrair e processar a mensagem CAN
        data = msg.data.hex().upper()  # Converte os dados para hexadecimal
        data_numeric = self.__encode_can_message(data)
        return data_numeric
    

