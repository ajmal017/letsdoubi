#!/usr/bin/env python
__author__ = "Kevin & Samuel"
__version__ = "0.1.0"

# Object that return all forecast result

import datetime
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web


class forecast_result(object):
    name = ""
    flag = ""
    accuracy = ""
    gain_chance = ""

    def __init__(self, name, flag, accuracy,gain_chance):
        self.name = name
        self.flag = flag
        self.accuracy = accuracy
        self.gain_chance = gain_chance

def make_result(name, flag, accuracy,gain_chance):
    forecasted_result = forecast_result(name, flag, accuracy,gain_chance)
    return forecasted_result