import soundfile as sf;
import numpy as np;
import matplotlib.pyplot as plt;

class CALL:
    '''
    Class for creating delayed sound files of 
    a certain length S given a call file,
    arrival times per sensor and a signal
    to noise ratio.
    
    Methods
    -------
    append_call
        Appends call to sea noise files
    get_peak
        Returns the peak value of a vocalisation
    
    Example
    -------
    >>> from call import CALL
    >>> tTS = [3.68526045,  6.08118478,  4.89982666];
    >>> call = CALL(10, 'Call0.wav', tTS, 5);
    >>> f_sea = ['Sea0.wav', 'Sea1.wav', 'Sea2.wav'];
    >>> call.append_call(f_sea);
    '''
    
    def __init__(self, length, f_call, tTS, s2n):
        self.length = length;
        self.data, self.rate = sf.read(f_call);
        self.tTS = tTS;
        self.noise_ratio = 1/s2n;
        self.set_pars();
    
    def set_pars(self):
        self.l = len(self.data);
        self.n = len(self.tTS);
        self.c = np.argmin(self.tTS);
        self.m = self.length*self.rate;
        
    def get_peak(self):
        self.peak = np.amax(self.data);
        return self.peak;
        
    def append_call(self, f_sea):
        start = np.zeros(self.n);
        sea   = np.zeros((self.n, self.m));
        dd    = np.zeros((self.n, self.l));
        mu    = 0; 
        pk    = np.argmax(self.data);
        
        for i in range(self.n):
            dd[i] = self.data;        
            sea[i], r = sf.read(f_sea[i]);
        
        sfs = sea;
        
        for i in range(self.n):
            start[i] = int(self.tTS[i]*self.rate - pk);
            
            for j in range(self.l):
                ref = int(start[i] + j);
                sfs[i][ref] = dd[i][j];
            
            noise = np.random.normal(mu, self.noise_ratio*self.get_peak(), self.m);
            sfs[i] = sfs[i] + noise;
                
        sf.write('F0.wav', sfs[0], self.rate);
        sf.write('F1.wav', sfs[1], self.rate);
        sf.write('F2.wav', sfs[2], self.rate);