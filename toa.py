import numpy as np;

class TOA:
    '''
    Class for finding the estimated TOA of a 
    signal source for each sensor given sensor 
    sound files containing the same single 
    sound event. Accuracy depends on number of
    blocks B and the number of samples M.
    
    Methods
    ----------
    get_tTSE
        Returns estimated TOA for each sensor
    '''
    
    def __init__(self, sfs, no_blocks, no_samples, rate, div):
        self.sfs = sfs;
        self.B = no_blocks;
        self.M = no_samples;
        self.R = rate;
        self.n = len(sfs);
        self.D = div;
        self.corr();

    def corr(self):
        b_size = int(self.M/self.B);
        
        self.tTSE = np.zeros(self.n);
        blocks    = np.zeros(((self.n, self.B*self.D, b_size)));
        cr_en     = np.zeros((self.n, self.B*self.D));
        
        for i in range(self.B*self.D - 1):
            srt = i*int(b_size/self.D);
            stp = srt + b_size;
            blocks[0][i] = self.sfs[0][srt:stp:1];
            cr_en[0][i]  = np.correlate(blocks[0][i], blocks[0][i]);
        
        pos          = np.argmax(cr_en[0]);
        cr_call      = blocks[0][pos];
        self.tTSE[0] = (b_size*(pos/self.D))/self.R;
        
        for j in range(1, self.n):
            for i in range(self.B*self.D - 1):
                srt = i*int(b_size/self.D);
                stp = srt + b_size;
                blocks[j][i] = self.sfs[j][srt:stp:1];
                cr_en[j][i]  = np.correlate(blocks[j][i], cr_call);
                
            pos = np.argmax(cr_en[j]);
            self.tTSE[j] = (b_size*(pos/self.D))/self.R;

    def get_tTSE(self):
        return self.tTSE;