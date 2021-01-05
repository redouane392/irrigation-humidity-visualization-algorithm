# -*- coding: utf-8 -*-
"""
Created on Mon Jan  4 09:25:28 2021

@author: Redouane
"""



import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from calendar import month_name


DATA	= 'data.json'
MONTH	= '{:02d}'.format(8)
FNAME	= 'irrigation_graph_2020-{:s}.png'.format(MONTH)
ZONES	= [[(0,   15), 'saturated',  'red'],[(15,  30), 'too wet', 'orange'],[(30,  60), 'perfect',	'green'],[(60, 100), 'plan to water', 'yellow'],[(100, 200), 'dry', 'red']]

def clean_data(dataframe):
	
	return dataframe.replace(200, np.nan)

def save_plot_to_file(dataframe, title, labels, start_date, end_date, filename):
	
	month_d = dataframe[start_date:end_date]
	columns	= month_d.columns
	indexes	= month_d.index

	fig, ax = plt.subplots(3, sharex = True, sharey = True)
	fig.set_size_inches(8, 8)
	fig.suptitle(title,fontsize = 10,y = 0.90)

	INITIAL = True

	for i, label in enumerate(columns):
		ax[i].margins(x = 0)
		ax[i].set_ylim(0, 200)
		line, = ax[i].plot(indexes, month_d[label].values)
		ax[i].legend((line, ), (label, ), loc = 'upper left', fontsize = 8)
		ax[i].tick_params(axis = 'y', labelsize = 8)

		for zone in ZONES:
			ax[i].axhspan(*zone[0],color = zone[2],lw = 0,alpha = 0.2)

			if INITIAL:
				labels[0].append(sum(zone[0]) / 2.0)
				labels[1].append(zone[1])

		if INITIAL:
			INITIAL = False

	plt.yticks(*labels)
	plt.xticks(rotation = 30, fontsize = 8, ha = 'right')
	plt.savefig(filename)

if __name__ == '__main__':
	file = open(DATA, 'r')
	data = json.load(file)[:-1]
	file.close()

	humidity_dataframe = pd.DataFrame(
	data  = { data[i]['datasets']['label'] : data[i]['datasets']['data'] for i in range(len(data)) },
	index =	data[0]['labels'],
	dtype = 'float'
	)

	humidity_dataframe.index = pd.to_datetime(humidity_dataframe.index)
	humidity_dataframe = clean_data(humidity_dataframe)

	labels = [[], []]

	save_plot_to_file(humidity_dataframe,'Irrigation {:s} 2020'.format(month_name[int(MONTH)]),labels,'2020-{:s}-01'.format(MONTH),'2020-{:s}-30'.format(MONTH),FNAME)