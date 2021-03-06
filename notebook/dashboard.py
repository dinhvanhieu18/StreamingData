from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
import random
import time
import pickle
import pandas as pd
import numpy as np
from bokeh.models import HoverTool
from bokeh.models import glyphs
from bokeh.layouts import column, row
import pymongo
from pymongo import MongoClient
#######################################################################################

model = pickle.load(open("final_model.sav", "rb"))

#######################################################################################

def get_last_row(collection):
    conn = MongoClient('mongodb', 27017)
    db=conn.btc
    cur=db[collection].find().sort('timestamp',pymongo.DESCENDING).limit(1)
    conn.close()
    return cur[0]

def get_some(collection, key):
    conn = MongoClient('mongodb', 27017)
    db=conn.btc
    res = []
    try:
        cur=db['realtime'].find().sort('timestamp',pymongo.DESCENDING).limit(10)
        conn.close()
        for c in cur:
            res.append(float(c[key]))
    except:
        cur=db['realtime'].find().sort('timestamp',pymongo.DESCENDING).limit(1)
        conn.close()
        res = [float(c[key])] * 10
    res = np.array(res).reshape((-1, 1))
    global model
    return list(model.predict(res))
#######################################################################################
# the style of tooltips
# refer to official tutorial, A1 Models and Primitives
tooltips_buy = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@buy</span>&nbsp;
</div>
"""
tooltips_sell = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@sell</span>&nbsp;
</div>
"""

tooltips_buy_ave = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@buy_avg</span>&nbsp;
</div>
"""
tooltips_sell_ave = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@sell_avg</span>&nbsp;
</div>
"""
tooltips_buy_pre = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@buy_pre</span>&nbsp;
</div>
"""
tooltips_sell_pre = """
<div>
    <span style="font-size: 17px; font-weight: bold;">@sell_pre</span>&nbsp;
