import tensorflow as tf

class AFDetector:
    """
    Template class for af detector submission.
    """
    def __init__(self, sample_rate):
        """
        Initialize the af detector.

        Params:
        -----
        sample_rate: int,
            Sampling frequency of the inputs.
        """

        # load model

        # load filters

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
        return tf.argmax(model_classifications)

    def preprocess(self, ecg):
        """
        Gets the ecg signal and prepares it for classification. Filtering,
        windowing and etc can be done here.
        """
        return None

    def get_model_classification(self, ecg):
        """
        Gets the preprocessed inputs and returns model outputs.
        """
        return None