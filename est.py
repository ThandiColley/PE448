import math;
import numpy as np;
from obspy.geodetics import degrees2kilometers as deg2km;

class EST:
    '''
    Class for finding coordinates of a signal source given 
    coordinates for sensors S0, S1 and S2, and TOA T0, T1, T2.
    
    Methods
    ----------
    get_tTSE
        Returns the estimated TOA for each sensor
    
    get_dTSE
        Returns the estimated distance between each sensor 
        and the target
    '''
    
    def __init__(self, sensors, tTSE):
        self.sens = sensors;
        self.tTSE = tTSE;
        self.set_pars();

    def set_pars(self):
        v = 1.5;
        
        self.n = len(self.sens);
        self.x = np.array(self.sens).transpose()[0];
        self.y = np.array(self.sens).transpose()[1];
        
        self.dTSE = np.zeros(self.n);
        
        for i in range(self.n):
            self.dTSE[i] = v*self.tTSE[i];

    def get_dTSE(self):
        return self.dTSE;
    
    def get_tTSE(self):
        return self.tTSE;

