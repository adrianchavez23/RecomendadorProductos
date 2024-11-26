from flask import Flask, request, jsonify, render_template
from flask_cors  import CORS, cross_origin 

import numpy as np
import pandas as pd
from joblib import load
import category_encoders as ce
from sklearn.preprocessing import StandardScaler
import json

pd.set_option('display.max_rows', None)  # Display all rows
pd.set_option('display.max_columns', None)  # Display all columns


#CARGAR CLIENTES
with open('data_dict.json', 'r') as file:
    clientes = json.load(file)

with open('data_dict_clusters.json', 'r') as file:
    clientes_clusters = json.load(file)

#CARGAR MODELOS
model_cluster0 = load('models/model_cluster0.pkl')
model_cluster1 = load('models/model_cluster1.pkl')
model_cluster2 = load('models/model_cluster2.pkl')
model_cluster3 = load('models/model_cluster3.pkl')
model_cluster4 = load('models/model_cluster4.pkl')
model_cluster5 = load('models/model_cluster5.pkl')
model_cluster6 = load('models/model_cluster6.pkl')
model_cluster7 = load('models/model_cluster7.pkl')
model_cluster8 = load('models/model_cluster8.pkl')
model_cluster9 = load('models/model_cluster9.pkl')

models = [model_cluster0, model_cluster1, model_cluster2, model_cluster3, model_cluster4, model_cluster5, model_cluster6, model_cluster7, model_cluster8, model_cluster9]

#CARGAR TARGET ENCODERS
target_encoder_cluster0_loaded = load('encoders/target_encoder_cluster0.pkl')
target_encoder_cluster1_loaded = load('encoders/target_encoder_cluster1.pkl')
target_encoder_cluster2_loaded = load('encoders/target_encoder_cluster2.pkl')
target_encoder_cluster3_loaded = load('encoders/target_encoder_cluster3.pkl')
target_encoder_cluster4_loaded = load('encoders/target_encoder_cluster4.pkl')
target_encoder_cluster5_loaded = load('encoders/target_encoder_cluster5.pkl')
target_encoder_cluster6_loaded = load('encoders/target_encoder_cluster6.pkl')
target_encoder_cluster7_loaded = load('encoders/target_encoder_cluster7.pkl')
target_encoder_cluster8_loaded = load('encoders/target_encoder_cluster8.pkl')
target_encoder_cluster9_loaded = load('encoders/target_encoder_cluster9.pkl')

target_encoders = [target_encoder_cluster0_loaded, 
                    target_encoder_cluster1_loaded, 
                    target_encoder_cluster2_loaded, 
                    target_encoder_cluster3_loaded, 
                    target_encoder_cluster4_loaded, 
                    target_encoder_cluster5_loaded,
                    target_encoder_cluster6_loaded,
                    target_encoder_cluster7_loaded,
                    target_encoder_cluster8_loaded,
                    target_encoder_cluster9_loaded ]

#CARGAR LABEL ENCODERS
label_encoder_cluster0_loaded = load('encoders/label_encoder_cluster0.pkl')
label_encoder_cluster1_loaded = load('encoders/label_encoder_cluster1.pkl')
label_encoder_cluster2_loaded = load('encoders/label_encoder_cluster2.pkl')
label_encoder_cluster3_loaded = load('encoders/label_encoder_cluster3.pkl')
label_encoder_cluster4_loaded = load('encoders/label_encoder_cluster4.pkl')
label_encoder_cluster5_loaded = load('encoders/label_encoder_cluster5.pkl')
label_encoder_cluster6_loaded = load('encoders/label_encoder_cluster6.pkl')
label_encoder_cluster7_loaded = load('encoders/label_encoder_cluster7.pkl')
label_encoder_cluster8_loaded = load('encoders/label_encoder_cluster8.pkl')
label_encoder_cluster9_loaded = load('encoders/label_encoder_cluster9.pkl')

label_encoders = [label_encoder_cluster0_loaded,
                  label_encoder_cluster1_loaded,
                  label_encoder_cluster2_loaded,
                  label_encoder_cluster3_loaded,
                  label_encoder_cluster4_loaded,
                  label_encoder_cluster5_loaded,
                  label_encoder_cluster6_loaded,
                  label_encoder_cluster7_loaded,
                  label_encoder_cluster8_loaded,
                  label_encoder_cluster9_loaded]

