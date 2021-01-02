#!usr/bin/python3.6

"""
Created on Sat Jan 2 2021

@author: Pegah Mirabedini
"""

"""This script makes a van der Waals heterostructure from two structures:
   Positional argument 1: Structure1 (Substrate) POSCAR file
   positional argument 2: Structure2 (layer) POSCAR file
   positional arguement 3: vdW distance between the layer and substrate (Angstrom)
   positional argument 4: vaccum spacing (Angstrom)
   Output format: POSCAR
   Note: The substrate and the layer should have similar in-plane size."""


import numpy as np
import sys


"""Helper function"""
def get_structural_info(lines):
    
    LVec = np.zeros([3,3])
    natoms = 0
    
    for i,line in enumerate(lines):
        if 'cart' in line or 'Cartesian' in line or 'Direct' in line:
            coord = line
            nelem = len(lines[i-1].split())
            natoms_mat = np.zeros(nelem)
            for n in range(nelem):
                natoms_mat[n] = int(lines[i-1].split()[n-nelem]) #returns float?!
                natoms += natoms_mat[n]
        
            natoms = int(natoms)
        
            LVec[0] = [float(lines[i-5].split()[j-3]) for j in range(3)]
            LVec[1] = [float(lines[i-4].split()[j-3]) for j in range(3)]
            LVec[2] = [float(lines[i-3].split()[j-3]) for j in range(3)]
            
            pos_init = i+1
     
    

    Pos = np.zeros([natoms,3])  
    
    for i,line in enumerate(lines):
        if 'cart' in line or 'Cartesian' in line:
            for l in range(natoms):
                Pos[l] = [float(lines[pos_init+l].split()[j-3]) for j in range(3)]
        elif 'Direct' in line:
            for l in range(natoms):
                dir_pos = [float(lines[pos_init+l].split()[j-3]) for j in range(3)]
                Pos[l] = np.dot(LVec,np.transpose(dir_pos))

            
    return nelem, natoms_mat, natoms, LVec, Pos
        


#Load Structural info.
Structure1 = sys.argv[1]
infile1 = open(Structure1, 'rt')
lines1 = infile1.readlines()
nelem_sub, natoms_mat_sub, natoms_sub, LVec_sub, pos_sub = get_structural_info(lines1)

Structure2 = sys.argv[2]
infile2 = open(Structure2, 'rt')
lines2 = infile2.readlines()
nelem_layer, natoms_mat_layer, natoms_layer, LVec_layer, pos_layer = get_structural_info(lines2)


#Move substrate atoms to strat from (0,0,0)
pos_sub[:,0] = pos_sub[:,0] - np.min(pos_sub[:,0])
pos_sub[:,1] = pos_sub[:,1] - np.min(pos_sub[:,1])
pos_sub[:,2] = pos_sub[:,2] - np.min(pos_sub[:,2])


#Move layer atoms to top of the substrate with a vdW spacing
vdW = sys.argv[3]
vdW = float(vdW)
pos_layer[:,0] = pos_layer[:,0] - np.min(pos_layer[:,0]) 
pos_layer[:,1] = pos_layer[:,1] - np.min(pos_layer[:,1]) 
pos_layer[:,2] = pos_layer[:,2] - np.min(pos_layer[:,2]) + np.max(pos_sub[:,2]) + vdW


#Integrate the layer and the substrate : generate the heterostructure
pos_hstructure = list(pos_sub) + list(pos_layer)


#Generate the lattice vectors (box) of the heterostructure
d = sys.argv[4]
d = float(d)
z = np.max(pos_layer[:,2]) + d
LVec_hstructure = np.array([list(LVec_layer[0,:]), list(LVec_layer[1,:]), list([0.,0.,z])])


#Generate the list of atom no. for all constituent elements
natoms_list_heter = list(natoms_mat_sub)+list(natoms_mat_layer)


#Save the generated heterostructure to a new POSCAR file
heterostructure = './heterostructure.POSCAR.vasp'
outfile = open(heterostructure,'wt')
outfile.writelines('heterostructure - vdW {}'.format(vdW) + '\n') 
outfile.writelines('{}'.format(1.0) + '\n') 
outfile.writelines(' '.join(str(elem) for elem in row) + '\n' for row in LVec_hstructure) 
outfile.writelines('{}'.format(int(natoms_list_heter[nat]))+' ' for nat in range(len(natoms_list_heter))) 
outfile.writelines('\n'+'{}'.format('cart')+'\n') 
outfile.writelines(' '.join(str(elem) for elem in row) +'\n' for row in pos_hstructure)


print('done')
