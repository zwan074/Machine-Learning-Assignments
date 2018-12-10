import numpy as np
import pylab as pl
import mlp

#Preprocessing of the data
#Load and normalise data
data = np.loadtxt('spambase/spambase.data',delimiter=',')
data[:,:57] = data[:,:57]-data[:,:57].mean(axis=0)
imax = np.concatenate((data.max(axis=0)*np.ones((1,58)),np.abs(data.min(axis=0)*np.ones((1,58)))),axis=0).max(axis=0)
data[:,:57] = data[:,:57]/imax[:57]

#1-of-N encoding for target data
target = np.zeros((np.shape(data)[0],2))
indices = np.where(data[:,57]==0) 
target[indices,0] = 1 # ham email
indices = np.where(data[:,57]==1)
target[indices,1] = 1 #spam email


# Randomly order the data
order = np.arange(np.shape(data)[0])
np.random.shuffle(order)
data = data[order,:]
target = target[order,:]

# Split into training, validation, and test sets at 50:25:25 ratio
train = data[::2,0:57] # 50% train data 
traint = target[::2]
valid = data[1::4,0:57]# 25% valid data 
validt = target[1::4]
test = data[3::4,0:57] #25% test data
testt = target[3::4]

# Function for running MLP with activiation function'softmax' and learning rate as 0.2
def run_MLP (train,traint,valid,validt,test,testt,nhidden):
    net = mlp.mlp(train,traint,nhidden,outtype='softmax')
    net.earlystopping(train,traint,valid,validt,0.2)
    net.confmat(test,testt)

# Train a simple MLP and comupte Confution Matrix
print( 'First MLP train result with 5 hidden nodes' )
run_MLP (train,traint,valid,validt,test,testt,5) # use 5 hidden nodes
print ('----------------------------------')
# Implement cross-validation;

#Cross validation 1:
#slice data into different range, 50% head , 25% middle and 25% tail
i0 = int(np.round(np.shape(data)[0]/2))
i1 = i0+ int(np.round(np.shape(data)[0]/4))

train_xvalidation1 = data[:i0,0:57] # 50% train data 
traint_xvalidation1 = target[:i0]
valid_xvalidation1 = data[i0:i1,0:57]# 25% valid data 
validt_xvalidation1 = target[i0:i1]
test_xvalidation1 = data[i1:,0:57] #25% test data
testt_xvalidation1 = target[i1:]
print ('Cross validation 1 result with 5 hidden nodes')
run_MLP (train_xvalidation1,traint_xvalidation1,valid_xvalidation1,validt_xvalidation1,test_xvalidation1,testt_xvalidation1,5)

#Cross validation 2:
#slice data into different range,25% head , 50% middle and 25% tail
i0 = int(np.round(np.shape(data)[0]/4))
i1 = i0+ int(np.round(np.shape(data)[0]/2))
train_xvalidation2 = data[i0:i1,0:57] # 50% train data 
traint_xvalidation2 = target[i0:i1]
valid_xvalidation2 = data[i1:,0:57]# 25% valid data 
validt_xvalidation2 = target[i1:]
test_xvalidation2 = data[:i0:,0:57] #25% test data
testt_xvalidation2 = target[:i0]
print ('Cross validation 2 result with 5 hidden nodes')
run_MLP (train_xvalidation2,traint_xvalidation2,valid_xvalidation2,validt_xvalidation2,test_xvalidation2,testt_xvalidation2,5)
print ('----------------------------------')

#Test out different sizes of hidden layer with the first MLP training dataset
print('Test out different sizes of hidden layer') #could seperate this process to avoid long waiting time or stuck in local minimum
for nhidden in [1,2,5,10,20,25,30,35,40,45,50]: 
    print ("Test Hidden Nodes "+str(nhidden)  )
    run_MLP (train,traint,valid,validt,test,testt,nhidden)
print ('----------------------------------')
#Test out different subsets of the features 

# compute and plot difference in means of input attributes between spam and ham data    
spamIndices = np.where(data[:,57]==1) 
hamIndices = np.where(data[:,57]==0) 
spamData = data[spamIndices,:57].mean(axis=1)
hamData = data[hamIndices,:57].mean(axis=1)
x = np.arange(len ((spamData-hamData) [0]))
pl.title('difference in means of input attributes between spam and ham data')
pl.plot((spamData-hamData) [0])
pl.show()

