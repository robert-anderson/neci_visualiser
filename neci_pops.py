import os
import matrix_utils
import numpy as np

def read_neci_pops(directory):
    file_contents = list()
    for filename in os.listdir(directory):
        if filename.startswith('fort.'):
            with open(directory+'/'+filename, 'r') as f:
                file_contents.append(f.readlines())

    return file_contents

def get_all_neci_pops(directory, det_map, magnitude=False):
    all_proc_data = read_neci_pops(directory)

    time_step = 0
    data_length = 0
    for i in range(len(all_proc_data[0])):
        if 'iter' in all_proc_data[0][i]:
            if time_step == 0:
                iteration = int(all_proc_data[0][i].split()[1])
                time_step = iteration
            data_length+=1

    if magnitude:
        data = np.zeros((3, data_length, len(det_map)))
    else:
        print (3, data_length, len(det_map))
        data = np.zeros((3, data_length, len(det_map)), dtype=np.complex_)

    for proc_data in all_proc_data:
      	iteration_id = -1
        for i in range(len(proc_data)):
            if 'iter' in proc_data[i]:
                iteration_id += 1
                try:
                    det = map(int, proc_data[i+1].split()+proc_data[i+2].split()[:2])
                    value0 = float(proc_data[i+2].split()[2])+1j*float(proc_data[i+2].split()[3])
                    value1 = float(proc_data[i+3].split()[0])+1j*float(proc_data[i+3].split()[1])
                    value2 = float(proc_data[i+3].split()[2])+1j*float(proc_data[i+4].split()[0])
                    if magnitude:
                        value0 = abs(value0)
                        value1 = abs(value1)
                        value2 = abs(value2)
                    data[0][iteration_id][matrix_utils.lookup_det_map(det_map, det)] = value0
                    data[1][iteration_id][matrix_utils.lookup_det_map(det_map, det)] = value1
                    data[2][iteration_id][matrix_utils.lookup_det_map(det_map, det)] = value2
                except ValueError:
                    pass
                except IndexError:
                    pass

    return data


