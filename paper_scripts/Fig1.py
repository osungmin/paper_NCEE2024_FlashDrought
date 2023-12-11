#!/usr/bin/env python
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from mpl_toolkits.basemap import Basemap

import warnings
warnings.filterwarnings("ignore")
print ("modules imported")

def load_fd():
    #load .csv file with extracted meteo/eco variables during flash drought events
    #each raw corresponds each flash drought event
    flash = pd.read_csv("./example_fd.csv",
                        header=0, index_col=0,
                        na_values=-9999.)
    flash['grid']=flash['p'].astype('str')+'_'+flash['q'].astype(str)
    print(flash[['dr_st_yr','arid','tree']].describe())
    return(flash)

def generateMapData(df):
    #to generate the 2D global map from the .csv file
    out = np.empty((720,1440)) #y, x size
    out[:,:]= np.nan
    print(" - working df size:", df.shape, "=>", out.shape)

    count=0
    for i in range(len(df)):
        if i%50000==0: print(" ...", i)

        imsi = df.iloc[i,:].copy()
        p, q = imsi['p'], imsi['q']
        if out[p, q]==out[p, q]: out[p, q]+=1
        else: out[p, q]=1 #np.nan at the first place
        count+=1

    outfpath='./map_freq.dat'
    np.save(open(outfpath, 'wb'), out, allow_pickle=False)
    print(" >> saved:", outfpath)

def generateMapData2(df):
    #to create the inset plot (imshow) for the 16 climate-veg regimes (0 to 15)
    #increase along the y-axis, e.g., 0=most humid and no tree 1=most humid and tree 0.25, so on

    df=df.drop_duplicates(subset=['p','q'], keep="last")
    df['dum']=np.nan #later to make a map
    df=df[['p','q','arid','tree','dum']].copy()

    out = np.empty((720,1440)) #y, x size
    out[:]= np.nan

    print(" - only unique grid pixels selected", df.shape)
    print(" - data into array out shape:", out.shape)

    arids= [0, 0.5, 1, 2, 9999]
    trees= [0, .25, .5, .75, 1]

    df_vals = pd.DataFrame(index=[str(x) for x in trees[:-1]][::-1], columns=[str(x) for x in arids[:-1]])

    val=0
    check=0
    thre=100

    for i in np.arange(0, len(arids)-1, 1):
        for j in np.arange(0, len(trees)-1, 1):
             df['dum'][(df['arid']>=arids[i])&(df['arid']<arids[i+1])&(df['tree']>=trees[j])&(df['tree']<trees[j+1])] = val
             sub_df=df[df['dum']==val].copy()
             check+= len(sub_df)

             if len(sub_df) >= thre:
                 df_vals.loc[str(trees[j]),str(arids[i])] = val
                 val+=1 #assing integer values from +=1
             else:
                 df_vals.loc[str(trees[j]),str(arids[i])] = -1 # to add color later
                 #will remove the grid pixel also from the map
                 df['dum'][(df['arid']>=arids[i])&(df['arid']<arids[i+1])&(df['tree']>=trees[j])&(df['tree']<trees[j+1])] = np.nan

    print(" - data values replaced", check, "df len", len(df))
    df_vals.to_csv("./map.imshow.arid_tree.dat")

    ##### to make a global map with the climate-veg regime info
    print("\n >> assign arid-tree value to each grid pixel")
    p_lats, q_lons= df["p"].values, df["q"].values

    i=0
    for p,q in zip(p_lats, q_lons):
        if i%10000==0: print ('...', i, "out of", len(df))
        imsi = df[(df["p"]==p) & (df["q"]==q)]
        if len(imsi)!=1: stop
        out[p, q]= imsi['dum'].values[0]

        i+=1

    print(".... saving")
    outfpath='./map.arid_tree.dat'
    np.save(open(outfpath, 'wb'), out, allow_pickle=False)
    print(" >> saved:", outfpath)

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

