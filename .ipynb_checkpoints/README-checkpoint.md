# PairSwap-ICI: A Test for Conditional Independence under Isotonicity

We introduce **PairSwap-ICI**, a novel testing algorithm to assess the conditional independence of $X$ and $Y$ given $Z$, under the assumption that $X$ is stochastically increasing in $Z$.

---

## Repository Overview

### File Structure

- **`simulations/`**  
  Contains code to reproduce the results in **Section 5** of the paper.  
  Example: Simulation studies for evaluating the power and type-I error control of the PairSwap-ICI test.

- **`real_data_analysis/`**  
  Contains code to reproduce the results in **Section 6**, analyzing real-world dataset.

- **`utils/`**  
  Contains utility functions required for the implementation of the `PairSwap-ICI` test.  

---

### Guide for the `utils` file

#### Core Functions

- **`cross_bin_matching`**  
  Implements **cross-bin matching** for a user-specified number of bins $K$. 

- **`neighbour_matching`**
  Implements neighbour matching, which matches $(Y,Z)$ tuples based on their nearest neighbors in $Z$-space.

- **`PairSwapICI_test`**
  Computes the $p$-value for the PairSwap-ICI test, given a dataset of $(X,Y,Z)$ and a matching strategy $M$ (e.g., neighbour or cross-bin matching).

- **`marg_indep_test`**
  Tests the marginal independence hypothesis $H_0:X\perp Y$ given a dataset of $(X,Y,Z)$.

## Installation
Clone the repository to get started:
```bash
git clone https://github.com/your_username/PairSwap-ICI.git
cd PairSwap-ICI
```
Ensure you have the required Python libraries installed (e.g., `numpy`, `scipy`). Use the following command to install them:
```bash
pip install -r requirements.txt
```

## Example usage
Below are examples for computing $p$-values using `PairSwap-ICI` test with different matching strategies.

### Neighbour matching
Given $n$ samples of $(X,Y,Z)$ (each univariate), implement the `PairSwap-ICI` test with `neighbour matching` as follows:
```python
from utils import neighbour_matching, PairSwapICI_test

# Generate or load your data (X, Y, Z)
# X, Y, Z = ...

# Create neighbour matching
M = neighbour_matching(Y, Z)

# Compute the p-value
p = PairSwapICI_test(X, Y, M)
```
### Cross-bin matching
To use cross-bin matching, choose a desired number of bins $K$:
```python
from utils import cross_bin_matching, PairSwapICI_test

# Generate or load your data (X, Y, Z)
# X, Y, Z = ...

# Create cross-bin matching with your chosen number of bins K
K = 10  # Example: 10 bins
M = cross_bin_matching(Y, Z, K)

# Compute the p-value
p = PairSwapICI_test(X, Y, M)
```