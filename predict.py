import pandas as pd
import numpy as np
from keras.models import load_model
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


def predict_weather(input_date):
    # Load the pre-trained time-series forecasting model in h5 format
    model = load_model('model.h5')

    # Load the scaler object used to scale the data during training
    scaler = MinMaxScaler()

    # Load the training data and fit the scaler object to the data
    df = pd.read_csv('london_dataset.csv')
    # Select only the required columns
    df = df[['datetime', 'tempmax', 'tempmin', 'temp', 'humidity', 'cloudcover', 'precip', 'windspeed']]
    column_names = df.columns.tolist()

    # Parse datetime column as index
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    train_data = scaler.fit_transform(df)


    # Prepare your input data
    # For example, assume your input data is a sequence of 7 normalized values with 7 features
    input_data = np.array([[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7], 
                        [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8], 
                        [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], 
                        [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], 
                        [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 0.1], 
                        [0.6, 0.7, 0.8, 0.9, 1.0, 0.1, 0.2], 
                        [0.7, 0.8, 0.9, 1.0, 0.1, 0.2, 0.3]])

    input_data = np.reshape(input_data, (1, 7, 7)) # Reshape the input data to match the format of the pre-trained model

    input_date = input_date.strftime("%Y-%m-%d")
    # Define the future dates you want to predict
    future_dates = pd.date_range(start='2022-01-02', end=input_date)

    # Use the pre-trained model to predict the future values
    predicted_values = []
    for i in range(len(future_dates)):
        prediction = model.predict(input_data)
        predicted_value = scaler.inverse_transform(prediction)
        predicted_values.append(predicted_value)
        prediction = np.reshape(prediction, (1, 1, prediction.shape[1])) # Reshape the prediction array to match the input_data shape
        input_data = np.concatenate((input_data[:,1:,:], prediction), axis=1) # Shift the input data by 1 day


    return predicted_values[len(future_dates)-1][0].tolist()
    
