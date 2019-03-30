""" ATR Indicator
"""

import math

import pandas
from talib import abstract

from analyzers.utils import IndicatorUtils


class ATR(IndicatorUtils):
    def analyze(self, historical_data, period_count=14,
                signal=['atr'], hot_thresh=None, cold_thresh=None):
        """Performs an ATR analysis on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            period_count (int, optional): Defaults to 14. The number of data points to consider for
                our ATR.
            signal (list, optional): Defaults to ATR. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)
        atr_values = abstract.ATR(dataframe, period_count).to_frame()
        atr_values.dropna(how='all', inplace=True)
        atr_values.rename(columns={atr_values.columns[0]: 'atr'}, inplace=True)

        mean = atr_values['atr'].mean()
        std_dev = atr_values['atr'].std()

        atr_upper_limit = mean+std_dev
        atr_lower_limit = mean-std_dev
        atr = atr_values['atr'][-1]

        if atr < atr_lower_limit or atr > atr_upper_limit:
            is_hot = True
            is_cold = False 
        else:
            is_hot = False
            is_cold = True    

        if atr_values[signal[0]].shape[0]:
            atr_values['mean'] = mean
            atr_values['std_dev'] = std_dev
            atr_values['is_hot'] = is_hot
            atr_values['is_cold'] = is_cold

        return atr_values
