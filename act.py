import math;
import numpy as np;
from obspy.geodetics import degrees2kilometers as deg2km;

class ACT:
    '''
    Class for finding TOA of a signal source given 
    coordinates for sensors S0, S1 and S2, and target T.
    
    Methods
    ----------
    get_tTSA
        Returns the TOA for each sensor
    
    get_dTSA
        Returns the distance between each sensor and
        the target
    '''
    
    def __init__(self, sensors, target):
        self.sens = sensors;
        self.target  = target;
        self.set_pars();

    def set_pars(self):
        self.n = len(self.sens);
        self.x = np.array(self.sens).transpose()[0];
        self.y = np.array(self.sens).transpose()[1];

    def get_tTSA(self):
        v = 1.5;
        
        dTSA = self.get_dTSA;
        self.tTSA = np.zeros(self.n);
        
        for i in range(self.n):
            self.tTSA[i] = self.dTSA[i]/v;
            
        return self.tTSA;
    
    def get_dTSA(self):
        self.dTSA = np.zeros(self.n);
        
        for i in range(self.n):
            self.dTSA[i] = deg2km(math.sqrt((self.target[0]-self.x[i])**2 
                            + (self.target[1]-self.y[i])**2));
            
        return self.dTSA;
