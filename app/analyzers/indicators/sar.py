""" MACD Indicator
"""

import math

import pandas
from talib import abstract

from analyzers.utils import IndicatorUtils


class SAR(IndicatorUtils):
    def analyze(self, historical_data, signal=['sar'], hot_thresh=None, cold_thresh=None):
        """Performs a macd analysis on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to macd. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)
        sar_values = abstract.SAR(dataframe).iloc[:]
        sar_values.dropna(how='all', inplace=True)

        if sar_values[signal[0]].shape[0]:
            sar_values['is_hot'] = sar_values[signal[0]] > hot_thresh
            sar_values['is_cold'] = sar_values[signal[0]] < cold_thresh

        return sar_values
