import numpy as np
import json, sys
import neci_pops, matrix_utils, colours
sys.path.insert(0, 'browser_ui')
import js_strings

matrix, det_map, sector_offsets = matrix_utils.read_hamiltonian('./Se2/dets.dat', './Se2/ham.dat', zero_coupling=False)
neci_pops_data = neci_pops.get_all_neci_pops('Se2/inst_pops', det_map, magnitude=False)

neci_pops_data = neci_pops_data[:,:10,:]
nstates, niters, ndets = neci_pops_data.shape
print nstates, niters, ndets

hist_md = {
	'nstates': nstates,
	'niters': niters,
	'iter_step': 100,
	'ndets': ndets,
	'bar_width': 2,
	'height': 100,
	'max_mag': np.absolute(neci_pops_data).max(),
	'sector_positions': sector_offsets,
	'sector_colours': ['#eee', '#ddd'],
};

hist_data = []
for istate in range(nstates):
	hist_data.append([])
	for iiter in range(niters):
		hist_data[-1].append({'mags':[], 'colours':[]})
		for idet in range(ndets):
			hist_data[-1][-1]['mags'].append(abs(neci_pops_data[istate, iiter, idet]))
			hist_data[-1][-1]['colours'].append(
				colours.get_phase_colour(np.angle(neci_pops_data[istate, iiter, idet]))
			)

colour_list = [colours.white, colours.blue]
pinned_values = [-6, 0]

sh = colours.SmoothHue(pinned_values, colour_list, logarithmic=True)
H_colours = []

for i in range(matrix.shape[0]):
	H_colours.append([])
	for j in range(matrix.shape[1]):
		H_colours[-1].append(sh.get_colour(abs(matrix[i,j])))



with open('browser_ui/main.js', 'w') as f:
	f.write('H=')
	f.write(json.dumps(H_colours))
	f.write('\nhist_md=')
	f.write(json.dumps(hist_md))
	f.write('\nhist_data=')
	f.write(json.dumps(hist_data))
	f.write('\n'+js_strings.script_string)
