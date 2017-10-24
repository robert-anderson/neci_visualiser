import scipy.misc
import numpy as np
import matrix_factory

def get_spin_sector_of_det(det):
    alphas = 0
    for elem in det:
        if elem%2==1:
            alphas+=1
    return len(det)-2*alphas

def get_spin_sector_by_pos(pos, sector_offsets):
    for i in range(1,len(sector_offsets)):
        if pos<sector_offsets[i]:
            return i

def print_highest_weighted_dets(V, det_map, cut_off):
    for vector_id in range(V.shape[1]):
        print "state",vector_id
        hist = [0]*5
        for i in range(V.shape[0]):
            spin_sector = get_spin_sector_of_det(det_map[i])
            spin_sector = len(hist)/2+spin_sector/2
            hist[spin_sector]+=abs(V[i, vector_id])
            if abs(V[i, vector_id])>0.2:
                print det_map[i]
                print 'abs weight', abs(V[i, vector_id])
                print 'spin sector', get_spin_sector_of_det(det_map[i])
        print hist
        print

def read_hamiltonian(dets_file, ham_file, rearrange=True, magnitude=True, zero_coupling=False):

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
    det_map = [[0]*nelec]*ham_dim

    for i in range(len(lines)/2):
        pos = lines[2*i].split()[0]
        det = map(int, lines[2*i].split()[1:]+lines[2*i+1].split())
        spin_sector = get_spin_sector_of_det(det)
        spin_sector = nsectors/2+spin_sector/2

        det_pos = sector_offsets[spin_sector]+sector_counts[spin_sector]
        print det_pos
        det_map[det_pos] = det
        sector_counts[spin_sector]+=1
        rearrangement_map[i] = det_pos

    print sector_counts
    print sector_sizes

    assert(sector_counts==sector_sizes) # make sure we found every det in each sector

    # now all that's left to do is put the hamiltonian together with the correct basis ordering
    # the result should be block diagonal
    H = np.zeros((ham_dim, ham_dim), dtype=np.complex_)

    for item in ham_list:
        if zero_coupling:
            if (get_spin_sector_by_pos(rearrangement_map[item[0]-1], sector_offsets) !=
            get_spin_sector_by_pos(rearrangement_map[item[1]-1], sector_offsets)):
                continue
        
        H[rearrangement_map[item[0]-1], rearrangement_map[item[1]-1]] = abs(item[2])
        if magnitude:
            if rearrange:
                H[rearrangement_map[item[0]-1], rearrangement_map[item[1]-1]] = abs(item[2])
                H[rearrangement_map[item[1]-1], rearrangement_map[item[0]-1]] = abs(item[2])
            else:
                H[item[0]-1, item[1]-1] = abs(item[2])
                H[item[1]-1, item[0]-1] = abs(item[2])
        else:
            if rearrange:
                H[rearrangement_map[item[0]-1], rearrangement_map[item[1]-1]] = item[2]
                if item[0]!=item[1]:
                    H[rearrangement_map[item[1]-1], rearrangement_map[item[0]-1]] = np.conj(item[2])
            else:
                H[item[0]-1, item[1]-1] = item[2]
                if item[0]!=item[1]:
                    H[item[1]-1, item[0]-1] = np.conj(item[2])
    return H, det_map, sector_offsets

def lookup_det_map(det_map, det):
    for i in range(len(det_map)):
        if det_map[i]==det:
            return i

def check_symmetric(M):
    assert(np.allclose(M, M.T))
    return (M==M.T).all()

def get_eigvals(H, a=0, b=-1):
    eigenValues, eigenVectors = np.linalg.eig(H)
    idx = eigenValues.argsort()#[::-1]   
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    return eigenValues[a:b], eigenVectors[:,a:b]

def rayleigh_quotient(H, v, denomenator=True):
    if denomenator:
        return reduce(np.dot, (np.conj(v).T, H, v))/np.linalg.norm(v)
    else:
        return reduce(np.dot, (np.conj(v).T, H, v))


def find_eigenvectors_by_projection(H, det_map, nstates, tau=0.5, tol=8, hist_len=10):
    I = np.identity(H.shape[0])
    P = I-tau*H
    #P = np.linalg.matrix_power(P,10)
    #V = np.random.random((H.shape[0], nstates))+1j*np.random.random((H.shape[0], nstates))
    V = np.zeros((H.shape[0], nstates), dtype=np.complex_)
    V[lookup_det_map(det_map, [1,2,3,4,5,6,7,8]), 0] = 1.0
    V[lookup_det_map(det_map, [1,2,3,4,5,6,7,9]), 1] = 1.0
    V[lookup_det_map(det_map, [1,2,3,4,5,6,8,10]), 2] = 1.0


    #e, V[:,0:1]= get_eigvals(H, a=0, b=1)
    #e, V[:,1:2]= get_eigvals(H, a=0, b=1)

    rq_histories=[[0]*nstates]*hist_len
    while True:
        V = np.dot(P, V)
        for i in range(nstates):
            V[:,i]/=np.linalg.norm(V[:,i])
        for i in range(nstates):
            for j in range(i):
                V[:,i]-=np.dot(np.conj(V[:,j]), V[:,i])*V[:,j]
        for i in range(nstates):
            V[:,i]/=np.linalg.norm(V[:,i])


        rqs = [abs(reduce(np.dot, (np.conj(V[:,i]).T, H, V[:,i]))) for i in range(nstates)]
        print rqs
        rq_histories=rq_histories[1:]+[rqs]
        if all(
            len(set(tuple(round(rq_histories[pos][istate],tol) for pos in range(hist_len))))==1
            for istate in range(nstates)
            ):# or int(round(np.random.random()*100))==3:
            print_highest_weighted_dets(V, det_map, 0.2)

            return rqs, V


'''
H = matrix_factory.random_symmetric(100)

e, v = find_eigenvectors_by_projection(H, 2)
print e
e, v= get_eigvals(H, a=0, b=1)
print e
e, v= get_eigvals(H, a=1, b=2)
print e

assert(0)
'''


'''
e, v= get_eigvals(H, a=0, b=1)
print e
e, v= get_eigvals(H, a=1, b=2)
print e
'''

#H, det_map= read_hamiltonian('./Se2/dets.dat', './Se2/ham.dat', rearrange=True, magnitude=False)
#e, v = find_eigenvectors_by_projection(H, det_map, 3)












