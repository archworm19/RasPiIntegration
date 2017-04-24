'''

Generate Sequences of Intensity Values


'''

import scipy as sp
import pylab as plt


#### Rescaling
# normalize to between 0 and 100 --> integers
def norm_seq(dat):
    mx = sp.amax(dat)
    mn = sp.amin(dat)
    norm_dat = (dat - mn) * (100.0 / (mx - mn))
    return full_dat.astype(sp.int0) 


#### Padding
# add 0s to beginning and end
def pad(dat, pad_size):
    zer = sp.zeros((pad_size))
    return sp.hstack((zer, dat, zer))


#### Sin
def sin_gen(t, scale):
    return sp.sin(t * scale) 


#### 1st order ~ supplied patterns
# constrain the 1st derivative
# randomly run through the supplied pattern of 1st derivs
# pip = pattern init probability
# nmag = noise magnitude, nmag0 = 0th order noise, nmag1 = 1st order 
def order1_patterns(t, patterns, pips, nmag0, nmag1):
    # max pattern length?
    maxl = 0
    for i in range(len(patterns)):
        if(len(patterns[i]) > maxl):
            maxl = len(patterns[i])

    order1 = sp.zeros((len(t)))
    for i in range(len(t)-maxl):
        # init any of the patterns:
        for j in range(len(pips)):
            if(sp.rand() < pips[j]):
                # add pattern to order 1:
                curl = len(patterns[j])
                order1[i:i+curl] = order1[i:i+curl] + patterns[j] 

    # 1st order noise:
    noise1 = (sp.rand(len(t)) - .5) * nmag1
    # 0th order noise:
    noise0 = (sp.rand(len(t)) - .5) * nmag0

    # add 1st order noise
    order1 = order1 + noise1
    # convert back to 0th order
    order0 = sp.cumsum(order1)
    order0 = order0 + noise0 
    return order0 

              

if(__name__ == '__main__'):

    t = sp.arange(0,500,1)
    patterns = [sp.array([1.0, -.5, 1.0, -.5, 1.0, -2.0])]
    print(sp.sum(patterns[0]))
    pips = [.05]
    nmag0 = 2.0
    nmag1 = 0.0
    dat = order1_patterns(t, patterns, pips, nmag0, nmag1)      
    plt.figure()
    plt.plot(t, dat)
    plt.show() 



