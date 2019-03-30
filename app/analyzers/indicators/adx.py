
""" ADX Indicator
"""

import math

import pandas
from talib import abstract

from analyzers.utils import IndicatorUtils


class ADX(IndicatorUtils):
    def analyze(self, historical_data, period_count=14,
                signal=['adx'], hot_thresh=None, cold_thresh=None):
        """Performs an ADX analysis on the historical data

        Args:
            historical_data (list): A mADXix of historical OHCLV data.
            period_count (int, optional): Defaults to 14. The number of data points to consider for
                our ADX.
            signal (list, optional): Defaults to ADX. The indicator line to check hot/cold
                against.
            hot_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to purchase.
            cold_thresh (float, optional): Defaults to None. The threshold at which this might be
                good to sell.

        Returns:
            pandas.DataFrame: A dataframe containing the indicators and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)
        adx_values = abstract.ADX(dataframe, period_count).to_frame()
        adx_values.dropna(how='all', inplace=True)
        adx_values.rename(columns={adx_values.columns[0]: 'adx'}, inplace=True)

        if adx_values[signal[0]].shape[0]:
            adx_values['is_hot'] = adx_values[signal[0]] > hot_thresh
            adx_values['is_cold'] = adx_values[signal[0]] <= cold_thresh

        return adx_values