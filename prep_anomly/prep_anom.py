#!/usr/bin/env python
import pandas as pd
import numpy as np
from netCDF4 import Dataset
print ("modules imported")

def nc_anom(var, yrs, detrend=False):
   ###
   ncpath="your_path_to_netcdf_files"
   outpath="your_path_to_output_directory"
   outfname_norm="anom.norm_"+var+"."+str(yrs[0])+"-"+str(yrs[-1])+".dat"
   
   ###
   n_days=73 #worked on pentad data
   flat, flon='lat','lon' #variable name for lat/lon in the netcdf
   
   print()
   print("*** anom ***", var)
   print(" >>", yrs[0], yrs[-1])
   print()

   nc_files=[]
   for yr in yrs:

     f = Dataset(ncpath+str(yr)+'.nc', 'r') #open netcdf by year
     nc= f.variables[var][:,:,:].filled(np.nan)
     lats= f.variables[flat]
     lons= f.variables[flon]

     if yr==yrs[0]: print(nc.shape, lats[:3], lons[:3]) #just to check
     f.close()
    
     nc_files.append(nc)

   append = np.concatenate(nc_files, axis=0) #concatenate netcdfs into 3d array
   print(" done,", len(yrs), "==?", len(nc_files), "append:", append.shape)
   if len(append) != len(yrs)*n_days: stop #just to check

   #computing long-term mean over th eperiod
   long_mean= np.nanmean(append[:,:,:], axis=0)
   print(" - long mean", long_mean.shape)
   print()

   #computing mean and std for the same n-th day
   _nc_mean, _nc_std = [], []
   for i in range(n_days):

      _idx=np.arange(i, len(append), n_days)

      #if i==0: print(_idx) #just to check
      #if i==n_days: print(_idx)

      # i-th day mean and std
      _nc_mean.append(np.reshape(np.nanmean(append[_idx,:,:], axis=0), (1,nc.shape[1],nc.shape[2])))
      _nc_std.append(np.reshape(np.nanstd(append[_idx,:,:], axis=0, ddof=1),(1,nc.shape[1],nc.shape[2])))

   print(" - mean and std for each day/pentad:", len(_nc_mean), len(_nc_std))
   #repeating mean and std; 73 values to 73 * # of years (working on pentad - 75 days!)
   nc_mean = np.tile(np.concatenate(_nc_mean, axis=0), (len(yrs),1,1))
   nc_std  = np.tile(np.concatenate(_nc_std, axis=0), (len(yrs),1,1))
   print(" - restructure for all years:", nc_mean.shape, nc_std.shape)
   print(" done.")

   ### computing normalised anomalies
   anoms=np.subtract(append,nc_mean)
   norm_anoms=np.divide(anoms,nc_std)
   ###

   #np.save(open(outpath+outfname_anom, 'wb'), anoms, allow_pickle=False)
   np.save(open(outpath+outfname_norm, 'wb'), norm_anoms, allow_pickle=False)
   print ("<< saved.")
   print()

    
###### define the entire period to be considered
yrs=np.arange(2001,2020+1,1)
var='swvl30' #name of variable (e.g. ERA5 soil moisture)
######

print(" **** ", var)
nc_anom(var, yrs, opt=opt, detrend=False)
print("End.")