</div>
"""
init = get_last_row('realtime')
init_ave = get_last_row('average')
init_pre_buy = get_some('average','buy_price')
init_pre_sell = get_some('average','sell_price')
x_axis = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#######################################################################################
### buy figure
fig_buy = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_buy.xaxis.axis_label = 'time'  # axis label
fig_buy.yaxis.axis_label = 'buy price'
fig_buy.background_fill_color = 'beige'  # the color of background is 'beige'
fig_buy.background_fill_alpha = 0.5
source_buy = ColumnDataSource(data=dict(x=[pd.to_datetime(init['timestamp'])], 
                                        y=[float(init['buy_price'])]))
# line figure, the data of x axis come from key x of dict 'source_buy'
fig_buy.line(x='x', y='y', alpha=0.5, legend='buy_price', source=source_buy)
buy_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
buy_add = fig_buy.add_glyph(source_or_glyph=source_buy, glyph=buy_glyph)
hover = HoverTool(tooltips=tooltips_buy, renderers=[buy_add])
fig_buy.legend.location = 'bottom_left'
fig_buy.add_tools(hover)
#######################################################################################
### sell figure
fig_sell = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_sell.xaxis.axis_label = 'time'  # axis label
fig_sell.yaxis.axis_label = 'sell price'
fig_sell.background_fill_color = 'beige'  # the color of background is 'beige'
fig_sell.background_fill_alpha = 0.5
source_sell = ColumnDataSource(data=dict(x=[pd.to_datetime(init['timestamp'])], 
                                         y=[float(init['sell_price'])]))
# line figure, the data of x axis come from key x of dict 'source_sell'
fig_sell.line(x='x', y='y', alpha=0.5, legend='sell_price', source=source_sell)
sell_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
sell_add = fig_sell.add_glyph(source_or_glyph=source_sell, glyph=sell_glyph)
hover = HoverTool(tooltips=tooltips_sell, renderers=[sell_add])
fig_sell.legend.location = 'bottom_left'
fig_sell.add_tools(hover)
#######################################################################################
### buy_ave figure
fig_buy_ave = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_buy_ave.xaxis.axis_label = 'time'  # axis label
fig_buy_ave.yaxis.axis_label = 'buy average price'
fig_buy_ave.background_fill_color = 'beige'  # the color of background is 'beige'
fig_buy_ave.background_fill_alpha = 0.5
source_buy_ave = ColumnDataSource(data=dict(x=[pd.to_datetime(init_ave['timestamp'])], 
                                        y=[float(init_ave['buy_price'])]))
# line figure, the data of x axis come from key x of dict 'source_buy'
fig_buy_ave.line(x='x', y='y', alpha=0.5, legend='buy_average_price', source=source_buy_ave)
buy_ave_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
buy_ave_add = fig_buy_ave.add_glyph(source_or_glyph=source_buy_ave, glyph=buy_ave_glyph)
hover = HoverTool(tooltips=tooltips_buy_ave, renderers=[buy_ave_add])
fig_buy_ave.legend.location = 'bottom_left'
fig_buy_ave.add_tools(hover)
#######################################################################################
### sell_ave figure
fig_sell_ave = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_sell_ave.xaxis.axis_label = 'time'  # axis label
fig_sell_ave.yaxis.axis_label = 'sell average price'
fig_sell_ave.background_fill_color = 'beige'  # the color of background is 'beige'
fig_sell_ave.background_fill_alpha = 0.5
source_sell_ave = ColumnDataSource(data=dict(x=[pd.to_datetime(init_ave['timestamp'])], 
                                         y=[float(init_ave['sell_price'])]))
# line figure, the data of x axis come from key x of dict 'source_sell'
fig_sell_ave.line(x='x', y='y', alpha=0.5, legend='sell_average_price', source=source_sell_ave)
sell_ave_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
sell_ave_add = fig_sell_ave.add_glyph(source_or_glyph=source_sell_ave, glyph=sell_ave_glyph)
hover = HoverTool(tooltips=tooltips_sell_ave, renderers=[sell_ave_add])
fig_sell_ave.legend.location = 'bottom_left'
fig_sell_ave.add_tools(hover)
#######################################################################################
### buy_pre figure
fig_buy_pre = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_buy_pre.xaxis.axis_label = 'time'  # axis label
fig_buy_pre.yaxis.axis_label = 'buy predict price'
fig_buy_pre.background_fill_color = 'beige'  # the color of background is 'beige'
fig_buy_pre.background_fill_alpha = 0.5
source_buy_pre = ColumnDataSource(data=dict(x=x_axis, 
                                            y=init_pre_buy))
# line figure, the data of x axis come from key x of dict 'source_buy'
fig_buy_pre.line(x='x', y='y', alpha=0.5, legend='buy_predict_price', source=source_buy_pre)
buy_pre_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
buy_pre_add = fig_buy_pre.add_glyph(source_or_glyph=source_buy_pre, glyph=buy_pre_glyph)
hover = HoverTool(tooltips=tooltips_buy_pre, renderers=[buy_pre_add])
fig_buy_pre.legend.location = 'bottom_left'
fig_buy_pre.add_tools(hover)
#######################################################################################
### sell_pre figure
fig_sell_pre = figure(plot_width=850, plot_height=300, x_axis_type='datetime',
                   title='USD'.format(20))
fig_sell_pre.xaxis.axis_label = 'time'  # axis label
fig_sell_pre.yaxis.axis_label = 'sell predict price'
fig_sell_pre.background_fill_color = 'beige'  # the color of background is 'beige'
fig_sell_pre.background_fill_alpha = 0.5
source_sell_pre = ColumnDataSource(data=dict(x=x_axis, 
                                         y=init_pre_sell))
# line figure, the data of x axis come from key x of dict 'source_sell'
fig_sell_pre.line(x='x', y='y', alpha=0.5, legend='sell_predict_price', source=source_sell_pre)
sell_pre_glyph = glyphs.Circle(x='x', y='y', size=3, fill_color='white')
sell_pre_add = fig_sell_pre.add_glyph(source_or_glyph=source_sell_pre, glyph=sell_pre_glyph)
hover = HoverTool(tooltips=tooltips_sell_pre, renderers=[sell_pre_add])
fig_sell_pre.legend.location = 'bottom_left'
fig_sell_pre.add_tools(hover)
#######################################################################################
cnt = 0
                               
def update():
    global cnt
    cnt += 1
    data_dict = get_last_row('realtime')
    new_data_buy = dict(x=[pd.to_datetime(data_dict['timestamp'])],
                        y=[float(data_dict['buy_price'])]) 
    source_buy.stream(new_data=new_data_buy, rollover=200)

    new_data_sell=dict(x=[pd.to_datetime(data_dict['timestamp'])],
                       y=[float(data_dict['sell_price'])])
    source_sell.stream(new_data=new_data_sell,rollover=200)
    
    if cnt % 4 == 0:
        data_dict_ave = get_last_row('average')
        new_data_buy_ave = dict(x=[pd.to_datetime(data_dict_ave['timestamp'])],
                                y=[float(data_dict_ave['buy_price'])]) 
        source_buy_ave.stream(new_data=new_data_buy_ave, rollover=200)

        new_data_sell_ave=dict(x=[pd.to_datetime(data_dict_ave['timestamp'])],
                               y=[float(data_dict_ave['sell_price'])])
        source_sell_ave.stream(new_data=new_data_sell_ave,rollover=200)
        
        pre_buy = get_some('average','buy_price')
        pre_sell = get_some('average','sell_price')
        new_data_pre_buy = dict(x=x_axis, y=pre_buy)
        new_data_pre_sell = dict(x=x_axis, y=pre_sell)
        source_buy_pre = ColumnDataSource(data=dict(x=[], 
                                             y=[]))
        source_buy_pre.stream(new_data=new_data_pre_buy, rollover=200)
        source_sell_pre = ColumnDataSource(data=dict(x=[], 
                                             y=[]))
        source_sell_pre.stream(new_data=new_data_pre_sell, rollover=200)
        
#######################################################################################
# the second parameter is refresh duration, unit is millisecond
# refer to https://bokeh.pydata.org/en/latest/docs/reference/document.html#bokeh.document.document.Document
curdoc().add_periodic_callback(update, 5 * 1000)
curdoc().add_root(row(column(fig_buy,fig_buy_ave,fig_buy_pre),column(fig_sell,fig_sell_ave,fig_sell_pre)))