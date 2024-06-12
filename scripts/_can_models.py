from scripts._can_libs_ import *

class ModelsTraining:
    def __init__(self) -> None:
        pass
        
    # Definição do modelo MLP
    def __create_mlp(self, input_dim, mult_label=False):
        model = Sequential()
        model.add(Dense(64, input_dim=input_dim, 
                            activation='relu'))
        model.add(Dense(32, activation='relu'))
        
        if mult_label:
            model.add(Dense(5, activation='softmax'))  # Para classificação binária
            model.compile(optimizer=Adam(learning_rate=0.001), 
                        loss='categorical_crossentropy', 
                        metrics=['accuracy'])
        else:
            model.add(Dense(1, activation='sigmoid'))  # Para classificação binária
            model.compile(optimizer=Adam(learning_rate=0.001), 
                        loss='binary_crossentropy', 
                        metrics=['accuracy'])
        return model

    # Função para salvar os pesos do modelo
    def __save_model_weights(self, model, filepath=None):
        if filepath is None:
            path_model = 'mlp_model.weights.h5'
        else:
            path_model = filepath + '/mlp_model.weights.h5'
        model.save_weights(path_model)

    # Função para carregar os pesos do modelo
    def __load_model_weights(self, model, filepath=None):
        if filepath is None:
            path_model = 'mlp_model.weights.h5'
        else:
            path_model = filepath
        return model.load_weights(path_model)


    def mlp_train(self,x_train, y_train, path_save_model=None, mult_label=False, epochs=100, batch_size=32):
        # Criando e treinando o modelo
        input_dim = x_train.shape[1]
        mlp_model = self.__create_mlp(input_dim, mult_label)

        # Definindo o callback de early stopping
        early_stopping = EarlyStopping(monitor='val_loss', patience=8, restore_best_weights=True)

        # Definindo o callback de TensorBoard
        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        # Treinando o modelo com early stopping e TensorBoard
        mlp_model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2, 
                  callbacks=[early_stopping, tensorboard_callback])

        # Salvando os pesos do modelo
        self.__save_model_weights(mlp_model, path_save_model)


    def load_mlp_model(self, x_train, x_test, y_test, path_save_model=None):
        input_dim = x_train.shape[1]
    
        # Criando um novo modelo e carregando os pesos
        model = self.__create_mlp(input_dim)
        
        if path_save_model is None:
            path_model = 'mlp_model.weights.h5'
        else:
            path_model = path_save_model
        
        self.__load_model_weights(model, path_model)

        # Verificando se os pesos foram carregados corretamente
        loss, accuracy = model.evaluate(x_test, y_test)
        print(f'Loss: {loss}, Accuracy: {accuracy}')
        return model

        
    
    # NAIVE BAYES NET
    def __create_naive(self, x_train, y_train):
        # # Criação dos modelos base
        naive = GaussianNB()
        naive.fit(x_train, y_train)
        return naive

    def naive_byes_train(self, x_train, x_test, y_train, y_test, path_export=None):      
        
        if path_export is None:
            path_model = 'naive_model.pkl'
        else:
            path_model = path_export + '/naive_model.pkl'
          
        naive = self.__create_naive(x_train, y_train)
        predict_naive  = naive.predict(x_test)
        joblib.dump(naive, path_model)
        print(classification_report(y_test, predict_naive))
        
        
    # RANDOM FOREST NET
    def __create_forest(self, x_train, y_train):
        # # Criação dos modelos base
        forest = RandomForestClassifier(n_estimators=100, 
                                        random_state=42)
        forest.fit(x_train, y_train)
        return forest

    def random_forest_train(self, x_train, x_test, y_train, y_test, path_export=None):      
        
        if path_export is None:
            path_model = 'forest_model.pkl'
        else:
            path_model = path_export + '/forest_model.pkl'
            
        forest = self.__create_forest(x_train, y_train)
        predict_forest  = forest.predict(x_test)
        joblib.dump(forest, path_model)
        print(classification_report(y_test, predict_forest))
        
    
    # GRADIENTE BOOSTING NET
    def __create_boost(self, x_train, y_train):
        # # Criação dos modelos base
        boost = GradientBoostingClassifier(n_estimators=10, 
                                           random_state=42)
        boost.fit(x_train, y_train)
        return boost

    def gradient_boost_train(self, x_train, x_test, y_train, y_test, path_export=None):   
        
        if path_export is None:
            path_model = 'boost_model.pkl'
        else:
            path_model = path_export + '/boost_model.pkl'
                 
        boost = self.__create_boost(x_train, y_train)
        predict_boost  = boost.predict(x_test)
        joblib.dump(boost, path_model)
        print(classification_report(y_test, predict_boost))
        
        
    
    # ISOLATION FOREST (NAO SUPERVISIONADO)
    def __create_isolation(self, x_train, contamination=0.1):
        # # Criação dos modelos base
        isolation = IsolationForest(contamination=contamination)  # contamination é a proporção de anomalias esperadas
        isolation.fit(x_train)
        return isolation

    def isolation_forest_train(self, x_train, x_test, path_export=None):   
        
        if path_export is None:
            path_model = 'isolation_model.pkl'
        else:
            path_model = path_export + '/isolation_model.pkl'
                 
        isolation = self.__create_isolation(x_train)
        predict_isolation  = isolation.predict(x_test)
        
        # Examinando as previsões
        for i in range(len(predict_isolation)):
            count = 0
            if predict_isolation[i] == -1:
                count += 1
        joblib.dump(isolation, path_model)
        print(f'qdte de anomalias encontradas: {count}')
        