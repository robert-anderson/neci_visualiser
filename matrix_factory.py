import numpy as np

def random_symmetric(dim):
    A = (np.random.random((dim, dim)) - np.random.random((dim, dim)))
    return A+A.T

def random_symmetric_blocked(dims):
    A = np.zeros((sum(dims), sum(dims)))
    tot = 0
    for i in range(len(dims)):
        A[tot:tot+dims[i], tot:tot+dims[i]] = random_symmetric(dims[i])
        tot+=dims[i]
    return A

