'''

Generate Sequences of Intensity Values


'''

import scipy as sp
from scipy import random
import pylab as plt
from scipy.ndimage.filters import gaussian_filter
from scipy.misc import factorial 


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


#### Taylor series pattern creation
# specify num_t
# specify taylor series parameters
# set minimum to zero
def taylor_gen(num_t, taylor_params):
    t = sp.arange(0, num_t, 1.0)
    x = sp.zeros(sp.shape(t))
    for i in range(len(taylor_params)):
        x = x + (taylor_params[i]/factorial(i)) * (t**i)
        print((taylor_params[i]/factorial(i))) 
    plt.figure()
    plt.plot(t,x)
    plt.show() 
        

#### Root-Based Polynomial Creation ####
# specify num_t
# specify roots
def poly_root_gen(num_t, roots, end_sign=1):
    t = sp.arange(0, num_t, 1.0) - (num_t/2)  
    x = sp.ones(sp.shape(t))
    for root in roots:
        x = x * (t - root)
    x = end_sign * x
    # move min to 0 and normalize:
    x = x - sp.amin(x)
    x = x / sp.amax(x) 
    return x


#### Gaussian Mixture Pattern ####

def gauss_func(x, mu, stddev, scale):
    return scale * sp.exp(-((x - mu)**2.0) / (2*(stddev**2.0)))

# recieves 3 lists: (mus, stddevs, scales)
def gauss_mix_pattern(t, mus, stddevs, scales):
    stim = sp.zeros((len(t)))
    for i in range(len(mus)):
        stim += gauss_func(t, mus[i], stddevs[i], scales[i])
    return stim  



#### Pattern Tiling of Sequence
# put patterns into sequence with some probability
# Assumes all patterns have the same length
def pattern_tile(num_t, patterns, probs):
    if(sp.sum(probs) > 1):
        print('illegal probs')
        return 
    cs = sp.cumsum(probs) 
    print(cs) 
    plen = len(patterns[0]) 
    num_iters = int(num_t / plen)
    x = sp.zeros((num_t))
    for i in range(num_iters):
        seq_start = i * plen
        seq_end = (i+1) * plen
        r = sp.rand()
        print(r) 
        ind = sp.where(r < cs)[0]
        if(len(ind) <= 0):
            continue
        pind = ind[0]
        print(pind)  
        x[seq_start:seq_end] = patterns[pind] 
    return x 




if(__name__ == '__main__'):
    
    num_t = 50
    t = sp.array([i for i in range(num_t)])   
 
    # stim 1:
    mus1 = [10, 20, 40]
    stddevs1 = [2.0, 2.0, 2.0]
    scales1 = [50, 90, 50]
    stim1 = gauss_mix_pattern(t, mus1, stddevs1, scales1)

    # stim 2:
    mus2 = [10, 30, 40]
    stddevs2 = [2.0, 2.0, 2.0]
    scales2 = [50, 90, 50]
    stim2 = gauss_mix_pattern(t, mus2, stddevs2, scales2)

    plt.figure()
    plt.plot(stim1)
    plt.plot(stim2)
    plt.show() 

    super_stim = pattern_tile(1000, [stim1, stim2], [.25, .25])

    plt.figure()
    plt.plot(super_stim)
    plt.show()

    sp.save('two_pattern_gauss', super_stim) 





