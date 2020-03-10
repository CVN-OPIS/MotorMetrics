import math

import numpy as np

from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.metrics import mean_squared_log_error


def flatten_extra_dims(quant):
    return quant.flatten()


def r2(y_true, y_pred):
    assert y_true.shape == y_pred.shape

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)
    return r2_score(y_true, y_pred)


def rmsle(y_true, y_pred):
    assert y_true.shape == y_pred.shape
    assert y_true.min() >= -1 and y_true.max() <= 1
    assert y_pred.min() >= -1 and y_pred.max() <= 1

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)
    terms_to_sum = (np.log(y_pred + 1) - np.log(y_true + 1))**2
    return (sum(terms_to_sum) * (1.0/len(y_true))) ** 0.5

def rmse(y_true, y_pred):
    assert y_true.shape == y_pred.shape

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)

    return np.sqrt(((y_pred - y_true) ** 2).mean())


def mae(y_true, y_pred):
    assert y_true.shape == y_pred.shape

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)
    return mean_absolute_error(y_true, y_pred)


def smape(y_true, y_pred):
    assert y_true.shape == y_pred.shape

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)
    return 100.0/ len(y_true) * np.sum(2.0 * np.abs(y_pred - y_true) / \
           (np.abs(y_true) + np.abs(y_pred) + 0.00001))


def sc(signal):
    signal = flatten_extra_dims(signal)
    return np.mean(abs(signal[1:] - signal[:-1]))


def smape_vs_sc(y_true, y_pred, window):
    assert window >= 1
    assert y_true.shape == y_pred.shape

    y_true = flatten_extra_dims(y_true)
    y_pred = flatten_extra_dims(y_pred)
    smape_vs_sc_all_windows = []

    for i in range(0, y_true.shape[0]):
        if i + window + 1 < y_true.shape[0]:
            smape_val = smape(y_true[i: i + window], y_pred[i: i + window])
            sc_val = sc(y_true[i : i + window])
            smape_vs_sc_all_windows.append([smape_val, sc_val])

    return np.asarray(smape_vs_sc_all_windows)


def sc_mse(y_pred, y_true):
    assert y_true.shape == y_pred.shape

    sc_y_true = np.mean(np.abs(y_true[:,:,1:] - y_true[:,:,:-1]), axis=2)
    mse = np.mean((y_pred - y_true) ** 2.0, axis=2)
    loss = sc_y_true * mse
    loss = np.mean(loss)
    return loss