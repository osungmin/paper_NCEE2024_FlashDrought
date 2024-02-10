# NCEE2024_FlashDrought

Paper codes and plot data for *"Global ecosystem responses to flash droughts are modulated by background climate and vegetation conditions"*, Communications Earth & Environment (2024): 10.1038/s43247-024-01247-4.

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
  - rawdata.zip; example raw research data containing the list of soil moisture and LAI anomalies during flash droughts.
  - pltdats.zip; processed data for the main manuscript figures. ! unzip the data into the same directory where the python scripts are located

