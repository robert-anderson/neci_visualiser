import numpy as np

red =        '#ff0000'
green =      '#00ff00'
blue =       '#0000ff'
lightblue =  '#81F0FF'
yellow =     '#FFF63D'
orange =     '#FF711A'
brown =      '#732C00'

white =      '#ffffff'
grey1 =      '#E5E5E5'
grey2 =      '#999999'
grey3 =      '#6E6E6E'
grey4 =      '#3F3F3F'
black =      '#000000'

def random_colour():
    return '#'+str(hex(np.random.randint(0xffffff)))[2:]

def pad_number(x):
    if len(str(x))==3:
        return '0x0'+str(x)[-1]
    else:
        return str(x)

def get_inbetween_colour(start, end, fraction):
    assert(fraction>=0)
    assert(fraction<=1)
    start_vec = colour_to_vector(start)
    end_vec = colour_to_vector(end)
    res_vec = end_vec-start_vec
    return vector_to_colour(start_vec+res_vec*fraction)


def colour_to_vector(colour):
    return np.array(tuple(int(colour[1:][2*i:2*i+2], base=16) for i in range(3)))

def vector_to_colour(vector):
    return '#'+''.join( tuple( pad_number(hex(int(round(abs(vector[i])))))[2:] for i in range(len(vector))))

class SmoothHue:
    def __init__(self, pinned_values, colours, logarithmic=False):
        assert(len(pinned_values)==len(colours))
        self.pinned_values = pinned_values
        self.colours = colours
        self.logarithmic = logarithmic
        self.colour_vectors = [colour_to_vector(colours[i]) for i in range(len(colours))]
        self.distances = [np.linalg.norm(self.colour_vectors[i]-self.colour_vectors[i+1]) for i in range(len(colours)-1)]
        self.total_distance = sum(self.distances)

    def get_colour(self, value):
        # assuming linear rate along path
        if self.logarithmic:
            if value==0.0:
                #the log doesn't exist
                value = self.pinned_values[0]
            else:
                value = np.log(value)
                if value<self.pinned_values[0]:
                    value = self.pinned_values[0]
                if value>self.pinned_values[-1]:
                    value = self.pinned_values[-1]

        else:
            assert(value>=self.pinned_values[0])
            assert(value<=self.pinned_values[-1])

        # locate which leg this distance is to be found on
        for i in range(len(self.pinned_values)-1):
            if value<=self.pinned_values[i+1]:
                # the point is somewhere between vector i and vector i+1
                break

        distance = self.distances[i]*(value-self.pinned_values[i])/float(self.pinned_values[i+1]-self.pinned_values[i])

        rel_vec = self.colour_vectors[i+1]-self.colour_vectors[i]
        rel_vec = rel_vec/np.linalg.norm(rel_vec)
        return vector_to_colour(self.colour_vectors[i]+rel_vec*distance)

