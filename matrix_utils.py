import scipy.misc
import numpy as np

def get_spin_sector_of_det(det):
    alphas = 0
    for elem in det:
        if elem%2==1:
            alphas+=1
    return len(det)-2*alphas

def read_hamiltonian(dets_file, ham_file):

    # first get the hamiltonian as a list
    ham_list = list()
    with open(ham_file, 'r') as f:
        for line in f.readlines():
            tmp = line.split()
            ham_list.append((int(tmp[0]), int(tmp[1]), float(tmp[2][1:-1].split(',')[0]) + 1j*float(tmp[2][1:-1].split(',')[1])))

    # now order the basis by spin sector
    with open(dets_file, 'r') as f:
        lines = f.readlines()
    norbs = 0
    nelec = 0
    for i in range(len(lines)/2):
        pos = lines[2*i].split()[0]
        det = map(int, lines[2*i].split()[1:]+lines[2*i+1].split())
        if max(det)>norbs:
            norbs=max(det)
        if nelec==0:
            nelec=len(det)

    if nelec%2==0:
        nsectors = 2*(norbs/2-nelec/2)+1
    else:
        nsectors = 2*(norbs/2-nelec/2)

    sector_sizes = [0]*nsectors
    sector_counts = [0]*nsectors
    ham_dim = int(scipy.misc.comb(norbs, nelec))

    for i in range(nsectors/2+1):
        tmp = int(scipy.misc.comb(norbs/2, nelec/2+i)*scipy.misc.comb(norbs/2, nelec/2-i))
        sector_sizes[nsectors/2-i] = tmp
        sector_sizes[nsectors/2+i] = tmp

    sector_offsets = [sum(sector_sizes[:i]) for i in range(len(sector_sizes))]

    rearrangement_map = [0]*ham_dim

    for i in range(len(lines)/2):
        pos = lines[2*i].split()[0]
        det = map(int, lines[2*i].split()[1:]+lines[2*i+1].split())
        spin_sector = get_spin_sector_of_det(det)
        spin_sector = nsectors/2+spin_sector/2

        det_pos = sector_offsets[spin_sector]+sector_counts[spin_sector]
        sector_counts[spin_sector]+=1
        rearrangement_map[i] = det_pos

    print sector_counts
    print sector_sizes

    assert(sector_counts==sector_sizes) # make sure we found every det in each sector

    # now all that's left to do is put the hamiltonian together with the correct basis ordering
    # the result should be block diagonal
    H = np.zeros((ham_dim, ham_dim))

    for item in ham_list:
        H[rearrangement_map[item[0]-1], rearrangement_map[item[1]-1]] = abs(item[2])
        H[rearrangement_map[item[1]-1], rearrangement_map[item[0]-1]] = abs(item[2])
    return H

def check_symmetric(M):
    assert(np.allclose(M, M.T))
    return (M==M.T).all()


