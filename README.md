# Journal2023_FlashDrought

Paper codes for *"Divergent ecosystem responses to flash droughts across climate-vegetation regimes"*, submitted (2023): doi not available yet.

1. See https://github.com/osungmin/Flash_Drought.git for identification of flash drought events

  - Conda environment can be created from fd_ecosystem.yml
```
$ conda env create -f fd_ecosystem.yml
```

2. Python scripts to prepare anomalies of considered variables: /prep_anomly (Python v3)
  - Input data in netcdf needs to be ready; we used ERA5 for meteorological data and MODIS, FLUXCOM, GOSIF data for ecological variables.
    - ERA5 meteorological data: https://cds.climate.copernicus.eu/
    - MODIS LAI: https://lpdaac.usgs.gov/products/mod15a2hv006/
    - FLUXCOM GPP: https://www.fluxcom.org
    - GOSIF SIF: https://globalecology.unh.edu/data/GOSIF.html
  - prep_anom.py
  
3. Python scripts to create paper figures: /paper_scripts (Python v3)
  - unzip pltdata.zip in the same directory; this is an example data with soil moisture and LAI anomalies during flash drought events
  - fig1.py, fig2.py, and fig3.py for each figure in the paper. 
