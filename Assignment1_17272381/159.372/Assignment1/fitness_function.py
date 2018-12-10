import numpy as np
import mlp

def initialise_data ():
    # Preprocessing data
    data = np.loadtxt('spambase/spambase.data',delimiter=',')
    data[:,:57] = data[:,:57]-data[:,:57].mean(axis=0)
    imax = np.concatenate((data.max(axis=0)*np.ones((1,58)),np.abs(data.min(axis=0)*np.ones((1,58)))),axis=0).max(axis=0)
    data[:,:57] = data[:,:57]/imax[:57]
   
    # 1-of-N encoding
    target = np.zeros((np.shape(data)[0],2));
    indices = np.where(data[:,57]==0) 
    target[indices,0] = 1
    indices = np.where(data[:,57]==1)
    target[indices,1] = 1
      
    #Take half of data for testing and compute fitness
    test = data[::2,0:57]
    testt = target[::2]
    
    #initialise MLP model,and using 2 hiddnes nodes and 'softmax' activation function
    net = mlp.mlp(test,testt,1,outtype='softmax') 
    return net,test,testt
        
def weight_optimisation_1 (population):

    
    net,test,testt = initialise_data()
    
    fitness = np.zeros((np.shape(population)[0],1))
    result = np.zeros((np.shape(population)[0],3))
    
    for i in range(np.shape(population)[0]):
        start = 0 
        end = 16
        edges = 0
        #Assign strings to each weight of edges in MLP network
        for j in range (net.nin + 1):
            for k in range (net.nhidden):
                net.weights1 [j,k]= convert_weight (population[i][start:end] ) 
                if (population[i][start:end][0] == 1):
                    edges += 1
                start = start + 16
                end = end + 16
                
        for j in range (net.nhidden + 1):
            for k in range (net.nout):
                net.weights2 [j,k]= convert_weight (population[i][start:end]) 
                if (population[i][start:end][0] == 1):
                    edges += 1
                start = start + 16
                end = end + 16
                
        fitness[i] = correct_percentage(test,testt,net)
        #fitness[i] = 1 / sum_of_square_errors (test,testt,net) 
        #alternative fitness value,  using correct percentage is more straightforward
        result[i] = correct_percentage(test,testt,net),sum_of_errors_squared (test,testt,net),edges # record result of data for each string
    fitness = np.squeeze(fitness)
    return fitness , result 


def weight_optimisation_2 (population):

    net,test,testt = initialise_data()
    
    fitness = np.zeros((np.shape(population)[0],1))
    result = np.zeros((np.shape(population)[0],4))
    
    for i in range(np.shape(population)[0]):
        start = 0 
        end = 16
        edges = 0
        
        for j in range (net.nin + 1):
            for k in range (net.nhidden):
                net.weights1 [j,k]= convert_weight (population[i][start:end] ) 
                if (population[i][start:end][0] == 1):
                    edges += 1
                start = start + 16
                end = end + 16

        for j in range (net.nhidden + 1):
            for k in range (net.nout):
                net.weights2 [j,k]= convert_weight (population[i][start:end]) 
                if (population[i][start:end][0] == 1):
                    edges += 1
                start = start + 16
                end = end + 16
        
        fitness[i] = correct_percentage(test,testt,net) + (500 / edges+1 )  #combine correct percent and complexity of MLP network
        
        if correct_percentage(test,testt,net) < 65 or edges > 50  :
            fitness[i] /= 4 # if perfomance is bad or network is very complex, discount the fitness. 
        elif correct_percentage(test,testt,net) > 80 and edges < 35  :
            fitness[i] *= 3  #if perfomance is good and model is simple, triple the fitness.   
        elif correct_percentage(test,testt,net) > 80  :
            fitness[i] *= 2  #if performance is good, double the fitness.   
        
        result[i] = fitness[i],correct_percentage(test,testt,net),sum_of_errors_squared (test,testt,net),edges  # record result of data for each string
        
    fitness = np.squeeze(fitness)
    return fitness , result


def weight_optimisation_version1 (population):
    return weight_optimisation_1 (population) [0]# use the first value for fitness .

def weight_optimisation_version2 (population):
    return weight_optimisation_2 (population) [0] # use the first value for fitness .



# convert a 16 bits binary string to MLP weight for its decimal format and edge connectivity 
def convert_weight(bit):
    
    integer = 0
    fraction = 0
    
    # bit[2:6] digits as integer part of number
    for i in range (2,6):
        integer = integer + bit[i] * 2 ** (i-2)
    #  bit[6:16] digits as fraction part of number   
    for i in range (6,16):        
        fraction = fraction + bit[i] * 2 ** (-1 * i + 5) 
    #  bit[1] as sign of number and bit[0] tells if its edge was connected, 0 for not connected and 1 for connected  
    decimal =  bit[0] * ((-1) ** bit[1] ) * (integer + fraction) 
    
    return decimal 


def correct_percentage(inputs,targets,net):
    #copy from MLP.confmat function to compute correct percentage for fitness function

    # Add the inputs that match the bias node
    inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
    outputs = net.mlpfwd(inputs)
    
    nclasses = np.shape(targets)[1]

    if nclasses==1:
        nclasses = 2
        outputs = np.where(outputs>0.5,1,0)
    else:
        # 1-of-N encoding
        outputs = np.argmax(outputs,1)
        targets = np.argmax(targets,1)

    cm = np.zeros((nclasses,nclasses))
    for i in range(nclasses):
        for j in range(nclasses):
            cm[i,j] = np.sum(np.where(outputs==i,1,0)*np.where(targets==j,1,0))

    return np.trace(cm)/np.sum(cm)*100   

def sum_of_errors_squared (inputs,targets,net) :     
    # Altanative reward of fitness function
    inputs = np.concatenate((inputs,-np.ones((np.shape(inputs)[0],1))),axis=1)
    validout = net.mlpfwd(inputs)
    val_error = 0.5*np.sum((targets-validout)**2)
    return val_error