#set up data for test subset of features 1
train_sub_features1 = data[::2,0:23] # 50% train data 
traint_sub_features1  = target[::2]
valid_sub_features1  = data[1::4,0:23]# 25% valid data 
validt_sub_features1  = target[1::4]
test_sub_features1  = data[3::4,0:23] #25% test data
testt_sub_features1  = target[3::4]

print('Result for sub features set 1 of spam data:')
run_MLP (train_sub_features1,traint_sub_features1,valid_sub_features1,validt_sub_features1,test_sub_features1,testt_sub_features1,1)

print ('----------------------------------')
#set up data for test subset of features 2
train_sub_features2 = data[::2,23:57] # 50% train data 
traint_sub_features2  = target[::2]
valid_sub_features2  = data[1::4,23:57]# 25% valid data 
validt_sub_features2  = target[1::4]
test_sub_features2  = data[3::4,23:57] #25% test data
testt_sub_features2  = target[3::4]
print('Result for sub features set 2 of spam data :')
run_MLP (train_sub_features2,traint_sub_features2,valid_sub_features2,validt_sub_features2,test_sub_features2,testt_sub_features2,1)

print ('----------------------------------')
#set up data for test subset of features 3
data = data[:,:57]
train_sub_features3 = data[::2,0::2] # 50% train data 
traint_sub_features3  = target[::2]
valid_sub_features3  = data[1::4,0::2]# 25% valid data 
validt_sub_features3  = target[1::4]
test_sub_features3  = data[3::4,0::2] #25% test data
testt_sub_features3  = target[3::4]

print('Result for sub features set 3 of spam data :')
run_MLP (train_sub_features3,traint_sub_features3,valid_sub_features3,validt_sub_features3,test_sub_features3,testt_sub_features3,1)

print ('----------------------------------')

#set up data for test subset of features 4

train_sub_features4 = data[::2,1::2] # 50% train data 
traint_sub_features4  = target[::2]
valid_sub_features4  = data[1::4,1::2]# 25% valid data 
validt_sub_features4  = target[1::4]
test_sub_features4  = data[3::4,1::2] #25% test data
testt_sub_features4  = target[3::4]


print('Result for sub features set 4 of spam data :')
run_MLP (train_sub_features4,traint_sub_features4,valid_sub_features4,validt_sub_features4,test_sub_features4,testt_sub_features4,1)
    

print ('----------------------------------')    
train_sub_features5 = data[::2,0:47] # 50% train data 
traint_sub_features5  = target[::2]
valid_sub_features5  = data[1::4,0:47]# 25% valid data 
validt_sub_features5  = target[1::4]
test_sub_features5  = data[3::4,0:47] #25% test data
testt_sub_features5  = target[3::4]


print('Result for sub features set 5 of spam data :')
run_MLP (train_sub_features5,traint_sub_features5,valid_sub_features5,validt_sub_features5,test_sub_features5,testt_sub_features5,1)


print ('----------------------------------')
train_sub_features6 = data[::2,47:53] # 50% train data 
traint_sub_features6  = target[::2]
valid_sub_features6  = data[1::4,47:53]# 25% valid data 
validt_sub_features6  = target[1::4]
test_sub_features6  = data[3::4,47:53] #25% test data
testt_sub_features6  = target[3::4]


print('Result for sub features set 6 of spam data :')
run_MLP (train_sub_features6,traint_sub_features6,valid_sub_features6,validt_sub_features6,test_sub_features6,testt_sub_features6,1)


print ('----------------------------------')
train_sub_features7 = data[::2,53:57] # 50% train data 
traint_sub_features7  = target[::2]
valid_sub_features7  = data[1::4,53:57]# 25% valid data 
validt_sub_features7  = target[1::4]
test_sub_features7  = data[3::4,53:57] #25% test data
testt_sub_features7  = target[3::4]

print('Result for sub features set 7 of spam data :')
run_MLP (train_sub_features7,traint_sub_features7,valid_sub_features7,validt_sub_features7,test_sub_features7,testt_sub_features7,1)





