import tensorflow as tf
import os
import numpy as np
from scipy import signal, stats
class AFDetector:
    """
    Template class for af detector submission.
    """
    def __init__(self, sample_rate):
        """
        Initialize the af detector.

        Params:
        -----
        sample_rate: int
            Sampling frequency of the inputs.
        """
        base_dir = os.getcwd()
        # load model
        self.sample_rate = sample_rate
        model_name = "model.h5"
        model_dir = os.path.join(base_dir, model_name)
        self.model = tf.keras.models.load_model(model_dir)

        # load filters
        self.sos = signal.butter(4, 15, 'hp', fs=sample_rate, output='sos')
    def classify(self, ecg):
        """
        Gets raw ECG signal and return the AF Classification result.

        Params:
        -----
        ecg: np.array,
            Raw 1-lead ECG signal

        Returns:
        -----
        AF classification: int,
            This is the af classification result.
                0 = Not AF
                1 = AF
                everything else = Not classified
        """
        preprocessed_ecg = self.preprocess(ecg)
        model_classifications = self.get_model_classification(preprocessed_ecg)
        return tf.convert_to_tensor(model_classifications)
    def preprocess(self, ecg):
        """
        Gets the ecg signal and prepares it for classification. Filtering,
        windowing and etc can be done here.
        """
        if len(ecg) > 5000:
            if self.sample_rate != 250:
                t = len(ecg)/self.sample_rate
                new_f = int(np.round(t*250))
                ecg = signal.resample(ecg, new_f)
        else:
            new_data = ecg
            while len(new_data) <= 5000:
                new_data = np.append(new_data, ecg)
            ecg = new_data[:5000]
            self.fg = ecg
            
        ecg_segments = []
        start = 0
        while (start + 5000) <= len(ecg):
            segment = ecg[start:5000 + start]
            segment = stats.zscore(segment)
            segment = signal.sosfilt(self.sos,segment)
            segment = segment.reshape(-1,1)
            ecg_segments.append(segment)
            start += 1250
            return np.array(ecg_segments)

    def get_model_classification(self, ecg):
        """
        Gets the preprocessed inputs and returns model outputs.
        """
        prediction = self.model.predict(ecg)
        prediction = np.round(prediction).astype(int)
        classification = sum(prediction)
        return 1 if classification > 0 else 0