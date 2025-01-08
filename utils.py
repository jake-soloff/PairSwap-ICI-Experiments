import numpy as np
import networkx as nx
import random
import statistics as stat


def cross_bin_matching(Y, Z, K):
    """
    Perform cross-bin matching based on the median of values within each bin.

    Parameters:
    Y (array-like) 
    Z (array-like): Conditioning variable.
    K (int): Number of bins to divide the Z-values into.

    Returns:
    list of tuples: Matched pairs of indices (i, j).
    """
    n = len(Z)
    
    o = np.argsort(Z)  # Indices to sort Z
    Z_ = Z[o]  # Sorted Z
    Y_ = Y[o]  # Sorted Y corresponding to sorted Z
    
    bins = np.array_split(np.arange(n), K)  # Divide indices into K bins
    medians = [stat.median(Y_[bin]) for bin in bins] # Compute medians for each bin

    M = []  # List to store matched pairs
    
    for k in range(len(bins) - 2):  # Loop over bins (excluding the last one)
        J_plus = (bins[k][Y_[bins[k]] >= medians[k]]).tolist() # identifying  points in left bin, as big as the median
        J_minus = (bins[k + 1][Y_[bins[k + 1]] < medians[k + 1]]).tolist() # identifying  points in right bin, smaller than median

        # Match pairs while there are elements in both groups
        while J_plus and J_minus:
            a = J_plus[np.argmax(Y_[J_plus])]  # Element with highest Y in J_plus
            b = J_minus[np.argmin(Y_[J_minus])]  # Element with lowest Y in J_minus
            J_plus.remove(a)
            J_minus.remove(b)

            if Y_[a] >= Y_[b]:
                M.append((o[a], o[b]))  # Store the matched pair
    return M


def neighbour_matching(Y, Z):
    """
    Perform neighbour matching based on the sorted order of Z.

    Parameters:
    Y (array-like)
    Z (array-like): Conditioning variable.

    Returns:
    list of tuples: Matched pairs of indices (i, j).
    """
    id = np.argsort(Z)  # Indices to sort Z
    M = []  # List to store matched pairs

    i = 0
    while i < len(Z) - 1:
        if Y[id[i]] > Y[id[i + 1]]: # check if anti-monotonicity is satisfied
            M.append((id[i], id[i + 1])) # Match adjacent pairs in the sorted order
        i += 2
    return M


def PairSwapICI_test(X, Y, M, nperm=1000):
    """
    Perform the SCINT test on paired differences.

    Parameters:
    X (array-like)
    Y (array-like)
    M (list of tuples): Matched pairs of indices.
    nperm (int): Number of random swaps for the test.

    Returns:
    float: p-value for the test.
    """
    # Compute paired differences
    Del_X = np.array([X[i] - X[j] for (i, j) in M])
    Del_Y = np.array([Y[i] - Y[j] for (i, j) in M])

    # Compute randomly swapped test statistics
    D_S = np.einsum('ij, j, j -> i',
                    (np.random.rand(nperm, len(M)) < 0.5),
                    Del_X,
                    Del_Y)

    # Compute p-value
    return (1 + np.sum(D_S <= 0)) / (1 + nperm)

def marg_indep_test(X, Y, nperm=1000):
    """
    Perform a marginal independence test based on dot product.

    Parameters:
    X (array-like)
    Y (array-like)
    nperm (int): Number of random permutations for the test.

    Returns:
    float: p-value for the test.
    """
    # Compute observed test statistic
    T = np.dot(X, Y)

    # Compute test statistics under permutation
    T_S = [np.dot(X[np.random.permutation(len(X))], Y) for _ in range(nperm)]

    # Compute p-value
    return (1 + np.sum(T_S >= T)) / (1 + nperm)
