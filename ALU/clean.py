from distillate import Distillate
import numpy as np
import qdf

def compute(input_streams):
        # data input
        LB = input_streams[0]
        LC=input_streams[1]
        LA=input_streams[2]
        raw_LB=[]
        raw_LC=[]
        raw_LA=[]
        major_good_LA=[]
        major_bad_LA=[]
        minor_good_LA=[]
        minor_bad_LA=[]
        major_good_LB=[]
        major_bad_LB=[]
        minor_good_LB=[]
        minor_bad_LB=[]
        major_good_LC=[]
        major_bad_LC=[]
        minor_good_LC=[]
        minor_bad_LC=[]
        
        # data input
        idx=0
        while idx < len(LB):
         raw_LB.append(LB[idx].value)
         idx+=1
        raw_LB=np.array(raw_LB)
        while idx < len(LB):
         raw_LB.append(LB[idx].value)
         idx+=1
        raw_LB=np.array(raw_LB)
        idx=0
        while idx < len(LA):
         raw_LA.append(LA[idx].value)
         idx+=1
        raw_LA=np.array(raw_LA)
        idx=0
        while idx < len(LC):
         raw_LC.append(LC[idx].value)
         idx+=1
        raw_LC=np.array(raw_LC)
        
        # calaulate the min outlier and major outlier
        LA_Q1=np.percentile(raw_LA,25)
        LA_Q3=np.percentile(raw_LA,75)
        LA_interquartile=LA_Q3-LA_Q1
        LA_innerfences=[LA_Q1-LA_interquartile*1.5,LA_Q3+LA_interquartile*1.5]
        LA_outerfences=[LA_Q1-LA_interquartile*3,LA_Q3+LA_interquartile*3]
        
        LB_Q1=np.percentile(raw_LB,25)
        LB_Q3=np.percentile(raw_LB,75)
        LB_interquartile=LB_Q3-LB_Q1
        LB_innerfences=[LB_Q1-LB_interquartile*1.5,LB_Q3+LB_interquartile*1.5]
        LB_outerfences=[LB_Q1-LB_interquartile*3,LB_Q3+LB_interquartile*3]
        LC_Q1=np.percentile(raw_LC,25)
        LC_Q3=np.percentile(raw_LC,75)
        LC_interquartile=LC_Q3-LC_Q1
        LC_innerfences=[LC_Q1-LC_interquartile*1.5,LC_Q3+LC_interquartile*1.5]
        LC_outerfences=[LC_Q1-LC_interquartile*3,LC_Q3+LC_interquartile*3]
        
        # classify data into difffernt group
        ldx=0
        while idx < len(LA):
         if LA[idx].value>LA_outerfences[1] or  LA[idx].value<LA_outerfences[0]:
            major_bad_LA.append((LA[idx].time, LA[idx].value))
            minor_bad_LA.append((LA[idx].time, LA[idx].value))
         elif LA[idx].value>LA_innerfences[1] or  LA[idx].value<LA_innerfences[0]:
            minor_bad_LA.append((LA[idx].time, LA[idx].value))
            major_good_LA.append((LA[idx].time, LA[idx].value))
         else:
            minor_good_LA.append((LA[idx].time, LA[idx].value))
            major_good_LA.append((LA[idx].time, LA[idx].value))
         idx+=1    
        ldx=0
        while idx < len(LB):
         if LB[idx].value>LB_outerfences[1] or  LB[idx].value<LB_outerfences[0]:
            major_bad_LB.append((LB[idx].time, LB[idx].value))
            minor_bad_LB.append((LB[idx].time, LB[idx].value))
         elif LB[idx].value>LB_innerfences[1] or  LB[idx].value<LB_innerfences[0]:
            minor_bad_LB.append((LB[idx].time, LB[idx].value))
            major_good_LB.append((LB[idx].time, LB[idx].value))
         else:
            minor_good_LB.append((LB[idx].time, LB[idx].value))
            major_good_LB.append((LB[idx].time, LB[idx].value))
         idx+=1  
        ldx=0
        while idx < len(LC):
         if LC[idx].value>LC_outerfences[1] or  LC[idx].value<LC_outerfences[0]:
            major_bad_LC.append((LC[idx].time, LC[idx].value))
            minor_bad_LC.append((LC[idx].time, LC[idx].value))
         elif LC[idx].value>LC_innerfences[1] or  LC[idx].value<LC_innerfences[0]:
            minor_bad_LC.append((LC[idx].time, LC[idx].value))
            major_good_LC.append((LC[idx].time, LC[idx].value))
         else:
            minor_good_LC.append((LC[idx].time, LC[idx].value))
            major_good_LC.append((LC[idx].time, LC[idx].value))
         idx+=1    
        return[major_good_LA,major_bad_LA,minor_good_LA,minor_bad_LA,major_good_LB,major_bad_LB,minor_good_LB,minor_bad_LB,major_good_LC,major_bad_LC,minor_good_LC,minor_bad_LC]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L2ANG','upmu/grizzly_new/L3ANG'],\
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','8b80c070-7bb1-44d3-b3a8-301558d573ea',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-01T00:10:00.000000', \
         'output_streams' : ['major_good_LA','major_bad_LA','minor_good_LA','minor_bad_LA','major_good_LB','major_bad_LB',
                             'minor_good_LB','minor_bad_LB','major_good_LC','major_bad_LC','minor_good_LC','minor_bad_LC'], \
         'output_units'   : ['Degree','Degree','Degree','Degree','Degree','Degree','Degree','Degree','Degree','Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'Remove Outlier', \
         'version'        : 3, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()
