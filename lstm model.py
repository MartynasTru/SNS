import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import TimeSeriesSplit
from keras.models import Sequential
from keras.layers import Dense, LSTM, Bidirectional, Dropout
import matplotlib.pyplot as plt

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

# Cross-validation
tscv = TimeSeriesSplit(n_splits=5)
validation_errors = []

# Loop through the time series splits
for train_index, val_index in tscv.split(x_train):
    x_train_fold, x_val_fold = x_train[train_index], x_train[val_index]
    y_train_fold, y_val_fold = y_train[train_index], y_train[val_index]

    # Initialize the LSTM model
    model = Sequential()
    model.add(Bidirectional(LSTM(units=50, return_sequences=True), input_shape=(x_train_fold.shape[1], data.shape[1])))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(units=50)))
    model.add(Dropout(0.2))
    model.add(Dense(units=data.shape[1]))

    # Compile and train the model
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train_fold, y_train_fold, epochs=50, batch_size=32, verbose=0)

    # Evaluate the model on the validation set
    val_error = model.evaluate(x_val_fold, y_val_fold, verbose=0)
    validation_errors.append(val_error)

# Calculate the average validation error across all folds
average_validation_error = np.mean(validation_errors)
print(f'Average validation error: {average_validation_error}')


# Evaluate the model on the test set
test_error = model.evaluate(x_test, y_test, verbose=0)
print(f'Test error: {test_error}')

# Make predictions on the test set
y_pred = model.predict(x_test)

# Inverse transform the scaled data back to the original values
y_test = scaler.inverse_transform(y_test)
y_pred = scaler.inverse_transform(y_pred)

# Calculate the root mean squared error
rmse = np.sqrt(np.mean(np.square(y_test - y_pred)))
print(f'Root Mean Squared Error (RMSE): {rmse}')

# Plot the predicted and true values
plt.plot(y_test, label="True values")
plt.plot(y_pred, label="Predicted values")
plt.legend()
plt.show() 