#!/usr/bin/env python
import numpy as np
import pandas as pd
import statistics

import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
from matplotlib.lines import Line2D

import warnings
warnings.filterwarnings("ignore")
print ("modules imported")

def load_fd_vars():
    warning="""
     ***
     this is to generate plot data for Fig. 2 using rawdata.csv (sample data)
     final plot data for the figure is provided under /_pltdats
     ***
    """
    print(warning)

    #load .csv file with extracted meteo/eco variables during flash drought events
    load = pd.read_csv("./example_fd.csv",
                        header=0, index_col=0,
                        na_values=-9999.)
    #assign lat information
    lats = np.arange(89.875, -90., -0.25)
    lons = np.arange(-179.875, 180.1, 0.25)
    load['lat']=load['p'].apply(lambda x: lats[x])
    load['lon']=load['q'].apply(lambda x: lons[x])
    print(load[['p','q','lat','lon']].describe())
    return(load)

def veg_codes(code):
    if (code==1): veg_type="ENF"
    elif (code==2): veg_type="EBF"
    elif (code==3): veg_type="DNF"
    elif (code==4): veg_type="DBF"
    elif (code==5): veg_type="MF"
    elif (code==6)|(code==7): veg_type="SHR"
    elif (code==8)|(code==9): veg_type="SAV"
    elif (code==10): veg_type="GRA"
    elif (code==12)|(code==14): veg_type="CRO"
    elif (code==19): veg_type="TDR"
    return(veg_type)

