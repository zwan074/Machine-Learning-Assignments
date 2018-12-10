import numpy as np
import pylab as pl
import ga
import fitness_function as fF

print('run version 1 ')
g1 = ga.ga (992, 'fF.weight_optimisation_version1'  ,200,100, -1 ,'sp' , 4 , True )
g1.runGA( )

index = np.where(fF.weight_optimisation_1(g1.population)[1][:,0] == fF.weight_optimisation_1(g1.population)[0].max())
print( 'Correct percentage, error and number of edges list for best fitness:')
print (fF.weight_optimisation_1(g1.population)[1][index])

print ('---------------')
print('run version 2 ')
g2 = ga.ga (992, 'fF.weight_optimisation_version2'  ,200,100, -1 ,'sp' , 4 , True )
g2.runGA( )
index = np.where(fF.weight_optimisation_2(g2.population)[1][:,0] == fF.weight_optimisation_2(g2.population)[0].max())
print( 'Correct percentage,error and number of edges list for best fitness:')
print (fF.weight_optimisation_2(g2.population)[1][index,1:])
