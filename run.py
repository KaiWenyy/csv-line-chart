import yaml
import argparse
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

with open('config.yaml', 'r') as stream:
	cfg = yaml.load(stream)
print(cfg['data_scope'][0])

parser = argparse.ArgumentParser(description='Read csvfile and plot the chart')
parser.add_argument('--csvfile', type=str, default="file.csv", help='input the csv file name')
opt = parser.parse_args()
print(opt)

data_array = np.zeros((len(cfg['array']), cfg['data_size']))
data_array_name = []
data_array_type = []
data_array_y_axis = []
y_axis_label = []

data_start_point = cfg['data_scope'][0]
#print(type(data_start_point))
data_end_point = cfg['data_scope'][1]

# default : chart type arguments dict
default_type = {'color':'b', 'linestyle': '-', 'marker': '.', 'linewidth':'1'}


# 開啟 CSV 檔案
with open(opt.csvfile, newline='') as csvfile:

	# 讀取 CSV 檔內容，將每一列轉成一個 dictionary
	rows = csv.DictReader(csvfile)
	l = 0
	size = 0
	for row in rows:
		l += 1
		tmp = 0
		if l >= data_start_point and l <= data_end_point:
			for a in cfg['array']:
				array = cfg['array'][a]
				#print(array['data_name'])
				d = row[array['data_name']]#[data_start_point:data_end_point+1]
				data_array[tmp][size] = d
				tmp +=1
			size += 1

for a in cfg['array']:
	array = cfg['array'][a]			
	data_array_name.append(array['name'])
	data_array_type.append(array['type'])
	data_array_y_axis.append(array['y_axis']['label'])
	if array['y_axis']['label'] not in y_axis_label:
		y_axis_label.append(array['y_axis']['label'])

fig, ax1 = plt.subplots()
# set x_axis
x_data = np.linspace(data_start_point,data_end_point,cfg['data_size'])
ax1.set_xlabel(cfg['x_axis']['label'])

line_object = []

for i in range(data_array.shape[0]):

	# set format type
	for t in default_type.keys():
		if data_array_type[i][t] != None:
			default_type[t] = data_array_type[i][t]		

	# whether share axis
	if data_array_y_axis[i] != y_axis_label[0]: # share x_axis
		ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
		color = 'k'
		ax2.set_ylabel(data_array_y_axis[i], color=color)  # we already handled the x-label with ax1
		# plot
		l2 = ax2.plot(x_data, data_array[i], 
			color=default_type['color'], 
			linestyle=default_type['linestyle'],
			marker=default_type['marker'],
			linewidth=default_type['linewidth'],
			label=data_array_name[i])
		ax2.tick_params(axis='y', labelcolor=color)
		line_object.append(l2)
		#plt.legend(loc='upper right')
	else:
		color = 'k'
		ax1.set_ylabel(data_array_y_axis[i], color=color)
		# plot
		print(data_array_name[i])
		l1 = ax1.plot(x_data, data_array[i], 
			color=default_type['color'], 
			linestyle=default_type['linestyle'],
			marker=default_type['marker'],
			linewidth=default_type['linewidth'],
			label=data_array_name[i])
		ax1.tick_params(axis='y', labelcolor=color)
		line_object.append(l1)
		#plt.legend(loc='upper right')


fig.tight_layout()  # otherwise the right y-label is slightly clipped	
plt.title(cfg['title'])
plt.xlim(data_start_point, data_end_point)
#fig.legend()
fig.legend(line_object,     # The line objects
           labels=data_array_name,   # The labels for each line
           loc='lower center',   # Position of legend
           #bbox_to_anchor = (0.5, 0),
           ncol = len(line_object),
           borderaxespad=0.1,    # Small spacing around legend box
           #title="Legend Title"  # Title for the legend
           )
plt.show()

