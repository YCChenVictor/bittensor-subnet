import json
import numpy as np
from model.market_price_movement_prediction.data_utils import columns_to_remove
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.callbacks import ModelCheckpoint


class ModelTrainer:
    def __init__(self, target, features, steps, feature_tickers, store_model_path):
        self.feature_tickers = feature_tickers
        self.steps = steps
        self.target = target
        self.features = features
        self.processed_features = None
        self.store_model_path = store_model_path
        self.matched_target_features = None
        with open("model_config.json", "r") as file:
            self.model_config = json.load(file)

    def build_model(self, input_shape):
        # Build the model
        model = Sequential()

        # First LSTM layer with dropout for regularization
        model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
        model.add(Dropout(0.5))  # Dropout layer to reduce overfitting
        model.add(BatchNormalization())  # Batch normalization to stabilize training

        # Flatten the output of the LSTM layer
        model.add(LSTM(128, return_sequences=False))
        model.add(Dropout(0.5))  # Dropout to prevent overfitting

        # Dense layers
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))  # Dropout to prevent overfitting

        # Output layer for classification (softmax activation function)
        model.add(Dense(1, activation='linear'))

        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae'])

        return model

    def process_data(self):
        self.target.set_index("time", inplace=True)
        self.features.set_index("forecast_at", inplace=True)
        processed_features = self.features.drop(
            columns=columns_to_remove
        )
        self.processed_features = processed_features

    def match(self):
        print("matching")
        matched_target_features = {}
        start_index = 0
        end_index = self.steps
        while end_index < len(self.processed_features):
            current_features = self.processed_features.iloc[start_index:end_index]
            forecast_at = current_features.iloc[-1].name
            target_movement = self.target.loc[forecast_at]
            start_index += 1
            end_index += 1
            matched_target_features[forecast_at] = [target_movement, current_features]
        self.matched_target_features = matched_target_features

    def train(self):
        Y_train = []
        X_train = []
        for key, value in self.matched_target_features.items():
            modified_feature = (
                value[1]
                .to_numpy()
            )
            Y_train.append(value[0].values)
            X_train.append(modified_feature)

        X_train = np.array(X_train)
        Y_train = np.array(Y_train)

        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train.reshape(-1, X_train.shape[-1])).reshape(X_train.shape)
        model = self.build_model((X_train.shape[1], X_train.shape[2]))
        checkpoint = ModelCheckpoint(filepath=self.store_model_path, monitor='accuracy', save_best_only=False, save_weights_only=False, save_freq='epoch')
        model.fit(
            X_train,
            Y_train,
            epochs=self.model_config["epochs"],
            batch_size=self.model_config["batch_size"],
            validation_split=0.2,
            callbacks=[checkpoint]
        )

        model_path = self.store_model_path
        model.save(model_path)
