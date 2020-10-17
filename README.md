# Structure_Toolbox

Class structures does structure transformation such as:

- define  a unitcell (available)
- create supercell (available)
- visualize atoms in supercell (simple version available)
- generate slabs (in progress)
- and more!


Currently it includes crystal structure opperation. But molecular operations will be added as well.


## sample input:

A sample input if a simple cubic structure and lattice vectors: a=b=c=2.
 
Number of requested periodic images is (2x,2y,1z). 


K = np.array([[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]])

LVec = np.identity(3)*2

Boundary = np.array([2,2,1])




