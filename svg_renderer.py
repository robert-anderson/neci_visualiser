import svg_strings
import colours
import numpy as np
import matrix_factory
import matrix_utils
import neci_pops

class SVG_renderer:
    def __init__(self, width, height, bg_colour=colours.white):
        self.width = width
        self.height = height
        self.bg_colour = bg_colour
        self.components = [svg_strings.header.format(d={'width':width, 'height':height, 'bg_colour':bg_colour})]
        self.id_counter = 0

    def get_new_id(self):
        self.id_counter+=1
        return 'obj_'+str(self.id_counter)


    def add_text(self, x, y, fontsize, text, colour=colours.black):
        if colour==self.bg_colour:
            return
        self.components.append(
            svg_strings.text.format(
                d = {
                    'x': x,
                    'y': y, 
                    'fontsize': fontsize,
                    'text': text,
                    'colour': colour,
                    'id': self.get_new_id(),
                }
            )
        )


    def add_line(self, x, y, dx, dy, colour=colours.black, width=1):
        if colour==self.bg_colour:
            return
        self.components.append(
            svg_strings.line.format(
                d = {
                    'x': x,
                    'y': y, 
                    'dx': dx, 
                    'dy': dy, 
                    'colour': colour,
                    'width': str(width),
                    'id': self.get_new_id(),
                }
            )
        )

    def add_square(self, x, y, size, colour=colours.black):
        self.add_line(x, y, 0, size, colour=colour, width=size)

    def add_heatmap(self, left, top, square_size, data, pinned_values, colour_list, logarithmic=False, div_positions=[]):
        sh = colours.SmoothHue(pinned_values, colour_list, logarithmic)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.add_square(left+j*square_size, top+i*square_size, square_size, colour=sh.get_colour(data[i,j]))
        for div_pos in div_positions:
            self.add_line(left+square_size*div_pos, top, 0, data.shape[0]*square_size+400, colour=colours.grey1, width=1)
            self.add_line(left, top+square_size*div_pos, data.shape[0]*square_size, 0, colour=colours.grey1, width=1)


    def add_histogram(self, left, bottom, height, data, bar_width=1, max_val=None, divs=[], colour=colours.black):
        if max_val is None:
            max_val = max(data)
        for i in range(len(data)):
            self.add_line(left+i*bar_width, bottom, 0, -height*data[i]/float(max_val), width=bar_width, colour=colour)
        

    def render(self, filename='tmp.svg'):
        self.components.append(svg_strings.footer)
        with open(filename, 'w') as f:
            f.write(''.join(self.components))


def get_phase_colour(theta):
	n = 420
	i = int(n*theta/(2*np.pi))
	#colour_list = [colours.blue, colours.cyan, colours.green, colours.orange, colours.red]
	#colour_list = [colours.blue, colours.magenta, colours.red]
	colour_list = [colours.blue, colours.cyan, colours.green]
	colour_list+=list(reversed(colour_list))
	colour_sector = i/(n/(len(colour_list)-1))
	return colours.get_inbetween_colour(colour_list[colour_sector], colour_list[colour_sector+1],
				float(i%(n/(len(colour_list)-1)))/(n/(len(colour_list)-1)))

sr = SVG_renderer(300, 300, bg_colour=colours.white)
r = 80
cx, cy = 200, 200
n = 1400
for i in range(n):
	sr.add_square(cx+r*np.cos(2*i*np.pi/n), cy+r*np.sin(2*i*np.pi/n),
			2, colour=get_phase_colour(2*i*np.pi/n))
	#sr.add_line(cx, cy, r*np.cos(2*i*np.pi/n), r*np.sin(2*i*np.pi/n),
#			width=1, colour=get_phase_colour(2*i*np.pi/n))

sr.render()

assert(0)

matrix, det_map, sector_offsets = matrix_utils.read_hamiltonian('./Se2/dets.dat', './Se2/ham.dat', zero_coupling=False)


'''
E, V = matrix_utils.get_eigvals(matrix, a=0, b=3)

print E
matrix_utils.print_highest_weighted_dets(V, det_map, 0.2)
'''

sr.add_heatmap(100,40,1, matrix,
        [
            -6,
            0,
        ], 
        [
            colours.white,
            colours.blue
        ],
        logarithmic=True,
        div_positions=sector_offsets+[matrix.shape[0]]
    )


neci_pops_data = neci_pops.get_all_neci_pops('Se2/inst_pops', det_map, magnitude=True)

istate=0
#for i in range(len(neci_pops_data[istate,0,:])):
#    if neci_pops_data[istate,0,:][i]!=0:
#        print i, det_map[i], neci_pops_data[istate,0,:][i]

iteration=neci_pops_data.shape[1]-1

#iteration = 1

for istate in [0,1,2]:
    sr.add_histogram(100,620+(2-istate)*100,80, neci_pops_data[istate,iteration,:])

sr.add_text(280,25, '20px', 'iteration {}'.format(iteration*100), colour=colours.black)
sr.render()

assert(0)


'''
sr.add_heatmap(100,100,1, matrix,
        [
            -20,
            -6,
            -2,
            np.log(matrix.max())
        ], 
        [
            colours.white,
            colours.get_inbetween_colour(colours.white, colours.blue, 0.05),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.7),
            colours.blue
        ],
        logarithmic=True
    )



sr.render()
'''

'''

        [
            colours.white,
            colours.get_inbetween_colour(colours.white, colours.blue, 0.1),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.2),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.3),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.4),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.5),
            colours.get_inbetween_colour(colours.white, colours.blue, 0.9),
            colours.blue
        ],

'''





















