import numpy as np
import pylab as pl
import som

def run_som(x,y,train,test,niteration):
    # Make and train a SOM
    net = som.som(x,y,train)
    net.somtrain(train,niteration)
    # Store the best node for each training input
    best = np.zeros(np.shape(test)[0],dtype=int)
    for i in range(np.shape(test)[0]):
        best[i],activation = net.somfwd(test[i,:])
    return best,net

def count_overlaps(target,best):
    # Find places where the same neuron represents different classes
    i0 = np.where(target==0)
    nodes0 = best[i0]
    i1 = np.where(target==1)
    nodes1 = best[i1]
    doubles = np.intersect1d(nodes0,nodes1)
    return len(doubles),doubles

def plot_som_graph(best,net,target,figure_number):
    doubles = count_overlaps(target,best)[1]
    pl.figure(figure_number)
    pl.plot(net.map[0,:],net.map[1,:],'k.',ms=2)
    where = np.where(target == 0)
    pl.plot(net.map[0,best[where]],net.map[1,best[where]],'o',ms=7)
    where = np.where(target == 1)
    pl.plot(net.map[0,best[where]],net.map[1,best[where]],'x',ms=7)
    pl.plot(net.map[0,doubles],net.map[1,doubles],'rs',ms=10)
    pl.axis([-0.1,1.1,-0.1,1.1])
    pl.axis('off')
    
def SOM_test (train,test,testt,niteration,figure_number):
    net = som.som(50,50,train)
    best = np.zeros(np.shape(train)[0],dtype=int)
    for i in range(np.shape(train)[0]):
        best[i],activation = net.somfwd(train[i,:])
            
    plot_som_graph(best,net,testt,figure_number)
    print ( 'Number of overlaps neuron for SOM of 50 x 50 network without Training ',count_overlaps(testt,best)[0] )
    
    best,net = run_som(10,10,train,test,niteration)
    plot_som_graph(best,net,testt,figure_number+1)
    print ( 'Number of overlaps neuron for SOM of 10 x 10 network ',count_overlaps(testt,best)[0] )
    
    best,net = run_som(20,20,train,test,niteration)
    plot_som_graph(best,net,testt,figure_number+2)
    print ( 'Number of overlaps neuron for SOM of 20 x 20 network ',count_overlaps(testt,best)[0] )
    
    best,net = run_som(50,50,train,test,niteration)
    plot_som_graph(best,net,testt,figure_number+3)
    print ( 'Number of overlaps neuron for SOM of 50 x 50 network ',count_overlaps(testt,best)[0] )  
      
#Preprocessing of the data
#Load and normalise data
data = np.loadtxt('spambase/spambase.data',delimiter=',')
data[:,:57] = data[:,:57]-data[:,:57].mean(axis=0)
imax = np.concatenate((data.max(axis=0)*np.ones((1,58)),np.abs(data.min(axis=0)*np.ones((1,58)))),axis=0).max(axis=0)
data[:,:57] = data[:,:57]/imax[:57]

target = data[:,57]

order = np.arange(np.shape(data)[0])
np.random.shuffle(order)
data = data[order,:]
target = target[order]

#Below test could be run seperately to have a neat graph set

#train and test all features of spam data as input
print ('train and test all features of spam data as input')
train = data[::2,0:57] #50% train data
traint = target[::2]
test = data[1::2,0:57] #50% test data
testt = target[1::2]
SOM_test (train,test,testt,100,1)

#train and test 1-23 features of spam data as input
print('---------------')
print ('train and test 1-23 features of spam data as input')
train = data[::2,0:23] #50% train data
traint = target[::2]
test = data[1::2,0:23] #50% test data
testt = target[1::2]
SOM_test (train,test,testt,100,5)

#train and test 24-57 features of spam data as input
print('---------------')
print ('train and test 24-57 features of spam data as input')
train = data[::2,23:57] #50% train data
traint = target[::2]
test = data[1::2,23:57] #50% test data
testt = target[1::2]
SOM_test (train,test,testt,100,9)


pl.show()










