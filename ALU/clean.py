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
        good_LB=[]
        good_LC=[]
        good_LA=[]
        bad_LB=[]
        bad_LC=[]
        bad_LA=[]
        idx=0
        for idx < len(LB):
         raw_LB.append(LB[idx].value)
         raw_LB=np.asarray(raw_LB)
         idx+=1
        r = boxplot(raw_LB)
        top_points_LB = r["fliers"][0].get_data()[1]
        bottom_pionts_LB = r["fliers"][2].get_data()[1]
        bottom_pionts_LB = list(bottom_pionts_LB)
        top_points_LB = list(top_points_LB)
        outliers_LB=bottom_pionts_LB+top_pionts_LB
        idx=0
        for idx < len(LA):
         raw_LA.append(LA[idx].value)
         raw_LA=np.asarray(raw_LA)
         idx+=1
        r = boxplot(raw_LA)
        top_points_LA = r["fliers"][0].get_data()[1]
        bottom_pionts_LA = r["fliers"][2].get_data()[1]
        bottom_pionts_LA = list(bottom_pionts_LA)
        top_points_LA = list(top_points_LA)
        outliers_LA=bottom_pionts_LA+top_pionts_LA
        idx=0
        for idx < len(LC):
         raw_LC.append(LC[idx].value)
         raw_LC=np.asarray(raw_LC)
         idx+=1
        r = boxplot(raw_LC)
        top_points_LC = r["fliers"][0].get_data()[1]
        bottom_pionts_LC = r["fliers"][2].get_data()[1]
        bottom_pionts_LC = list(bottom_pionts_LC)
        top_points_LC = list(top_points_LC)
        outliers_LC=bottom_pionts_LA+top_pionts_LC
        idx=0
        for idx < len(LA):
         if LA[idx].value in outliers_LA:
            bad_LA.append((LA[idx].time, LA[idx].value))              
         else:
            good_LA.append((LA[idx].time, LA[idx].value))     
         idx+=1    
        idx=0
        for idx < len(LB):
         if LB[idx].value in outliers_LB:
            bad_LB.append((LB[idx].time, LB[idx].value))              
         else:
            good_LB.append((LB[idx].time, LB[idx].value))     
         idx+=1  
        idx=0
        for idx < len(LC):
         if LC[idx].value in outliers_LC:
            bad_LC.append((LC[idx].time, LC[idx].value))              
         else:
            good_LC.append((LC[idx].time, LC[idx].value))     
         idx+=1        
        return[good_LA,bad_LA,good_LB,bad_LB,good_LC,bad_LC]
        
        
        
# set all data stream, date, distillate name, unit, output folder needed for this job     
opts = { 'input_streams'  : ['upmu/grizzly_new/L1ANG','upmu/grizzly_new/L2ANG','upmu/grizzly_new/L3ANG'],\
         'input_uids'     : ['b4776088-2f85-4c75-90cd-7472a949a8fa','8b80c070-7bb1-44d3-b3a8-301558d573ea',
                             'b653c63b-4acc-45ee-ae3d-1602e6116bc1'], \
         'start_date'     : '2014-10-01T00:00:00.000000', \
         'end_date'       : '2014-10-01T00:00:10.000000', \
         'output_streams' : ['good_LA','bad_LA','good_LB','bad_LB','good_LC','bad_LC'], \
         'output_units'   : ['Degree','Degree','Degree','Degree','Degree','Degree'], \
         'author'         : 'Andrew', \
         'name'           : 'Remove Outlier', \
         'version'        : 2, \
         'algorithm'      : compute }        
qdf.register(Distillate(), opts)
qdf.begin()
