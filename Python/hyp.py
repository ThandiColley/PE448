import numpy as np;
import math;
import matplotlib.pyplot as plt;
from obspy.geodetics import kilometers2degrees as km2deg;
import itertools;

class HYP:
    '''
    Class for plotting the estimated location
    of a signal source using hyperbola theory.
    
    Methods
    -------
    plot_sensors
        Plots sensors.
        
    plot_target
        Plots actual target.
        
    plot_hyp
        Plots estimation hyperbole.
    '''
    
    def __init__(self, sensors, target, dTS):
        self.S   = sensors;
        self.T   = target;
        self.dTS = km2deg(dTS);
        
        self.set_params();
    
    def set_params(self):
        self.n = len(self.S);
        self.x = np.array(self.S).transpose()[0];
        self.y = np.array(self.S).transpose()[1];
        
        self.dSS   = np.zeros(self.n);
        self.theta = np.zeros(self.n);
        self.d     = np.zeros(self.n);
        self.a     = np.zeros(self.n);
        self.b     = np.zeros(self.n);
        mid = np.zeros((self.n, 2));
        
        for i in range(self.n):
            self.dSS[i] = math.sqrt((self.x[(i+1)%len(self.x)]-self.x[i])**2 + (self.y[(i+1)%len(self.y)]-self.y[i])**2);
            mid[i][0] = (self.x[(i+1)%len(self.x)]+self.x[i])/2;
            mid[i][1] = (self.y[(i+1)%len(self.y)]+self.y[i])/2;
            
            slope         = (self.y[(i+1)%len(self.y)]-self.y[i]) / (self.x[(i+1)%len(self.x)]-self.x[i])
            self.theta[i] = -math.atan(slope);
    
            if slope <= 0:
                self.theta[i] = -math.pi/2 + self.theta[i];
            else:
                self.theta[i] =  math.pi/2 + self.theta[i];
            
        self.midx = np.array(mid).transpose()[0];
        self.midy = np.array(mid).transpose()[1];
        
        self.xmax = max(max(self.x), self.T[0]);
        self.xmin = min(min(self.x), self.T[0]);
        self.ymax = max(max(self.y), self.T[1]);
        self.ymin = min(min(self.y), self.T[1]);
        
        for i in range(self.n):
            self.d[i] = self.dSS[i]/2;
            self.a[i] = abs(self.dTS[i] - self.dTS[(i+1)%len(self.dTS)])/2;
            self.b[i] = math.sqrt(self.d[i]**2 - self.a[i]**2);
            
    def plot_sensors(self):
        
        buff = 0.001;
        
        plt.xlim((self.xmin-(buff)) , (self.xmax+(buff)));
        plt.ylim((self.ymin-(buff)) , (self.ymax+(buff)));
        
        for i in range(self.n):
            plt.annotate("  S" + str(i), (self.x[i], self.y[i]));
        plt.scatter(self.x, self.y, color='k', marker='^');
    
    def plot_target(self):
        plt.annotate("  W", (self.T[0], self.T[1]));
        plt.scatter(self.T[0], self.T[1], color='k', marker='s');
        
    def plot_hyp(self):
        buff = 0.02;
        xp   = np.linspace(-10*(self.xmax-self.xmin), 10*(self.xmax-self.xmin), 1001);
        colora = itertools.cycle(["hotpink", "orange", "deepskyblue"]);
        colorb = itertools.cycle(["hotpink", "orange", "deepskyblue"]);
        
        plt.xlim((self.xmin-(buff)) , (self.xmax+(buff)));
        plt.ylim((self.ymin-(buff)) , (self.ymax+(buff)));
        
        for i in range(self.n):
            y1 = np.sqrt((self.a[i]**2)*(1 + ((xp**2) / (self.b[i]**2))));
            y2 = -y1;
    
            x1rot = xp*math.cos(self.theta[i]) + y1*math.sin(self.theta[[i]]);
            x2rot = xp*math.cos(self.theta[i]) + y2*math.sin(self.theta[[i]]);
            y1rot = -xp*math.sin(self.theta[i]) + y1*math.cos(self.theta[[i]]);
            y2rot = -xp*math.sin(self.theta[i]) + y2*math.cos(self.theta[[i]]);
        
            plt.plot(x1rot + self.midx[i], y1rot + self.midy[i], color=next(colora), linewidth=1);
            plt.plot(x2rot + self.midx[i], y2rot + self.midy[i], color=next(colorb), linewidth=1);
        