## Structure

Class structures can be used to:

- define  a unitcell (available)
- create supercell (available)
- visualize atoms in supercell (simple version available)
- generate slabs (in progress)
- and more!


### sample input:

Consider a simple cubic structure with lattice vectors: a=b=c=2.
 
Number of requested periodic images is (2x,2y,1z). 


K = np.array([[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]])

LVec = np.identity(3)*2

Boundary = np.array([2,2,1])




