import serial
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
import time

ser = serial.Serial('COM3', 9600)

def read_data():
    while True:
        data = ser.readline().decode('utf-8')
        try:
            json_data = json.loads(data)
        except ValueError:
            continue
        return json_data

data = []
for i in range(7*24*60//5):
    json_data = read_data()
    data.append(json_data)

df = pd.DataFrame(data)

X = df[['temperature', 'humidity']]
y = df.index
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean squared error: {mse}")

writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Data')
writer.save()

while True:
    future_data = []
    for i in range(60//5):
        json_data = read_data()
        future_data.append(json_data)
        df = df.iloc[1:]
        df = df.append(json_data, ignore_index=True)
        X_pred = df[['temperature', 'humidity']].iloc[-1:]
        y_pred = model.predict(X_pred)
        df = df.append({'temperature': X_pred['temperature'].iloc[0], 'humidity': X_pred['humidity'].iloc[0], 'predicted': y_pred[0]}, ignore_index=True)

    writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Data')
    writer.save()

    fig, ax = plt.subplots()
    ax.plot(df.index, df['temperature'], label='Temperature')
    ax.plot(df.index, df['humidity'], label='Humidity')
    ax.plot(df.index, df['predicted'], label='Predicted')
    ax.legend()
    ax.set_xlabel('Time (minutes)')
    ax.set_ylabel('Value')
    plt.show()
    time.sleep(1)

ser.close()
