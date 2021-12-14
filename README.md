## Project (E) 448 2021

### The Development and Parameter Optimisation of a Cetacean Localisation Algorithm

The occurrence of Bryde's whales along the coasts of South Africa has, to this day, not yet been accurately assessed. For effective management and conservation of this cetacean, the ability to track and monitor its movement is imperative. Passive acoustic monitoring (PAM) is an efficient method of recording the vocalisations of Bryde's whales; the value in PAM systems lies largely in the post-processing of such recordings. 

This project details the development and optimisation of a Python algorithm that uses PAM recordings from an array of hydrophones to localise the source of significant acoustic events that occur within the recording. Cross-correlation and TDOA principles are applied to gather information from three separate recordings, with which hyperbolic trilateration is performed to produce the GPS coordinates of the source. 

The performance of the algorithm is optimised through multiple sets of simulations. Upon optimisation, the algorithm accurately localises the signal source within 1 metre. This accuracy is maintained for recordings with a signal-to-noise ratio as low as 0.5 dB.
