import numpy as np;
import soundfile as sf;
from sklearn.metrics import mean_squared_error;
import matplotlib.pyplot as plt;

from act import ACT;
from est import EST;
from call import CALL;
from toa import TOA;

class RUN:
    '''
    Class for running tests to find actual and 
    estimated arrival times for a set of sensors
    and a target.
    
    Methods
    -------
    get_RMSE
        Returns the root-mean-squared error.
    
    get_dTSE
        Returns the estimated arrival time for 
        each sensor.
    '''
    
    def __init__(self, target, sensors, s2n, f_call, f_sea, no_blocks):
        self.t         = target;
        self.s         = sensors;
        self.s2n       = s2n;
        self.f_call    = f_call;
        self.f_sea     = f_sea;
        self.no_blocks = no_blocks;
    
    def get_rmse(self):
        self.set_pars();
        self.set_act();
        self.set_call();
        self.set_est();
            
        rmse = mean_squared_error(self.dTSA, self.dTSE, squared=False);
        
        return rmse;
    
    def get_dTSE(self):
        return self.dTSE;
        
    def set_pars(self):
        self.x = np.array(self.s).transpose()[0];
        self.y = np.array(self.s).transpose()[1];
        self.n = len(self.s);
        
    def set_act(self):
        act       = ACT(self.s, self.t);
        self.dTSA = act.get_dTSA();
        self.tTSA = act.get_tTSA();
        
    def set_call(self):
        rec_len = 10;
        call    = CALL(rec_len, self.f_call, self.tTSA, self.s2n);
        call.append_call(self.f_sea);
        
        F0, self.rate = sf.read('F0.wav');
        F1, self.rate = sf.read('F1.wav');
        F2, self.rate = sf.read('F2.wav');

        self.samples  = rec_len*self.rate;
        self.sfs = np.zeros((self.n, self.samples));

        self.sfs[0] = F0;
        self.sfs[1] = F1;
        self.sfs[2] = F2;
        
        self.pk = call.get_peak();
        
    def set_est(self):
        block_divisor = 2;
        
        toa = TOA(self.sfs, self.no_blocks, self.samples, self.rate, block_divisor);
        self.tTSE = toa.get_tTSE();

        est = EST(self.s, self.tTSE);
        self.dTSE = est.get_dTSE();