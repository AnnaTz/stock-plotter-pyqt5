import numpy as np
import matplotlib.lines as mlines
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams.update({'font.size': 11})
matplotlib.use('Qt5Agg')
from matplotlib.ticker import FuncFormatter
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
from indicators import macd_calc, moving_average_calc, rsi_calc


def candlestick_chart(ax, quotes, width=0.2, colorup='k', colordown='r', alpha=1.0):
    OFFSET = width/2.0
    lines = []
    patches = []
    for q in quotes:
        t, open, close, high, low = q[:5]
        if close>=open :
            color = colorup
            lower = open
            height = close-open
        else:
            color = colordown
            lower = close
            height = open-close
        vline = mlines.Line2D(
            xdata=(t, t), ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True)
        rect = mpatches.Rectangle(
            xy = (t-OFFSET, lower),
            width = width,
            height = height,
            facecolor = color,
            edgecolor = color)
        rect.set_alpha(alpha)
        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()
    return lines, patches


def axis_formatter(x, i):
    if x == 0: return '0'
    magnitude = np.floor(np.log10(x))
    if magnitude >= 9:
        value = x / 1e9
        suffix = 'B'
    elif magnitude >= 6:
        value = x / 1e6
        suffix = 'M'
    elif magnitude >= 3:
        value = x / 1e3
        suffix = 'K'
    else:
        value = x
        suffix = ''
    return f'{value:g}{suffix}'
    
    
def calc_and_chart(stock, data, n_ma1=20, n_ma2=200, expo_ma = False, n_rsi=14):
    if data.empty or len(data) < max(n_ma1, n_ma2):
        raise ValueError("Not enough data to plot with the given parameters.")
    
    date = mdates.date2num(data.index)    
    open_p, high_p, low_p, close_p, volume = (data.iloc[:, i] for i in [0, 1, 2, 3, 5])
    candle_list = [
        (date[x], open_p.iloc[x], close_p.iloc[x], high_p.iloc[x], low_p.iloc[x], volume.iloc[x]) 
        for x in range(len(date))
    ]

    fig, (ax0, ax1, ax1v, ax2) = plt.subplots(4, 1, sharex=True, gridspec_kw={'height_ratios': [1, 3, 0.5, 1]})
    fig.set_facecolor('#07000d')
    plt.gca().yaxis.set_major_locator(mticker.MaxNLocator(prune='upper'))

    ma1 = moving_average_calc(close_p, n_ma1, exp=expo_ma)
    ma2 = moving_average_calc(close_p, n_ma2, exp=expo_ma)
    SP = len(date[n_ma2-1:])
    if SP <= 0:
        raise ValueError("Not enough data points for the selected moving averages.")
    candlestick_chart(ax1, candle_list[-SP:], width=.75, colorup='#9eff15', colordown='#ff1717')
    ax1.plot(date[-SP:], ma1[-SP:], '#e1edf9', label=f'{n_ma1} {"EMA" if expo_ma else "SMA"}', lw=2)
    ax1.plot(date[-SP:], ma2[-SP:], '#4ee6fd', label=f'{n_ma2} {"EMA" if expo_ma else "SMA"}', lw=2)
    ax1.text(0.015, 0.98, 'Price', va='top', color='w', transform=ax1.transAxes)     
    ma_leg = ax1.legend(loc=9, ncol=2, prop={'size':11}, fancybox=True, borderaxespad=0.)
    ma_leg.get_frame().set_alpha(0.4)
    for text in ma_leg.get_texts():
        text.set_color('w')

    rsi = rsi_calc(close_p, n_rsi)
    rsi = rsi.astype(str).astype(float)
    ax0.plot(date[-SP:], rsi[-SP:], lw=2, color='#c1f9f7')
    ax0.axhline(50, color = 'w')
    ax0.fill_between(date[-SP:], rsi[-SP:], 50, where=(rsi[-SP:]>=50), interpolate=True, facecolor='#386d13', edgecolor='#386d13')
    ax0.fill_between(date[-SP:], rsi[-SP:], 50, where=(rsi[-SP:]<=50), interpolate=True, facecolor='#8f2020', edgecolor='#8f2020')
    ax0.text(0.015, 0.95, f'RSI ({n_rsi})', va='top', color='w', transform=ax0.transAxes)
    plt.setp(ax0.get_xticklabels(), visible=False)
    
    volume = volume.astype(str).astype(np.int64)
    plt.setp(ax1.get_xticklabels(), visible=False)
    ax1v.bar(date[-SP:], volume[-SP:], facecolor='#7cb07c')        
    ax1v.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='lower'))
    ax1v.yaxis.set_major_formatter(FuncFormatter(axis_formatter))
    ax1v.text(0.015, 0.95, 'Volume', va='top', color='w', transform=ax1v.transAxes)
    
    macd = macd_calc(close_p)
    ema9 = moving_average_calc(macd, 9)
    ax2.plot(date[-SP:], macd[-SP:], color='#4ee6fd', lw=2)
    ax2.plot(date[-SP:],ema9[-SP:], color='#e1edf9', lw=2)
    ax2.fill_between(date[-SP:], macd[-SP:]-ema9[-SP:], 0, alpha=0.5, facecolor='#00ffe8', edgecolor='#00ffe8')
    ax2.text(0.015, 0.95, 'MACD (12,26,9)', va='top', color='w', transform=ax2.transAxes)     
    ax2.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))
    ax2.xaxis.set_major_locator(mticker.MaxNLocator(15))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.setp(ax2.xaxis.get_ticklabels(), rotation=45, fontsize=11)

    for ax in [ax0, ax1, ax1v, ax2]:
        for spine in ax.spines.values():
            spine.set_color('#5998ff')
        ax.tick_params(colors='w')
        ax.set_facecolor('#07000d')
    plt.subplots_adjust(left=.085, bottom=.16, right=.94, top=.93, wspace=.20, hspace=0)
    plt.suptitle(stock, fontsize=14, fontweight='bold', color='w')
    return fig