def plt_map(ax, pltdat):

    m=plt_basemap(ax)

    lons, lats = np.arange(-179.875, 180.1, 0.25), np.arange(89.875, -90., -0.25)
    if pltdat.shape[0]!=len(lats):stop
    if pltdat.shape[1]!=len(lons):stop

    lon, lat = np.meshgrid(lons,lats)
    xi, yi = m(lon, lat)

    boundaries = np.arange(3, 18+1, 3)
    cmap = mpl.colors.ListedColormap(["cornflowerblue","lightsteelblue","gold","darkorange","red"])
    cmap.set_over("darkred")
    cmap.set_under("royalblue")

    cs = m.pcolormesh(xi,yi,pltdat, cmap=cmap,
                      norm = mpl.colors.BoundaryNorm(boundaries, ncolors=cmap.N))

    plt.text(-180, 105, 'a)', weight='bold', fontsize=10)
    #plt.title("Frequency of flash drought (2001-2020)", pad=12, fontsize=9)

    cax = inset_axes(ax, "100%", "100%", loc="lower left",
                     bbox_to_anchor=(0.,0.05,.25,.07), bbox_transform=ax.transAxes)

    cbar = plt.colorbar(cs, cax=cax, extend='both', orientation='horizontal')
    cbar.ax.tick_params(labelsize=7, length=2, size=0)

    cax.xaxis.set_label_position('top')
    plt.xlabel("Frequency", fontsize=8, labelpad=3)
    return(m)

def plt_map_regime(ax, pltdat, inset_pltdat):
    col_dict={-1:"lightgrey",
              0:"#ffff66",
              1:"#26d701",
              2:"#68991c",
              3:"#233309",
              4:"#ffcc00",
              5:"#78ec6c",
              6:"#8acc26",
              7:"#344d0e",
              8:"#ff9900",
              9:"#a9f36a",
              10:"yellowgreen",
              11:"#456613",
              12:"#ff0000",
              13:"#ddf969",
              14:"#9ce62a",
              15:"darkred"} #4
    cm = ListedColormap([col_dict[x] for x in col_dict.keys()])

    m=plt_basemap(ax)

    lons, lats = np.arange(-179.875, 180, 0.25), np.arange(89.975, -90, -0.25)
    lon, lat = np.meshgrid(lons,lats)
    xi, yi = m(lon, lat)
    cs = m.pcolormesh(xi, yi, pltdat, vmin=-1, vmax=15, cmap=cm)

    plt.text(-180, 105, 'b)', weight='bold', fontsize=10)
    
    ax2 = inset_axes(ax, "100%", "100%", loc="lower left",
                     bbox_to_anchor=(-.02,0.12,.28,.28), bbox_transform=ax.transAxes)

    im=plt.imshow(inset_pltdat, cmap=cm, interpolation='none', vmin=-1, vmax=15,
                  extent=[0,4,0,4])

    plt.xlabel("Aridity", fontsize=8, labelpad=2)
    plt.xticks(range(5),["0","0.5","1","2","4"], fontsize=7)
    plt.ylabel("Tree dominance", fontsize=8, labelpad=1)
    plt.yticks(range(5),["0",".25",".50",".75","1"], fontsize=7)
    ax2.tick_params(axis='both', which='major', pad=1)

def main():
    ### prepare figure setting
    fig= plt.figure(figsize=(6, 6), facecolor='w', edgecolor='k')
    gs = gridspec.GridSpec(2, 1, height_ratios=[1,1],
                           left=0.1, right=0.95,
                           top=0.95, bottom=0.05,
                           hspace=0.1)

    ### upper map: frequency
    print("\n >> plotting the freq map (upper)")
    ax = fig.add_subplot(gs[0])

    fpath='../map_freq.dat'
    with open(fpath, 'rb') as f:
        pltdat = np.load(f)[:,:]

    plt_map(ax, pltdat)

    ### bottom map: regime
    print(" \n >> plotting the regime map (bottom)")
    ax = fig.add_subplot(gs[1])

    fpath='./map.arid_tree.dat'
    with open(fpath, 'rb') as f:
        pltdat = np.load(f)[:,:]
    
    inset_pltdat =pd.read_csv("./map.imshow.arid_tree.dat",
                               header=0, index_col=0, na_values=-9999)
    plt_map_regime(ax, pltdat, inset_pltdat)


##### generating map data #########################
generateMapData(load_fd())
generateMapData2(load_fd())
#################################################

main()
plt.show()
print ("End.")
