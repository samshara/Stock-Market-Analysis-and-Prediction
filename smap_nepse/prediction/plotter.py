import sys
sys.path.insert(0, '../../smap_nepse')

import pandas as pd
import numpy as np
import prepareInput as pi
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.finance as finance
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.mlab as mlab
import matplotlib.font_manager as font_manager

from pandas.tools.plotting import table
from preprocessing import moreIndicators as indi

__author__ = "Semanta Bhandari"
__copyright__ = ""
__credits__ = ["Sameer Rai","Sumit Shrestha","Sankalpa Timilsina"]
__license__ = ""
__version__ = "0.1"
__email__ = "semantabhandari@gmail.com"


def indicator_plot(df):
    index = df.index
    df.index = range(len(df.index))
    df.columns = ['Transactions','Traded_Shares','Traded_Amount','High','Low','Close']
    df = indi.EMA(df, 20)
    df = indi.RSI(df, 14)
    df = indi.MOM(df, 10)
    df = indi.MA(df, 100)
    df = indi.MA(df, 20)

    df.index = index
    last = df[-1:]
    df = df.drop(df.columns[:5], axis=1)
    # print(df.describe())
    print(df.corr())
    # print(df.RSI_10)
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
     
    textsize = 9
    left, width = 0.1, 0.8
    rect1 = [left, 0.7, width, 0.2]
    rect2 = [left, 0.3, width, 0.4]
    rect3 = [left, 0.1, width, 0.2]
     
    fig = plt.figure(facecolor='white')
    axescolor = '#f6f6f6'  # the axes background color
     
    ax1 = fig.add_axes(rect1, axisbg=axescolor)  # left, bottom, width, height
    ax2 = fig.add_axes(rect2, axisbg=axescolor, sharex=ax1)
    ax2t = ax2.twinx()
    ax3 = fig.add_axes(rect3, axisbg=axescolor, sharex=ax1)
     
    rsi = df.RSI_14*100
    fillcolor = 'darkgoldenrod'
    ticker = 'NABIL'
    ax1.plot(df.index, rsi, color=fillcolor)
    ax1.axhline(70, color=fillcolor)
    ax1.axhline(30, color=fillcolor)
    ax1.fill_between(df.index, rsi, 70, where=(rsi >= 70), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.fill_between(df.index, rsi, 30, where=(rsi <= 30), facecolor=fillcolor, edgecolor=fillcolor)
    ax1.text(0.6, 0.9, '>70 = overbought', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.text(0.6, 0.1, '<30 = oversold', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_ylim(0, 100)
    ax1.set_yticks([30, 70])
    ax1.text(0.025, 0.95, 'RSI (14)', va='top', transform=ax1.transAxes, fontsize=textsize)
    ax1.set_title('%s daily' % ticker)
    # plt.figure()
    # df.plot()
    ma20 = df['MA_20']
    ma100 = df['MA_100']
    linema100, = ax2.plot(df.index, ma100, color='green', lw=2, label='MA (100)', linestyle = '--')
    linema20, = ax2.plot(df.index, ma20, color='blue', lw=2, label='MA (20)', linestyle = '-.')
    close, = ax2.plot(df.index, df.Close, color='red', lw=2, label='Close')
     
     
    s = '%s H:%1.2f L:%1.2f C:%1.2f' % (
        last.index[0].date(), last.High, last.Low, last.Close)
    t4 = ax2.text(0.3, 0.9, s, transform=ax2.transAxes, fontsize=textsize)
     
    props = font_manager.FontProperties(size=10)
    leg = ax2.legend(loc='center left', shadow=True, fancybox=True, prop=props)
    leg.get_frame().set_alpha(0.5)
     
    ax3.plot(df.index, df.Momentum_10)
    ax3.text(0.025, 0.95, 'Momentum (10)', va='top',
             transform=ax3.transAxes, fontsize=textsize)
    plt.show()

#if __name__ == "__main__" :
dataframe = pi.load_data_frame('NABIL.csv')
indicator_plot(dataframe[1000:])
