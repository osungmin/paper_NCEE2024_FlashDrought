# NCEE2024_FlashDrought

Paper codes and plot data for *"Global ecosystem responses to flash droughts are modulated by background climate and vegetation conditions"*, accepted (2024): doi not available yet.

1. See https://github.com/osungmin/FlashDrought.git for identification of flash drought events

  - Conda environment can be created from fd_ecosystem.yml
```
$ conda env create -f fd_ecosystem.yml
```


2. Python scripts to prepare plot data: /prep_scripts (Python v3)
   
  - Input data in netcdf needs to be ready; soil moisture and eco variables at 0.25 deg, pentad resolutions. 
    - ERA5 soil moisture: https://cds.climate.copernicus.eu/
    - MODIS LAI: https://lpdaac.usgs.gov/products/mod15a2hv006/
    - FLUXCOM GPP: https://www.fluxcom.org
    - GOSIF SIF: https://globalecology.unh.edu/data/GOSIF.html
  - prep_anom.py: to prepare anomalies of the considered variables. 
  - extract_vars.py: to extract the anomalies at the days of flash drought events. 
  
3. Python scripts to create paper figures: /paper_scripts (Python v3)

  - fig1.py, fig2.py, and fig3.py: python codes for the main figures.
  - unzip rawdata.zip in the same directory; this is an example raw research data with soil moisture and LAI anomalies during flash drought events.
  - Note that the final data for the main manuscript figures are under /pltdata

