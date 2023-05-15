import os
import pandas as pd
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Model

def load_patient_data(main_directory):

    # Get the list of patient folders
    patient_folders = [folder for folder in os.listdir(main_directory)]

    march_data = []  # Initialize empty data frame for march data
    leg_extension_data = []  # Initialize empty data frame for leg extension data
    knee_flexion_data = []  # Initialize empty data frame for knee flexion data

    for patient_folder in patient_folders:
        patient_path = os.path.join(main_directory, patient_folder)  # Path to the patient folder

        march_files = [file for file in os.listdir(patient_path) if file.__contains__("mar")]
        march_patient_data = pd.concat([pd.read_csv(os.path.join(patient_path, file)) for file in march_files]) # Load CSV data for the patient
        march_data.append(march_patient_data)  # Append patient data to march data frame

        leg_extension_files = [file for file in os.listdir(patient_path) if file.__contains__("pie")]
        leg_extension_patient_data = pd.concat([pd.read_csv(os.path.join(patient_path, file)) for file in leg_extension_files]) # Load CSV data for the patient
        leg_extension_data.append(leg_extension_patient_data)  # Append patient data to leg extension data frame

        knee_flexion_files = [file for file in os.listdir(patient_path) if file.__contains__("sen")]
        knee_flexion_patient_data = pd.concat([pd.read_csv(os.path.join(patient_path, file)) for file in knee_flexion_files]) # Load CSV data for the patient
        knee_flexion_data.append(knee_flexion_patient_data)  # Append patient data to knee flexion data frame

    march_data = pd.concat(march_data)  # Concatenate all march data frames
    leg_extension_data = pd.concat(leg_extension_data)  # Concatenate all leg extension data frames
    knee_flexion_data = pd.concat(knee_flexion_data)  # Concatenate all knee flexion data frames

    
    return march_data,leg_extension_data,knee_flexion_data

# Example usage
main_directory = "C:/EMG/CSV_N"
g_march_data,g_leg_extension_data,g_knee_flexion_data = load_patient_data(os.path.join(main_directory))

column_index = 4
if column_index < len(g_march_data.columns):
    g_march_data = g_march_data.drop(g_march_data.columns[column_index], axis=1)

if column_index < len(g_leg_extension_data.columns):
    g_leg_extension_data = g_leg_extension_data.drop(g_leg_extension_data.columns[column_index], axis=1)

if column_index < len(g_knee_flexion_data.columns):
    g_knee_flexion_data = g_knee_flexion_data.drop(g_knee_flexion_data.columns[column_index], axis=1)

g_march_data_train,g_march_data_test=train_test_split(g_march_data,test_size=0.2)
g_leg_extension_data_train,g_leg_extension_data_test=train_test_split(g_leg_extension_data,test_size=0.2)
g_knee_flexion_data_train,g_knee_flexion_data_test=train_test_split(g_knee_flexion_data,test_size=0.2)

num_features=4

input_shape = (num_features,)

# Define the encoder architecture
input_data = Input(shape=input_shape)
encoded = Dense(64, activation='relu')(input_data)
encoded = Dense(32, activation='relu')(encoded)
encoded = Dense(16, activation='relu')(encoded)

# Define the decoder architecture
decoded = Dense(32, activation='relu')(encoded)
decoded = Dense(64, activation='relu')(decoded)
decoded = Dense(num_features, activation='sigmoid')(decoded)

# Create the autoencoder model
autoencoder = Model(input_data, decoded)

# Compile the model
autoencoder.compile(optimizer='adam', loss='mse')

# Train the autoencoder using your good EMG data
autoencoder.fit(g_march_data_train, g_march_data_train, epochs=10, batch_size=32)