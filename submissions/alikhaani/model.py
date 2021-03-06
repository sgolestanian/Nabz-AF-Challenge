import tensorflow as tf
from tensorflow.keras.models import load_model
from scipy.io import loadmat
# Please run "pip install neurokit2" to install NeuroKit2
import neurokit2.signal as nsig
import numpy as np

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
        self.default_rate = sample_rate

        # load model
        self.model = load_model("AF-detection.h5")

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
        return tf.squeeze(tf.argmax(model_classifications))

    def preprocess(self, ecg):
        """
        Gets the ecg signal and prepares it for classification. Filtering,
        windowing and etc can be done here.
        """

        sys_fs = 360

        if sys_fs != self.default_rate:
            s = nsig.signal_resample(ecg,sampling_rate=self.default_rate,desired_sampling_rate=360 )
            ecg = s

        maxlen = 2160

        if len(ecg) > maxlen:
            sig_len = len(ecg)
            new_len = sig_len - maxlen
            sig = ecg[new_len:]
        elif len(ecg) < maxlen:
            sig = self.fit_tolength(ecg,maxlen)
        elif len(ecg) == maxlen:
            sig = ecg
            

        sig2 = sig.reshape(1,2160)
        sig2 = sig2.astype('float32')

        return sig2

    def fit_tolength(source, length):
        target = np.zeros([length])
        w_l = min(source.size, target.size)
        target[0:w_l] = source[0:w_l]
        return target


    def get_model_classification(self, ecg):
        """
        Gets the preprocessed inputs and returns model outputs.
        """
        predict = self.model.predict(ecg)

        return predict