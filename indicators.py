import numpy as np


def moving_average_calc(values, window, exp=True):
    if not exp:
        weights = np.repeat(1.0, window)/window
        ma = np.convolve(values, weights, 'valid')
    else:
        weights = np.exp(np.linspace(-1., 0. , window))
        weights /= weights.sum()
        ma = np.convolve(values, weights, mode='full')[:len(values)]
        ma[:window] = ma[window]
    return ma


def macd_calc(x, slow=26, fast=12):
    ema_slow = moving_average_calc(x, slow)
    ema_fast = moving_average_calc(x, fast)
    return ema_fast-ema_slow


def rsi_calc(price, n):
    gain = (price-price.shift(1)).fillna(0)

    def rsi_helper(p):
        avg_gain = p[p>0].sum()/n
        avg_loss = -p[p<0].sum()/n 
        rs = avg_gain/avg_loss
        return 100 - 100/(1+rs)

    return gain.rolling(n).apply(rsi_helper)
