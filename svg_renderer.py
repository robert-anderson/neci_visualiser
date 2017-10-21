import svg_strings
import colours
import numpy as np
import matrix_factory
import matrix_utils

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

    def add_heatmap(self, left, top, square_size, data, pinned_values, colour_list, logarithmic=False):
        sh = colours.SmoothHue(pinned_values, colour_list, logarithmic)
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                self.add_square(left+j*square_size, top+i*square_size, square_size, colour=sh.get_colour(data[i,j]))


    def add_histogram(self, left, bottom, height, data, bar_width=1, max_val=None, divs=[], colour=colours.black):
        if max_val is None:
            max_val = max(data)
        for i in range(len(data)):
            self.add_line(left+i*bar_width, bottom, 0, -height*data[i]/float(max_val), width=bar_width, colour=colour)
        

    def render(self, filename='tmp.svg'):
        self.components.append(svg_strings.footer)
        with open(filename, 'w') as f:
            f.write(''.join(self.components))



sr = SVG_renderer(300, 300, bg_colour=colours.white)
#sr = SVG_renderer(300, 300, bg_colour=colours.black)
#sr.add_histogram(200, 40, 100, np.random.random(200), bar_width=4, colour=colours.red)

matrix = matrix_utils.read_hamiltonian('./Se2/dets.dat', './Se2/ham.dat')
print matrix_utils.check_symmetric(matrix)

#sr.add_heatmap(100,100,1, matrix, [0.0,1e-2,3e-2,6e-2,matrix.max()], [colours.black, colours.brown, colours.red, colours.orange, colours.white])
#sr.add_heatmap(100,100,1, matrix, [0.0,1e-2,3e-2,6e-2,1,matrix.max()], [colours.white, colours.grey1, colours.grey2, colours.grey3, colours.grey4, colours.black])
#sr.add_heatmap(100,100,1, matrix, [0.0,1e-2,3e-2,6e-2,1,matrix.max()], list(reversed([colours.white, colours.grey1, colours.grey2, colours.grey3, colours.grey4, colours.black])))

sr.add_heatmap(100,100,1, matrix,
        [
            -6,
            0,
        ], 
        [
            colours.white,
            colours.blue
        ],
        logarithmic=True
    )



sr.render()

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





















