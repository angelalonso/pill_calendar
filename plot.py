import pandas as pd
from pandas import DataFrame

import matplotlib.pyplot as plt

df = pd.read_csv('Calendar.csv', parse_dates=True)

df.plot()
plt.show()
