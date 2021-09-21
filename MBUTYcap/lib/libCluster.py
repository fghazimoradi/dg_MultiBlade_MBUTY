#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 10:46:16 2021

@author: francescopiscitelli
"""

import numpy as np
import time
import sys


from lib import libReadPcapngVMM as pcapr
from lib import libSampleData as sdat
from lib import libMapping as maps
from lib import libHistograms as hh
from lib import libPlotting as plo
from lib import libParameters as para


# NOTE  IF YOU CLUSTERIZE AGAIN THE SAME CASSETTE -> exit

###############################################################################
###############################################################################

class events():
    def __init__(self): 
        
        self.Cassette     = np.zeros((0), dtype = 'float64') 
        self.CassetteIDs  = np.zeros((0), dtype = 'float64') 
        self.positionW    = np.zeros((0), dtype = 'float64') 
        self.positionS    = np.zeros((0), dtype = 'float64') 
        
        self.timeStamp = np.zeros((0), dtype = 'float64')
        
        self.PHW = np.zeros((0), dtype = 'float64') 
        self.PHS = np.zeros((0), dtype = 'float64') 
        
        self.multW = np.zeros((0), dtype = 'float64') 
        self.multS = np.zeros((0), dtype = 'float64') 
        
        self.positionWmm  = np.zeros((0), dtype = 'float64')
        self.positionSmm  = np.zeros((0), dtype = 'float64')
        self.positionZmm  = np.zeros((0), dtype = 'float64')
        self.wavelength   = np.zeros((0), dtype = 'float64')
        self.ToF          = np.zeros((0), dtype = 'float64')
        
        self.Nevents          = np.zeros((0), dtype = 'float64') 
        self.NeventsNotRejAll = np.zeros((0), dtype = 'float64') 
        self.NeventsNotRej2D  = np.zeros((0), dtype = 'float64') 
        self.NeventsNotRejAfterTh  = np.zeros((0), dtype = 'float64') 
        
    def append(self, eve):
        
        self.CassetteIDs = np.append(self.CassetteIDs, eve.CassetteIDs)
        self.Cassette    = np.concatenate((self.Cassette, eve.Cassette), axis=0)
        self.positionW   = np.concatenate((self.positionW, eve.positionW), axis=0)
        self.positionS   = np.concatenate((self.positionS, eve.positionS), axis=0)
        self.timeStamp   = np.concatenate((self.timeStamp, eve.timeStamp), axis=0)
        self.PHW         = np.concatenate((self.PHW, eve.PHW), axis=0)
        self.PHS         = np.concatenate((self.PHS, eve.PHS), axis=0)
        self.multW       = np.concatenate((self.multW, eve.multW), axis=0)
        self.multS       = np.concatenate((self.multS, eve.multS), axis=0)
        
        self.Nevents     = np.append(self.Nevents, eve.Nevents)
        self.NeventsNotRejAll = np.append(self.NeventsNotRejAll, eve.NeventsNotRejAll)
        self.NeventsNotRej2D  = np.append(self.NeventsNotRej2D, eve.NeventsNotRej2D)
        self.NeventsNotRejAfterTh  = np.append(self.NeventsNotRejAfterTh, eve.NeventsNotRejAfterTh)
        
        self.positionWmm  = np.concatenate((self.positionWmm, eve.positionWmm), axis=0)
        self.positionSmm  = np.concatenate((self.positionSmm, eve.positionSmm), axis=0)
        self.positionZmm  = np.concatenate((self.positionZmm, eve.positionZmm), axis=0)
        self.ToF          = np.concatenate((self.ToF, eve.ToF), axis=0)
        self.wavelength   = np.concatenate((self.wavelength, eve.wavelength), axis=0)
        
    def appendSelection(self, eve, boolArray):
        
        self.Cassette    = np.concatenate((self.Cassette, eve.Cassette[boolArray]), axis=0)
        self.positionW   = np.concatenate((self.positionW, eve.positionW[boolArray]), axis=0)
        self.positionS   = np.concatenate((self.positionS, eve.positionS[boolArray]), axis=0)
        self.timeStamp   = np.concatenate((self.timeStamp, eve.timeStamp[boolArray]), axis=0)
        self.PHW         = np.concatenate((self.PHW, eve.PHW[boolArray]), axis=0)
        self.PHS         = np.concatenate((self.PHS, eve.PHS[boolArray]), axis=0)
        self.multW       = np.concatenate((self.multW, eve.multW[boolArray]), axis=0)
        self.multS       = np.concatenate((self.multS, eve.multS[boolArray]), axis=0)
        self.positionWmm = np.concatenate((self.positionWmm, eve.positionWmm[boolArray]), axis=0)
        self.positionSmm = np.concatenate((self.positionSmm, eve.positionSmm[boolArray]), axis=0)
        self.positionZmm = np.concatenate((self.positionZmm, eve.positionZmm[boolArray]), axis=0)
        self.ToF         = np.concatenate((self.ToF, eve.ToF[boolArray]), axis=0)
        self.wavelength  = np.concatenate((self.wavelength, eve.wavelength[boolArray]), axis=0)
        
        
        # self.CassetteIDs = np.unique(self.Cassette)
        # self.CassetteIDs = np.append(self.CassetteIDs, eve.CassetteIDs)
        
        CassIDs = np.unique(eve.Cassette[boolArray])
        
        self.CassetteIDs = np.append(self.CassetteIDs, CassIDs)
        
        indexes = []
        for ids in CassIDs:
            indexes.append(np.argwhere(eve.CassetteIDs == ids))
        
        # self.Nevents     = np.append(self.Nevents, eve.Nevents[indexes])
        
        self.Nevents     = np.append(self.Nevents, eve.Nevents[tuple(indexes)])
        
        self.NeventsNotRejAll = np.append(self.NeventsNotRejAll, eve.NeventsNotRejAll[tuple(indexes)])
        self.NeventsNotRej2D  = np.append(self.NeventsNotRej2D, eve.NeventsNotRej2D[tuple(indexes)])
        
        self.NeventsNotRejAfterTh  = np.append(self.NeventsNotRejAfterTh, np.sum(boolArray))

        
    def transform(self, cassette1ID, POPH):
     
        self.CassetteIDs = cassette1ID
        self.Cassette  = cassette1ID*np.ones(np.shape(POPH)[0])
        self.positionW = POPH[:,0]
        self.positionS = POPH[:,1]
        self.timeStamp = POPH[:,2]
        self.PHW       = POPH[:,3]
        self.PHS       = POPH[:,4]
        self.multW     = POPH[:,5]
        self.multS     = POPH[:,6]
        
        
    def createAbsUnitsArrays(self):
         
        leng = len(self.positionW)
         
        self.positionWmm  = np.zeros((leng), dtype = 'float64')
        self.positionSmm  = np.zeros((leng), dtype = 'float64')
        self.positionZmm  = np.zeros((leng), dtype = 'float64')
        self.wavelength   = np.zeros((leng), dtype = 'float64')
        self.ToF          = np.zeros((leng), dtype = 'float64')
        
    def concatenateEventsInArrayForDebug(self):
        
        leng = len(self.Cassette)
        
        eventsArray = np.zeros((leng,8),dtype = 'float64')
        
        eventsArray[:,0] = self.timeStamp
        eventsArray[:,1] = self.Cassette
        eventsArray[:,2] = self.positionW
        eventsArray[:,3] = self.positionS
        eventsArray[:,4] = self.PHW
        eventsArray[:,5] = self.PHS
        eventsArray[:,6] = self.multW
        eventsArray[:,7] = self.multS
                        
        return eventsArray
    

###############################################################################
###############################################################################

class multiplicityCount():
    def __init__(self, events): 
        
         self.flag2D = False
         self.flag1D = False

         mbins = np.arange(0,33,1)     
      
         self.wirefire  = np.zeros((len(mbins)-1))
         self.stripfire = np.zeros((len(mbins)-1))
         self.wirefire1D= np.zeros((len(mbins)-1))
                  
         TwoDim = events.positionS >= 0
         
         multiwhistcoinc = hh.histog().hist1D(mbins, events.multW[TwoDim])
         multishistcoinc = hh.histog().hist1D(mbins, events.multS)
         
         # multiwhistcoinc = np.histogram(,mbins)
         # multishistcoinc = np.histogram(events.multS,mbins)
         
         OneDim = events.positionS == -1
         multiwhist = hh.histog().hist1D(mbins, events.multW[OneDim])
         
         # multiwhist = np.histogram(events.multW[OneDim],mbins)
         
         if  sum(multiwhistcoinc) != 0:   
             self.flag2D = True
             self.wirefire  = multiwhistcoinc/sum(multiwhistcoinc)
             self.stripfire = multishistcoinc/sum(multishistcoinc[1:])
                  
         if  sum(multiwhist) != 0:
             self.flag1D = True
             self.wirefire1D  = multiwhist/sum(multiwhist)
         
         
###############################################################################         

class clusterHits():
     def __init__(self, hits, showStat): 
         
         # 0 is no stat, 1 is stat per cassette, 2 is stat for all at once 
         self.showStat = showStat
         
         self.hits = hits
  
         # intervals of showing percentage over 100%, 4 means 25%, 50%, 75% and 100%
         self.intervals = 4
         
         # number of decimals after comma in seconds, to round the serach for clusters: 6 means 1us rounding 
         self.resolution = 7
         
         self.events = events()
       
         
     def clusterize1cassette(self, cassette1ID, timeWindow):
         
         present = checkCassIDs.checkIfPresentInHits(self.hits,cassette1ID)
         
         # init an empty event obj
         self.events1Cass  = events()
         
         self.rejCounter = np.zeros(5)
         
         if present:
 
            print('\n \t clustering ... Cassette ID ',str(cassette1ID),' ',end='')
            
            # this is a trick to accept also the clusters very close in time otherwise rejected
            # Timewindowrec = np.ceil(timeWindow*1e6/3)/1e6+0.01e-6
            # timeWindow    = timeWindow+0.01e-6
            # changed later to 
            
            # this is a trick to accept also the clusters very close in time otherwise rejected
            # and also timeWindow defines the max time distance from first event and last event in a 
            # candidate cluster.
            # the recursive is the delta time between adjiacdent event in candidate but timeWindow is the max allowed 
            # gap for first and last 
            # and also add 1% to avoid rounding issues *1.01
            # timeWindow    = timeWindow*1.01
            # TimewindowRecursive = timeWindow/2
                    
            TimeWindowMax          = timeWindow*1.01
            TimeWindowRecursive    = TimeWindowMax/2
        
            ##########
         
            #select only the data relative to the wanted cassette ID
            selectCassette = self.hits.Cassette == cassette1ID
         
            # for speed the hits are inserted in an array
            # add a line at top [0,0,0,0] not to lose the 1st event
            data =  np.zeros((np.shape(self.hits.timeStamp[selectCassette])[0],4), dtype = 'float64') 
            data[:,0] = self.hits.timeStamp[selectCassette]
            data[:,1] = self.hits.WiresStrips[selectCassette]
            data[:,2] = self.hits.ADC[selectCassette]
            data[:,3] = self.hits.WorS[selectCassette]

            # add a line at top [0,0,0,0] not to lose the 1st event
            data = np.concatenate( ( np.zeros((1,np.shape(data)[1]), dtype = 'float64'), data ), axis=0)  #add a line at top not to lose the 1st event
            data[0,0] = -np.inf
 

            data[:,0] = np.around(data[:,0],decimals=self.resolution) #time rounded at 1us precision is 6 decimals, 7 is 100ns, etc...

            deltaTime = np.diff(data[:,0])                    #1st derivative of time 
            deltaTime = np.concatenate(([0],deltaTime),axis=0) #add a zero at top to restore length of vector
        
            clusterlogic = (np.absolute(deltaTime) <= TimeWindowRecursive) #is zero when a new cluster starts 
        
            # data1 = np.concatenate((data,clusterlogic[:,None]),axis=1) #this is for debugging 
        
            index = np.argwhere(clusterlogic == 0) #find the index where a new cluster may start 
            
            #################################
    
            ADCCH = np.zeros((np.shape(data)[0],12))
    
            ADCCH[:,0:3] = data[:,0:3]  # first 3 columns as data
            ADCCH[:,3]   = clusterlogic # col 3 is 0 where a new cluster may start
    
            ADCCH[:,4]   = data[:,3] == 0   # wire  
            ADCCH[:,5]   = data[:,3] == 1   # strip 
    
            ADCCH[:,6]   = data[:,1]*ADCCH[:,4]   # wire ch
            ADCCH[:,7]   = data[:,1]*ADCCH[:,5]   # strip ch
    
            ADCCH[:,8]   = data[:,2]*ADCCH[:,4]   # wire ADCs 
            ADCCH[:,9]   = data[:,2]*ADCCH[:,5]   # strip ADCs 
    
            ADCCH[:,10]  =  ADCCH[:,4]*ADCCH[:,6]*ADCCH[:,8]    # weighted position on wires
            ADCCH[:,11]  =  ADCCH[:,5]*ADCCH[:,7]*ADCCH[:,9]    # weighted position on strips
            
            #################################
 
            NumClusters = np.shape(index)[0]
            
            self.events1Cass.Nevents = NumClusters
        
            self.POPH = np.zeros((NumClusters,7))  #output data with col0 position wires, col1 poisiton strips, col2 tof, col3 pulse height wires, col4 pulse height strips, col 5 multiplicity w, col 6 muiltiplicity strips
    
            # filling ToF column
            tempTof   = data[index,0]
            self.POPH[:,2] = tempTof[:,0]     #tof
     
            #################################
            
            # add a fake last cluster to make loop up to the very last true cluster
            index = np.concatenate((index,[[np.shape(data)[0]]]),axis=0)
            ADCCH = np.concatenate((ADCCH,np.zeros((1,12))),axis=0) 
    
             #################################
            if  NumClusters >= 0:
                
                for kk in range(0,NumClusters,1):
                    
                        steps = int(NumClusters/self.intervals)+1    # equivalent as ceil rounding 
                        if np.mod(kk,steps) == 0 or kk == (NumClusters-1):
                            percents = int(round(100.0 * kk / float(NumClusters), 1))
                            print('['+format(percents,'01d') + '%]',end=' ')
                        
                        clusterq = ADCCH[index[kk,0]:index[kk+1,0],:]
                        
                        acceptWindow = ((clusterq[-1,0] - clusterq[0,0]) <= TimeWindowMax)  #max difference in time between first and last in cluster 
                       
                        clusterq = clusterq[clusterq[:,1].argsort(kind='quicksort'),:]  #order cluster by ch number
                   
                        is_wire  = clusterq[:,4] == 1
                        is_strip = clusterq[:,5] == 1
                        
                        # n wires n strips in cluster
                        ww = len(clusterq[is_wire, 4])   #num of wires in cluster
                        ss = len(clusterq[is_strip, 5])  #num of strips in cluster
            
                        
                        if (ww != 0 and ss != 0 and ss <= 63 and ww <= 31 and acceptWindow): #if there is at least 1 wire and 1 strip and no ch number above 32
            
                            mmaxw = clusterq[is_wire, 6][-1]
                            mmaxs = clusterq[is_strip, 7][-1]
                            mminw = clusterq[is_wire, 6][0]
                            mmins = clusterq[is_strip, 7][0]
                
                            neigw = (mmaxw - mminw) == (ww-1) #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
                            neigs = (mmaxs - mmins) == (ss-1)
                            
                            if (neigw == 1 and neigs == 1):    #if they are neighbour then...
                                
                                self.rejCounter[0] = self.rejCounter[0]+1;   #counter 2D
                                
                                self.POPH[kk,5]   = ww     #multiuplicity wires
                                self.POPH[kk,6]   = ss     #multiuplicity strips
                                self.POPH[kk,3]   = np.sum(clusterq[:,8],axis=0)   #PH wires
                                self.POPH[kk,4]   = np.sum(clusterq[:,9],axis=0)   #PH strips
                                self.POPH[kk,0]   = round((np.sum(clusterq[:,10],axis=0))/(self.POPH[kk,3]),2)         #position wires 0 to 31
                                self.POPH[kk,1]   = round((((np.sum(clusterq[:,11],axis=0))/(self.POPH[kk,4]))),2)     #position strips from 0 to 31 or up to 63
                
                            else:
                                self.rejCounter[1] = self.rejCounter[1]+1;                #counter if they are no neighbour 
                                
                        elif (ww >= 1 and ss == 0 and ww <= 31 and acceptWindow): #put in 1D hist only for wires when there is no strip 
                                
                            mmaxw = clusterq[is_wire, 6][-1]
                            mminw = clusterq[is_wire, 6][0] 
                
                            neigw = (mmaxw - mminw) == (ww-1)    #if event repated is rejected because neigw is 1 even if the same wire is repeated and should be 2 
                           
                            if (neigw == 1):    #if they are neighbour then...
                    
                                self.rejCounter[2] = self.rejCounter[2]+1;                #counter 1D
                    
                                self.POPH[kk,5]   = ww     #multiuplicity wires
                                self.POPH[kk,3]   = np.sum(clusterq[:,8],axis=0)   #PH wires
                                self.POPH[kk,0]   = round((np.sum(clusterq[:,10],axis=0))/(self.POPH[kk,3]),2)         #position wires
                                self.POPH[kk,1]   = -1 #position strips if absent
                                   
                            else:
                                self.rejCounter[1] = self.rejCounter[1]+1              #counter if they are no neighbour 
                                
                        elif (ww >= 32 or ss >= 64):
                              self.rejCounter[3] = self.rejCounter[3]+1               #counter if cluster above possible limits          
                              print('\n cluster > 32 in either directions w or s -> probably rate too high \n')
                             
                        else:
                            self.rejCounter[4] = self.rejCounter[4]+1               #any other case not taken into account previously
                            
                
                # print('\n')        
                   
                rejected = np.logical_and((self.POPH[:,5] == 0),(self.POPH[:,6] == 0))    #remove rejected from data in rejCoiunter[4] it is when only strips and wire and sgtrip mult is 0, whole row in POPH is 0 actually 
                    
                self.POPH     = self.POPH[np.logical_not(rejected),:]    #remove rejected from data
                
                # self.events.NeventsNotRejAll = self.events.Nevents - (self.rejCounter[1]+self.rejCounter[3]+self.rejCounter[4]);
                # self.events.NeventsNotRej2D   = np.sum(self.POPH[:,1] >= 0)
                
                self.events1Cass.NeventsNotRejAll = self.rejCounter[0] + self.rejCounter[2]
                self.events1Cass.NeventsNotRej2D  = self.rejCounter[0]
                
                self.events1Cass.transform(cassette1ID, self.POPH)
        
        ################################
                if self.showStat == 'individualStat':
                    self.someStat(self.events1Cass,self.rejCounter)
        ################################
        
                del self.POPH
                
                if NumClusters == len(self.hits.timeStamp[selectCassette]):
                    print('--> \033[1;33mWARNING: time window for clustering might be too small!\033[1;37m',end='')
                    time.sleep(1)
                
        
            # return data, self.POPH   
        
     
     def someStat(self, events, rejCounter):
         
            Ncandidates      = np.sum(events.Nevents)
            NeventsNotRejAll = np.sum(events.NeventsNotRejAll)
            # some stats  
            
            multi  = multiplicityCount(events)
                      
            if NeventsNotRejAll != 0 :
                rej2 = 100*(rejCounter/Ncandidates)

                print("\n\n\t N of candidates: %d -> not rejected events %d (%.1f%%) (2D: %d (%.1f%%), 1D: %d (%.1f%%))" % (Ncandidates,NeventsNotRejAll,100*NeventsNotRejAll/Ncandidates,rejCounter[0],100*rejCounter[0]/NeventsNotRejAll,rejCounter[2],100*rejCounter[2]/NeventsNotRejAll))
                print("\t not rej (2D) %.1f%%, only w (1D) %.1f%%, rejected (2D or 1D) %.1f%%, rejected >32 %.1f%%, rejected other reasons (only strips - noise)  %.1f%% \n" % (rej2[0],rej2[2],rej2[1],rej2[3],rej2[4]));
                # print("\t not rej (2D) %.1f%%, only w (1D) %.1f%% \n " % (rej3[0],rej3[2]))
                  
                if  multi.flag2D:        
                    print(' \t multiplicity:')      
                    print(" \t 2D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*multi.wirefire[1],100*multi.wirefire[2],100*multi.wirefire[3],100*multi.wirefire[4],100*multi.wirefire[5])); 
                    print(" \t 2D: percentage of strips fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5)" % (100*multi.stripfire[1],100*multi.stripfire[2],100*multi.stripfire[3],100*multi.stripfire[4],100*multi.stripfire[5])); 
                        
                if  multi.flag1D:            
                    print(" \t 1D: percentage of  wires fired per event: %.1f%% (1), %.1f%% (2), %.1f%% (3), %.1f%% (4), %.1f%% (5) \n" % (100*multi.wirefire1D[1],100*multi.wirefire1D[2],100*multi.wirefire1D[3],100*multi.wirefire1D[4],100*multi.wirefire1D[5])); 
            
            else:
                    print("\t N of candidates: %d -> not rejected events %d (2D: %d, 1D: %d)" % (Ncandidates,NeventsNotRejAll,rejCounter[0],rejCounter[2]))
                    
                
            


                

     def clusterizeManyCassettes(self, cassettesIDs, timeWindow):
            
             checkCassIDs.checkIfRepeatedIDs(cassettesIDs)
             
             self.rejCounterAll = np.zeros((5))
             
             for cc in cassettesIDs:
                 
                 self.clusterize1cassette(cc, timeWindow)
                 
                 self.events.append(self.events1Cass)
                 
                 self.rejCounterAll += self.rejCounter
                 
                 
             del self.events1Cass   
             
             if self.showStat == 'globalStat':
                 self.someStat(self.events,self.rejCounterAll)
  
    
####################################################
class checkCassIDs():  
    
    def checkIfRepeatedIDs(cassettesIDs):
         
         presentCassettes = np.unique(cassettesIDs)
         
         if len(presentCassettes) != len(cassettesIDs):
        
              print('\t \033[1;33mWARNING: Repeated entries in Cassette IDs ',str(cassettesIDs),' ... exiting.', end=' ')
              print('\033[1;37m')
              time.sleep(3)
              sys.exit()
 
    def checkIfPresentInHits(hits,cassette1ID):
         
         presentCassettes = np.unique(hits.Cassette[~np.isnan(hits.Cassette)])
         
         if not(cassette1ID in presentCassettes):
             
             flag = False 
             
             print('\n \t \033[1;33mWARNING: Cassette ID ',str(cassette1ID),' not found! Skipped! These hits only contains Cassettes IDs:', end=' ')
             for cc in presentCassettes:
                 print(int(cc),end=' ')
             print('\033[1;37m',end=' ')
         else: 
             flag = True
             
         return flag 
     
    def checkIfPresentInEvents(events,cassette1ID):
         
         presentCassettes = np.unique(events.Cassette[~np.isnan(events.Cassette)])
         
         if not(cassette1ID in presentCassettes):
             
             flag = False 
             
             # print('\n \t \033[1;33mWARNING: Cassette ID ',str(cassette1ID),' not found! Skipped! These events only contains Cassettes IDs:', end=' ')
             # for cc in presentCassettes:
             #     print(int(cc),end=' ')
             # print('\033[1;37m',end=' ')
         else: 
             flag = True
             
         return flag 
     
###############################################################################
###############################################################################

if __name__ == '__main__':

   filePath  = './config/'+"MB300_FREIA_config.json"
   filePathD = './data/'+'freia_1k_pkts_ng.pcapng'
   
   tProfilingStart = time.time()

   config = maps.read_json_config(filePath)
   
   parameters = para.parameters(config)
   parameters.cassettes.cassettes = [1]
   
   # name = config.get_DetectorName()
   # config.get_cassettesInConfig()
   
   # config.get_cassID2RingFenHybrid(5)
   # print(config.RingID, config.FenID, config.hybridID)
   # config.get_cassID2RingFenHybrid(55)
   # print(config.RingID, config.FenID, config.hybridID)
   # config.get_cassID2RingFenHybrid(1)
   # print(config.RingID, config.FenID, config.hybridID)
   
   # config.get_cassID2RingFenHybrid([1,41])
   

   
   # pr = pcapr.pcap_reader(filePathD)
   #   #  # pr.debug = True
   # pr.read()
   # vmm1 = pr.readouts
   
   # vmm2 = sdat.sampleData()
   # vmm2.fill()

   # cassettes = [1,2,3,4,5]

   # re  = maps.mapDetector(vmm1, filePath)
   #    # re.debug = False
   #    # re.initCatData()

   # re.mappAllCassAndChannels_GlobalCoord(cassettes)
   # hits = re.hits
   
   Nhits = 1e4
   cassettes = [1]
     
   bb = sdat.sampleHitsMultipleCassettes(cassettes,'./data/')
   bb.generateGlob(Nhits)
   
   hitsArray = bb.hits.concatenateHitsInArrayForDebug()
   
   hits = bb.hits
   
   ## # # # # # # # # # #  
   # aa = sdat.sampleReadouts2()
   # aa.fill()
   # readouts = aa.readouts
   
   # # map data
   # md  = maps.mapDetector(readouts, config)
   # md.mappAllCassAndChannelsGlob()
   # hits = md.hits
   ## # # # # # # # # # #
   # cc = clusterHits(hits) 
   
   # allEvents= events()
   # aa, bb = cc.clusterize1cassette(1,2e-6)
   
   # allEvents.append(cc.events)
   
   # dd = np.loadtxt('dataset1_large_Sorting=True_Filtering=False_Clustered.txt',dtype='float64',delimiter=' ')
   
   
   # aa1, bb1 = cc.clusterize1cassette(3,2e-6)
   
   # allEvents.append(cc.events)
   
   showStat = 'globalStat'
   
   cc = clusterHits(hits, showStat)
   
   # cc.checkIfRepeatedIDs([1,1,2,3,56])
   
   # cc.clusterize1cassette(1,2e-6)
   
   cc.clusterizeManyCassettes([1], 2e-6)
   
   
   
   events =  cc.events
   
   eventsArray = events.concatenateEventsInArrayForDebug()
   
   allAxis = hh.allAxis()
   allAxis.createAllAxis(parameters)
   
   pp = plo.plottingEvents(events,allAxis)
    
   pp.plotXYToF(logScale = False, absUnits = False)
   
   
   tElapsedProfiling = time.time() - tProfilingStart
   print('\n Completed in %.2f s' % tElapsedProfiling) 