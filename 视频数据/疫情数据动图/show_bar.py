#encoding=utf-8
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import datetime

# pip install MovieWriter -i https://pypi.doubanio.com/simple

plt.rcParams['font.sans-serif']=['SimHei','Times New Roman'] # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False


df = pd.read_csv('data.csv', usecols=['date','tag','number'])




colors = dict(zip(
    ['武汉-确诊', '武汉-治愈', '湖北-确诊', '湖北-治愈','中国-确诊',
     '中国-治愈'],
    ['#669999', '#66CC99', '#CCFFFF', '#99CC00',
     '#CCFF99','#FF0033']
))
print(colors)

# fig, ax = plt.subplots(figsize=(15, 8))
# dff = dff[::-1]   # 从上到下翻转值
# # 将颜色值传递给`color=`
# ax.barh(dff['tag'], dff['number'], color=[colors[x] for x in dff['tag']])
# # 遍历这些值来绘制标签和值(Tokyo, Asia, 38194.2)
# for i, (value, name) in enumerate(zip(dff['number'], dff['tag'])):
#     ax.text(value, i,     name,            ha='right')  # Tokyo: 名字
#     ax.text(value, i,     value,           ha='left')   # 38194.2: 值
# # 在画布右方添加年份
# ax.text(1, 0.4, current_year, transform=ax.transAxes, size=46, ha='right')
#
# plt.show()

def draw_barchart(date):
       dff = df[df['date'].eq(date)].sort_values(by='number', ascending=True).tail(6)
       ax.clear()

       ax.barh(dff['tag'], dff['number'], color=[colors[x] for x in dff['tag']])
       dx = dff['number'].max() / 200
       for i, (value, name) in enumerate(zip(dff['number'], dff['tag'])):
              ax.text(value - dx, i, name, size=14, weight=600, ha='right', va='center')
              ax.text(value + dx, i, "{:,}".format(value), size=14, ha='left', va='center')
       # ... polished styles
       ax.text(1, 0.4, date, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=800)
       ax.text(0, 1.06, '人数 (单位：人)', transform=ax.transAxes, size=12, color='#777777')
       ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
       ax.xaxis.set_ticks_position('top')
       ax.tick_params(axis='x', colors='#777777', labelsize=12)
       ax.set_yticks([])
       ax.margins(0, 0.075)
       ax.grid(which='major', axis='x', linestyle='-')
       ax.set_axisbelow(True)
       ax.text(0, 1.1, '44天见证中国力量，中国必胜，武汉必胜',
               transform=ax.transAxes, size=24, weight=600, ha='left')
       ax.text(1, 0, 'by herain', transform=ax.transAxes, ha='right',
                   color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
       plt.box(False)
       # plt.show()


# draw_barchart('2020-02-25')


def getDatesByTimes(sDateStr, eDateStr):
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
    list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y-%m-%d'))
    return list

import matplotlib.animation as animation
fig, ax = plt.subplots(figsize=(10, 7))
animator = animation.FuncAnimation(fig, draw_barchart, frames=getDatesByTimes('2020-01-24', '2020-03-07'))

animator.save('mmv.html')

