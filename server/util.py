import pickle
import json
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load data
path = r"C:\Users\HP\Desktop\look\HPM1\cleaned_data.csv"
df = pd.read_csv(path)

# Split data
X = df.drop('price', axis=1)
y = df['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=10)

# Feature scaling
sc = StandardScaler()
sc.fit(X_train)
X_train = sc.transform(X_train)
X_test = sc.transform(X_test)

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, total_sqft, bath, balcony, bhk):
    # Ensure pandas is imported
    import pandas as pd

    # Create a DataFrame with one row containing all features
    input_data = pd.DataFrame([[total_sqft, bath, balcony, bhk] + [0] * (len(__data_columns) - 4)],
                              columns=__data_columns)

    # Set the location dummy to 1 if it exists in our columns
    if location in __data_columns:
        input_data[location] = 1

    # Scale the input data using the same scaler used for training data
    input_data_scaled = sc.transform(input_data)

    # Predict the price using the trained stacking model
    return round(__model.predict(input_data_scaled)[0], 2)

def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    # Load the columns from the JSON file
    with open("./server/artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[4:]  # first 4 columns are sqft, bath, balcony, bhk

    # Load the trained model from the pickle file
    global __model
    if __model is None:
        with open('./server/artifacts/banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)

    print("loading saved artifacts...done")

def get_location_names():
    return __locations

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3, 3)) # 81.17
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2, 2)) # 76.72
    print(get_estimated_price('Kalhalli', 1000, 2, 2, 2))  # other location 66.96
    print(get_estimated_price('Ejipura', 1000, 2, 2, 2))  # other location 66.96
