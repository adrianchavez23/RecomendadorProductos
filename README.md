# Recomendador de productos

Se utiliza un servidor Flask para la implementación. 
Este servidor despliega la interfaz de usuario. En esta interfaz, el usuario ingresa las características de un producto y hace una petición al servidor para obtener las predicciones.
En la ruta de /predict en servicios.py es donde se procesa el input del usuario, para luego entrar a un bloque iterativo donde se concatena con la información del cliente actual en la iteración.
A este nuevo dataframe se le tienen que aplicar transformaciones necesarias para que que tenga la misma forma que los datos de entrenamiento. Esto se hace por medio de encoders importados previamente entrenados en base al cluster del cliente actual. 
Una vez obtenido el dataframe de predicción, se puede hacer la predicción al modelo del cluster del cliente actual.
Estas predicciones se guardan en un diccionario de resultados para luego ordenarlas de mayor a menor. La respuesta del servidar es una lista de las Top 10 CLientes con mejor probabilidad de éxito.

