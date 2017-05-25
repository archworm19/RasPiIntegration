'''

Generate Sequences of Intensity Values


'''

import scipy as sp
from scipy import random
import pylab as plt
from scipy.ndimage.filters import gaussian_filter


#### Rescaling
# normalize to between 0 and 100 --> integers
def norm_seq(dat, maxi=100):
    mx = sp.amax(dat)
    mn = sp.amin(dat)
    norm_dat = (dat - mn) * ((1.0*maxi) / (mx - mn))
    return norm_dat.astype(sp.int0) 



#### Padding
# add 0s to beginning and end
def pad(dat, pad_size):
    zer = sp.zeros((pad_size))
    return sp.hstack((zer, dat, zer))



#### Sin
def sin_gen(t, scale):
    return sp.sin(t * scale) + 1.0



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



#### Pattern vs Sorted version of pattern 
# pp = probability of pattern
# ps = probability of shuffled pattern 
# NOTE: doesn't allow for overlapping patterns
def pattern_vs_shuffled(t, pattern, pp, ps):
    patl = len(pattern)
    seq = sp.zeros((len(t)))
    i = 0
    while(i < (len(t) - patl)):
        r = sp.rand()
        if(r < pp):
            seq[i:i+patl] = seq[i:i+patl] + pattern
            i = i + patl
            continue
        if(r < (pp + ps)): 
            # copy and shuffle
            pcop = sp.copy(pattern)
            random.shuffle(pcop)
            seq[i:i+patl] = seq[i:i+patl] + pcop
            i = i + patl
            continue
        i += 1
    return seq   


#### 2 Rand Patterns ####
def two_pattern_comp(seq_len, pat_len, sum_intense, p1, p2, var):
    # generate the random patterns:
    pat1 = sp.rand(1, pat_len)
    pat1 = gaussian_filter(pat1, var)
    pat1 = pat1 - sp.amin(pat1)
    pat1 = pat1 * (sum_intense / sp.sum(pat1))
    pat2 = sp.rand(1, pat_len)
    pat2 = gaussian_filter(pat2, var)
    pat2 = pat2 - sp.amin(pat2) 
    pat2 = pat2 * (sum_intense / sp.sum(pat2))

    # iterate thru full sequence --> write patterns
    seq = sp.zeros((seq_len))
    ind = 0
    while(ind + pat_len < seq_len):
        p = sp.rand()
        if(p < p1):
            seq[ind:ind + pat_len] = pat1[:]
        elif(p < p1 + p2):
            seq[ind:ind + pat_len] = pat2[:]
        ind += pat_len
    return seq              



if(__name__ == '__main__'):

    padl = 25
    seq_len = 950
    pat_len = 25
    sum_intense = 500
    p1 = .2
    p2 = .2
    var = 5.0  
    tp = two_pattern_comp(seq_len, pat_len, sum_intense, p1, p2, var) 

    # pad:
    tp = pad(tp, padl)

    plt.figure()
    plt.plot([i for i in range(len(tp))], tp)
    plt.show() 

    sp.save('two_pattern_comp', tp)
        

