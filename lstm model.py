import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Dropout
from keras.optimizers import Adam

# Load the dataset
data = pd.read_csv("weather_data.csv", parse_dates=["datetime"], index_col="datetime")

# Preprocessing
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data)

# Create sequences
def create_sequences(data, seq_length):
    x, y = [], []
    for i in range(len(data) - seq_length):
        x.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(x), np.array(y)

seq_length = 24
x, y = create_sequences(data_scaled, seq_length)

# Train-test split
train_size = int(0.8 * len(x))
x_train, x_test = x[:train_size], x[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

# Define the parameter grid for the grid search
param_grid = {
    'seq_length': [24, 48],
    'num_units': [50, 100],
    'dropout': [0.2, 0.5],
    'learning_rate': [0.001, 0.01, 0.1],
    'batch_size': [32, 64],
    'epochs': [50, 100]
}

# Initialize the LSTM model
def create_model(seq_length, num_units, dropout, learning_rate):
    model = Sequential()
    model.add(Bidirectional(LSTM(units=num_units, return_sequences=True), input_shape=(seq_length, data.shape[1])))
    model.add(Dropout(dropout))
    model.add(Bidirectional(LSTM(units=num_units)))
    model.add(Dropout(dropout))
    model.add(Dense(units=data.shape[1]))
    optimizer = Adam(lr=learning_rate)
    model.compile(optimizer=optimizer, loss='mean_squared_error')
    return model

# Define the time series cross-validation
tscv = TimeSeriesSplit(n_splits=5)

# Initialize the grid search
grid_search = GridSearchCV(estimator=KerasRegressor(build_fn=create_model), param_grid=param_grid, cv=tscv, verbose=1)

# Fit the grid search to the training data
grid_search_results = grid_search.fit(x_train, y_train)

# Print the best parameters and validation error
print(f"Best Parameters: {grid_search_results.best_params_}")
print(f"Validation Error: {grid_search_results.best_score_}")

# Train the final model on the full training dataset using the best hyperparameters
best_params = grid_search_results.best_params_
model = create_model(best_params['seq_length'], best_params['num_units'], best_params['dropout'], best_params['learning_rate'])
model.fit(x_train, y_train, epochs=best_params['epochs'], batch_size=best_params['batch_size'], verbose=1)

# Evaluate the final model on the test dataset
test_error = model.evaluate(x_test, y_test, verbose=0)
print(f"Test Error: {test_error}")
