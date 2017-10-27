import numpy as np
import json
import js_strings

def wave(x, omega_t, k, phase):
	return np.cos(k*x-omega_t-phase)**2

hist_md = {
	'nstates': 3,
	'niters': 200,
	'iter_step': 1,
	'ndets': 495,
	'bar_width': 1,
	'height': 100,
	'max_mag': 3,
	'sector_positions': [30, 40],
	'sector_colours': ['#eee', '#ddd'],
};

x = np.linspace(0,4*np.pi, hist_md['ndets'])

hist_data = []
hist_data.append([])
for iiter in range(hist_md['niters']):
	hist_data[-1].append({'mags':list(wave(x, iiter/8.0, 1, 0)), 'colours':['black']*hist_md['ndets']})

hist_data.append([])
for iiter in range(hist_md['niters']):
	hist_data[-1].append({'mags':list(wave(x, iiter/8.0, 0.8, 0)), 'colours':['blue']*hist_md['ndets']})

hist_data.append([])
for iiter in range(hist_md['niters']):
	hist_data[-1].append({'mags':list(wave(x, iiter/8.0, 0.8, 0)+wave(x, iiter/8.0, 1, 0)), 'colours':['orange']*hist_md['ndets']})
	'''
	for idet in range(hist_md['ndets']):
		hist_data[-1]['mags'].append()
		hist_data[-1]['colours'].append()
	'''

with open('main.js', 'w') as f:
	f.write('hist_md=')
	f.write(json.dumps(hist_md))
	f.write('\nhist_data=')
	f.write(json.dumps(hist_data))
	f.write('\n'+js_strings.script_string)
