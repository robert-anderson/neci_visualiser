import numpy as np

black =      '#000000'
white =      '#ffffff'
red =        '#ff0000'
green =      '#00ff00'
blue =       '#0000ff'

def random_colour():
    return '#'+str(hex(np.random.randint(0xffffff)))[2:]

def pad_number(x):
    if len(str(x))==3:
        return '0x0'+str(x)[-1]
    else:
        return str(x)

def colour_to_vector(colour):
    return np.array(tuple(int(colour[1:][2*i:2*i+2], base=16) for i in range(3)))

def vector_to_colour(vector):
    return '#'+''.join( tuple( pad_number(hex(int(round(vector[i]))))[2:] for i in range(len(vector))))

class SmoothHue:
    def __init__(self, min_value, max_value, colours=[white, black]):
        self.min_value = min_value
        self.max_value = max_value
        self.colours = colours
        self.colour_vectors = [colour_to_vector(colours[i]) for i in range(len(colours))]
        self.distances = [np.linalg.norm(self.colour_vectors[i]-self.colour_vectors[i+1]) for i in range(len(colours)-1)]
        self.total_distance = sum(self.distances)

    def get_colour(self, value):
        # assuming linear rate along path
        assert(value>=self.min_value)
        assert(value<=self.max_value)
        distance = self.total_distance*(value-self.min_value)/float(self.max_value-self.min_value)
        # locate which leg this distance is to be found on
        for i in range(len(self.distances)):
            if distance<=self.distances[i]:
                # the point is somewhere between vector i and vector i+1
                break
            else:
                distance-=self.distances[i]

        rel_vec = self.colour_vectors[i+1]-self.colour_vectors[i]
        rel_vec = rel_vec/np.linalg.norm(rel_vec)
        return vector_to_colour(self.colour_vectors[i]+rel_vec*distance)        