def plt_basemap(ax):

    m = Basemap(projection='cyl',\
                llcrnrlat=-60, urcrnrlat=90, llcrnrlon=-180, urcrnrlon=180, lon_0=0,
                resolution='c', ax=ax)

    m.drawmapboundary(fill_color='white', zorder=-1)
    m.fillcontinents(color='0.8', lake_color='white', zorder=0)

    m.drawcoastlines(color='0.6', linewidth=0.5)
    m.drawcountries(color='0.6', linewidth=0.5)

    m.drawparallels(np.arange(-45., 180., 45.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)
    m.drawmeridians(np.arange(0., 360., 90.), labels=[1,0,0,1], dashes=[1,1], linewidth=0.25, color='0.5', fontsize=8)
    return(m)

def plt_map(ax, pltdat, m, opt=None):

    lons, lats = np.arange(-179.875, 180.1, 0.25), np.arange(89.875, -90., -0.25)
    lon, lat = np.meshgrid(lons,lats)
    xi, yi = m(lon, lat)

    boundaries = np.arange(3, 18+1, 3)
    cmap = mpl.colors.ListedColormap(["cornflowerblue","lightsteelblue","gold","darkorange","red"])
    cmap.set_over("darkred")
    cmap.set_under("royalblue")

    cs = m.pcolormesh(xi,yi,pltdat, cmap=cmap,
                      norm = mpl.colors.BoundaryNorm(boundaries, ncolors=cmap.N))

    return(m)

def plot_rec(ax, bmap, lonmin, lonmax, latmin, latmax, text=None):
    #to plot the black box for each region
    xs = [lonmin,lonmax,lonmax,lonmin,lonmin]
    ys = [latmin,latmin,latmax,latmax,latmin]
    bmap.plot(xs, ys, latlon = True, color='k', linewidth=1)
    ax.annotate(text, xy=(lonmin-3, latmax+2), xycoords='data', \
                textcoords='data', fontsize=8, weight='bold')

def plt_subset(load, subset):
    region= load[(load['lon']>subset[0])&(load['lon']<subset[1])&\
                 (load['lat']>subset[2])&(load['lat']<subset[3])].copy()

    up, bt=0.75, 0.25
    soilm_med=(region[['swvl30'+str(x) for x in np.arange(-5,20+1,1)]]).median(skipna=True)
    soilm_up=(region[['swvl30'+str(x) for x in np.arange(-5,20+1,1)]]).quantile(q=up)
    soilm_bt=(region[['swvl30'+str(x) for x in np.arange(-5,20+1,1)]]).quantile(q=bt)

    eco_med=(region[['lai.modis'+str(x) for x in np.arange(-5,20+1,1)]]).median(skipna=True)
    eco_up=(region[['lai.modis'+str(x) for x in np.arange(-5,20+1,1)]]).quantile(q=up)
    eco_bt=(region[['lai.modis'+str(x) for x in np.arange(-5,20+1,1)]]).quantile(q=bt)

    return(soilm_med, soilm_up, soilm_bt, eco_med, eco_up, eco_bt)

def comp_meteo(load, subset):
    #to plot static information on the map
    region= load[(load['lon']>subset[0])&(load['lon']<subset[1])&\
                 (load['lat']>subset[2])&(load['lat']<subset[3])].copy()
    region['grid']=region['p'].astype('str')+'_'+region['q'].astype(str)

    region_perGrid=region.drop_duplicates(subset='grid', keep='first')

    arid=np.nanmedian(region_perGrid['arid'])
    tree=np.nanmedian(region_perGrid['tree'])

    veg=statistics.mode(region_perGrid['veg'])

    plt.text(10., -1.25, 'DryIdx:'+str(round(arid,2)), fontsize=7)
    plt.text(10., -1.48, 'TreeCover:'+str(round(tree,2)), fontsize=7)
    plt.text(10., -1.71, 'DomVeg:'+veg_codes(int(veg)), fontsize=7)
    return(arid, tree)


def plt_lines(ax,soilm,soilm_up,soilm_bt,eco,eco_up,eco_bt,yaxis_opt=False):
    x_times=np.arange(-5,20+1,1)
    plt.plot(x_times, soilm, 'k-')
    plt.fill_between(x_times, soilm_up, soilm_bt, color="k", linestyle='-', alpha=0.1)
    plt.plot(x_times, eco, 'g-')
    plt.fill_between(x_times, eco_up, eco_bt, color="g", linestyle='-', alpha=0.1)

    plt.axvline(x=-2, c='grey', linewidth=0.3, linestyle=':')
    plt.axvline(x=0, c='grey', linewidth=0.3, linestyle=':')
    plt.axvline(x=10, c='grey', linewidth=0.3, linestyle=':')
    plt.axhline(y=0, c='k', linewidth=1, linestyle='-')
    ax.axvspan(-2, 0, alpha=0.3, color='lightgrey')
    plt.xlabel('Time [pentad]', labelpad=5, fontsize=9)
    plt.xticks(np.arange(0,20+1,5),['drought\nstarts',5,10,15,20], fontsize=7)
    plt.xlim(-5,20)
    
    if yaxis_opt:
        plt.ylabel('Norm. Anomaly', labelpad=10, fontsize=9)
        plt.yticks(np.arange(-2,1+1,1), fontsize=7)
    else: plt.yticks(np.arange(-2,1+1,1), ['']*len(np.arange(-2,1+1,1)), fontsize=7)
    plt.ylim(-2,1)

def main():
    ### prepare figure setting
    fig= plt.figure(figsize=(9, 7), facecolor='w', edgecolor='k')
    gs = gridspec.GridSpec(5, 1, height_ratios=[1,.25,1,0.25,1],
                           left=0.1, right=0.97,
                           top=0.95, bottom=0.1,
                           hspace=0.2)

    gs0 = gridspec.GridSpecFromSubplotSpec(1, 5,
                       subplot_spec=gs[0], width_ratios=[0.,1,1,1,0.5],
                       wspace=0.2)

    gs1 = gridspec.GridSpecFromSubplotSpec(1, 5,
                       subplot_spec=gs[2], width_ratios=[1.3,.1,2,.1,1.3],
                       wspace=0.15)

    gs2 = gridspec.GridSpecFromSubplotSpec(1, 5,
                       subplot_spec=gs[4], width_ratios=[0.,1,1,1,0.5],
                       wspace=0.2)

    ##### MAP
    ax_map = fig.add_subplot(gs1[2])
    m=plt_basemap(ax_map)

    fpath='./map_freq.dat' #this map data was created from Fig.1
    with open(fpath, 'rb') as f:
        pltdat = np.load(f)[:,:]

    plt_map(ax_map, pltdat, m)

    ##### TEMPORAL PLOTS
    #open here to create plot data
    #pltdat=load_fd_vars()

    fpath='./map_subregions.dat' 
    with open(fpath, 'rb') as f:
        pltdat = np.load(f)[:,:]
    
    ##### sub regions
    rnames=['ENA','CEU','SAS','EAS','NWS','SES','WAF','EAU']
    rareas=[[-85,-75,30,45],[0,20,45,60],[70,90,8,30],[100,120,20,35],
            [-85,-65,-5,5],[-60,-40,-30,-15],[10,25,-8,10],[145,155,-30,-20]]
    rtexts=['a','b','c','d','e','f','g','h','i']

    for i in range(8):
        print(" >>>>> ", rnames[i])

        lonmin,lonmax,latmin,latmax=rareas[i]
        plot_rec(ax_map,m,lonmin,lonmax,latmin,latmax, text=rtexts[i])

        #time series of soil moisture and ecovar
        if i==0: ax = fig.add_subplot(gs0[1])
        if i==1: ax = fig.add_subplot(gs0[2])
        if i==2: ax = fig.add_subplot(gs0[3])
        if i==3: ax = fig.add_subplot(gs1[0])
        if i==4: ax = fig.add_subplot(gs1[4])
        if i==5: ax = fig.add_subplot(gs2[1])
        if i==6: ax = fig.add_subplot(gs2[2])
        if i==7: ax = fig.add_subplot(gs2[3])

        if i in[0,3,5]: yaxis_opt=True
        else: yaxis_opt=False

        plt.text(-5, 1.2, rtexts[i]+') '+rnames[i], weight='bold', fontsize=10)
        #open here to compute temporal variations of soil moisture and eco variables
        #soilm,soilm_up,soilm_bt,eco,eco_up,eco_bt=plt_subset(load.copy(), [lonmin,lonmax,latmin,latmax])
        soilm=pltdat.loc[rtexts[i],'soilm']
        soilm_up, soilm_bt=pltdat.loc[rtexts[i],'soilm_up'], pltdat.loc[rtexts[i],'soilm_bt']
        eco=pltdat.loc[rtexts[i],'eco']
        eco_up, eco_bt=pltdat.loc[rtexts[i],'eco_up'], pltdat.loc[rtexts[i],'eco_bt']
        plt_lines(ax, soilm,soilm_up,soilm_bt,eco,eco_up,eco_bt, yaxis_opt=yaxis_opt)
        #open here to compute spatially-averaged dryness index and tree dominance values
        #arid, tree=comp_meteo(load.copy(), [lonmin,lonmax,latmin,latmax])
        arid, tree=pltdat.loc[rtexts[i],'arid'], pltdat.loc[rtexts[i],'tree']
        
    #legend
    legend_elements=[Line2D([0],[0], linestyle='-', color="k", label='Soil Moist.'),
             Line2D([0],[0], marker=None, linestyle='-', color="g", label='LAI')]

    legend=ax.legend(handles=legend_elements, loc="upper right", prop={'size': 9},\
                    labelspacing=0,bbox_to_anchor=(1.75,.5), bbox_transform=ax.transAxes)
    legend.get_frame().set_alpha(0.3)


##### main ######################################
main()
#################################################

plt.show()
print ("End.")

