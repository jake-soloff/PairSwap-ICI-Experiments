import numpy as np
import networkx as nx

## TO DO - ADD DOCUMENTATION
def cross_bin_matching(Y, Z, K, eta, Y0=0):
    W = eta*K

    M = []
    for k in range(1, 2*K+1):
        J_plus = list(np.where(
                (-W+(k-1)*eta<=Z) & 
                (Z<-W+k*eta) & 
                (Y>Y0)
            )[0])

        J_minus = list(np.where(
                (-W+k*eta<=Z) & 
                (Z<-W+(k+1)*eta) & 
                (Y<=Y0)
            )[0])
        
        while J_plus and J_minus:
            a = J_plus[np.argmax(Y[J_plus])]
            b = J_minus[np.argmin(Y[J_minus])]
            M.append((a,b))
            J_plus.remove(a)
            J_minus.remove(b)

    return(M)

# NB: E should encode Z[i] preceq Z[j]
def max_weight_matching(E, V):
    n = E.shape[0]
    W = np.maximum(E, 0)**2 / V
    W = np.maximum(W, W.T)
    
    G = nx.Graph()
    for i in range(1,n):
        for j in range(i):
            G.add_edge(i, j, weight=W[i,j])

    M0 = nx.max_weight_matching(G)
    M = []
    for (i, j) in M0:
        if E[i,j] > 0: 
            M.append((i,j))
        elif E[i,j] < 0:
            M.append((j,i))

    return(M)