#CARGAR SCALERS
scaler_cluster_0_loaded = load('encoders/scaler_cluster0.pkl')
scaler_cluster_1_loaded = load('encoders/scaler_cluster1.pkl')
scaler_cluster_2_loaded = load('encoders/scaler_cluster2.pkl')
scaler_cluster_3_loaded = load('encoders/scaler_cluster3.pkl')
scaler_cluster_4_loaded = load('encoders/scaler_cluster4.pkl')
scaler_cluster_5_loaded = load('encoders/scaler_cluster5.pkl')
scaler_cluster_6_loaded = load('encoders/scaler_cluster6.pkl')
scaler_cluster_7_loaded = load('encoders/scaler_cluster7.pkl')
scaler_cluster_8_loaded = load('encoders/scaler_cluster8.pkl')
scaler_cluster_9_loaded = load('encoders/scaler_cluster9.pkl')

scalers = [scaler_cluster_0_loaded,
           scaler_cluster_1_loaded,
           scaler_cluster_2_loaded,
           scaler_cluster_3_loaded,
           scaler_cluster_4_loaded,
           scaler_cluster_5_loaded,
           scaler_cluster_6_loaded,
           scaler_cluster_7_loaded,
           scaler_cluster_8_loaded,
           scaler_cluster_9_loaded]

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type,Authorization'

resultados = [] 


def encode_data(data, client_data, numero_cluster):
    
    clients_df = pd.DataFrame([client_data])
    df = pd.DataFrame([data])

    combined_df = pd.concat([clients_df, df], axis=1)
    
    cols_to_encode_target = ['ProdKey', 'Brand', 'Size', 'Flavor', 'Container', 'ProductType', 'sub_canal_comercial']

    target_encoder_loaded = target_encoders[numero_cluster]
    label_encoder_loaded = label_encoders[numero_cluster]
    scaler_loaded = scalers[numero_cluster]

    # Encode the features using target encoder
    encoded_data = target_encoder_loaded.transform(combined_df[cols_to_encode_target])

    # Encode the 'Returnability' column using label encoder
    encoded_data['Returnability'] = label_encoder_loaded.transform(df['Returnability'])

    encoded_data['Productos_Por_Empaque'] = df['Productos_Por_Empaque']
    encoded_data['MLSize'] = df['MLSize']
    encoded_data['industry_customer_size'] = clients_df['industry_customer_size']
    encoded_data['pob_e_300m'] = clients_df['pob_e_300m']
    encoded_data['pc_habitacional_mixta_300m'] = clients_df['pc_habitacional_mixta_300m']
    encoded_data['ingreso_maximo_300m'] = clients_df['ingreso_maximo_300m']
    encoded_data['pob_ab_300m'] = clients_df['pob_ab_300m']
    encoded_data['prob_inter_mod_300m'] = clients_df['prob_inter_mod_300m']
    encoded_data['autos_hora_18'] = clients_df['autos_hora_18']
    encoded_data['ingreso_rentas_300m'] = clients_df['ingreso_rentas_300m']
    encoded_data['flo_sem_cmas_300m'] = clients_df['flo_sem_cmas_300m']

    #Fill NaN. Buscar como hacerle para que el filling de NaNs sea igual que en el DataHandling
    encoded_data = encoded_data.fillna(0)
    
    encoded_data_standarized = pd.DataFrame(scaler_loaded.transform(encoded_data), columns=encoded_data.columns)
    
    
    return encoded_data_standarized



@app.route("/",methods=['GET'])
def formulario():
    return render_template('interfaz.html')



@app.route('/predict', methods=['POST'])
@cross_origin()
def prediccion():
  if request.method == 'POST':
        user_input_data = request.get_json()

        user_input_data['Productos_Por_Empaque'] = int(user_input_data['Productos_Por_Empaque'])
        user_input_data['MLSize'] = int(user_input_data['MLSize'])

        for i in clientes:
            if str(i['CustomerId']) in clientes_clusters:


                cluster_cliente = clientes_clusters[str(i['CustomerId'])]

                input_value = encode_data(user_input_data, i, cluster_cliente)
                
                model = models[cluster_cliente]

                predictions = model.predict(input_value)
                probabilities = model_cluster9.predict_proba(input_value)

                print("Predictions:", predictions)
                print("Probabilities:", probabilities)

                resultado = {'CustomerId': i['CustomerId'], 'Porcentaje': probabilities[0][1]}
                resultados.append(resultado)

        resultados_ordenados = sorted(resultados, key=lambda x: x['Porcentaje'], reverse=True)


        return jsonify({'status': 1, 'message': 'Success', 'resultados': resultados_ordenados[:10], 'userdata': user_input_data}) 
    #invalido 
  return jsonify({'status': 0, 'message': 'Invalid request'})



if __name__ == "__main__":
    app.run(debug=True, port=3001)

  