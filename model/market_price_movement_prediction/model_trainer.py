import json
import numpy as np
from data_utils import columns_to_remove
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam


class ModelTrainer:
    def __init__(self, target, features, steps, feature_tickers, store_model_path):
        self.feature_tickers = feature_tickers
        self.steps = steps
        self.target = target
        self.features = features
        self.store_model_path = store_model_path
        self.match_target_features = None
        with open("model_config.json", "r") as file:
            self.model_config = json.load(file)

    def match(self):
        print("matching")
        match_target_features = {}
        start_index = 0
        end_index = self.steps
        while end_index < len(self.features):
            current_features = self.features.iloc[start_index:end_index]
            forecast_at = current_features.iloc[-1]["forecast_at"]
            target_movement = self.target[self.target["Time"] == forecast_at]
            start_index += 1
            end_index += 1
            match_target_features[forecast_at] = [target_movement, current_features]
        self.match_target_features = match_target_features

    def build_model(self, X_train):
        # Build the model
        model = Sequential()

        # First LSTM layer with dropout for regularization
        model.add(LSTM(64, input_shape=X_train[0].shape, return_sequences=True))
        model.add(Dropout(0.2))  # Dropout layer to reduce overfitting
        model.add(BatchNormalization())  # Batch normalization to stabilize training

        # Second LSTM layer
        model.add(LSTM(64))
        model.add(Dropout(0.2))  # Dropout for regularization
        model.add(BatchNormalization())  # Batch normalization

        # Dense layers
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.2))  # Dropout to prevent overfitting

        # Output layer for regression (no activation function)
        model.add(Dense(1))

        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mae'])

        return model

    def train(self):
        Y_train = []
        X_train = []
        for key, value in self.match_target_features.items():
            modified_feature = (
                value[1]
                .drop(
                    columns=columns_to_remove
                )
                .to_numpy()
            )
            Y_train.append(value[0].iat[0, value[0].columns.get_loc("Movement")])
            X_train.append(modified_feature)

        X_train = np.array(X_train)
        Y_train = np.array(Y_train).reshape(-1, 1)

        model = self.build_model(X_train)
        model.fit(
            X_train,
            Y_train,
            epochs=self.model_config["epochs"],
            batch_size=self.model_config["batch_size"],
        )

        model_path = self.store_model_path
        model.save(model_path)
