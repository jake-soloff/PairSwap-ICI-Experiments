import numpy as np
import networkx as nx
import random


## TO DO - ADD DOCUMENTATION
def cross_bin_matching(Y, Z, eta):
    """
    Cross bin matching: ...
    """
    ql_pts = np.arange(0, 1+eta, eta)
    ql_pts[len(ql_pts)-1] = np.floor(ql_pts[len(ql_pts)-1])
    bin_ends = np.quantile(Z, ql_pts)

    # medians = []
    # for l in range(len(bin_ends)-1):
    #     medians.append(stat.median(Y[np.where(
    #         (bin_ends[l]<=Z) & (Z<bin_ends[l+1]))[0]
    #                                ]))

    medians=np.full(len(bin_ends)-1,0)
        
    M = []
    for k in range(len(bin_ends)-2):                 
        J_plus = np.array(np.where(
                (bin_ends[k]<=Z) & 
                (Z<bin_ends[k+1]) & 
                (Y>=medians[k])
        )[0]).tolist()

        J_minus = np.array(np.where(
                (bin_ends[k+1]<=Z) & 
                (Z<bin_ends[k+2]) & 
                (Y<medians[k+1])
        )[0]).tolist()
        
        while J_plus and J_minus:
            #if np.max(Y[J_plus])<np.min(Y[J_minus]): break
            a = J_plus[np.argmax(Y[J_plus])]
            b = J_minus[np.argmin(Y[J_minus])]
            J_plus.remove(a)
            J_minus.remove(b)
            #a = random.choice(J_plus);J_plus.remove(a)
            #b = random.choice(J_minus);J_minus.remove(b)
            if Y[a] >= Y[b]:
                M.append((a,b))
    return(M)

def same_bin_matching(Y, Z, eta):
    ql_pts = np.arange(0, 1+eta, eta)
    ql_pts[len(ql_pts)-1] = 1
    bin_ends = np.quantile(Z, ql_pts)
        
    M = []
    for k in range(len(bin_ends)-2):                 
        J = np.where((bin_ends[k]<=Z) & (Z<bin_ends[k+1]))[0].tolist()

        while J:
            a = random.choice(J);J.remove(a)
            if len(J)==0:break
            b = random.choice(J);J.remove(b)
            if (Z[a]-Z[b])*(Y[a]-Y[b])<=0:
                if Z[a]<Z[b]:
                    M.append((a,b))
                else:
                    M.append((b,a))
    return(M)

def immediate_neighbor_matching(Y, Z):
    id = np.argsort(Z)

    i=0;M=[]
    while i+1<len(Z):
        if Y[id[i]]>=Y[id[i+1]]:
            M.append((id[i],id[i+1]))
        i+=2
    return(M)


def cross_bin_matching_old(Y, Z, K, eta, Y0=0):
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
