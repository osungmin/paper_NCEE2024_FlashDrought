#!/usr/bin/env python
import pandas as pd
import numpy as np

from scipy.interpolate import CubicSpline

import matplotlib as mpl
import matplotlib.pylab as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms
import matplotlib.colors as mcolors
from mpl_toolkits.axes_grid1 import make_axes_locatable
print ("modules imported")

def load_fd():
    warning="""
     ***
     this is to generate plot data for Fig. 3 using rawdata.csv (sample data)
     final plot data for the figure is provided under /_pltdats
     ***
    """
    print(warning)
    
    #load .csv file with extracted meteo/eco variables during flash drought events
    load = pd.read_csv("./rawdata.csv",
                        header=0, index_col=0,
                        na_values=-9999.)
    return(load.dropna(subset=['arid','tree','lai.modis0']))

def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = mcolors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

def custom_cmap(opt):

    if opt=='timing':
        cmap = truncate_colormap(plt.cm.YlOrRd_r, 0.0, .7)
    if opt=='intensity':
        colors01 = truncate_colormap(plt.cm.BrBG, 0., 0.4) #brown
        colors02 = truncate_colormap(plt.cm.BrBG, 0.5, 0.65) #green
        colors1 = colors01(np.linspace(0, 1, 320))
        colors2 = colors02(np.linspace(0, 1, 80))
        # combine them and build a new colormap
        colors = np.vstack((colors1, colors2))
        cmap = mcolors.LinearSegmentedColormap.from_list('my_colormap', colors)
    cmap.set_bad('gainsboro')
    cmap.set_under('gainsboro')
    return cmap

def create_imshow(df, targetvar=None, opt=None):

    xvar, yvar='arid', 'tree'
    xbins= [-.1, 0.5, 1, 2, 4]
    ybins=[0, 0.25, 0.5, 0.75, 1]
    thre= 100

    df_vals = pd.DataFrame(index=[str(x) for x in ybins[::-1]],
                           columns=[str(x) for x in xbins[:-1]])

    count=0
    for i in np.arange(0, len(xbins)-1, 1):
        df1 = df[(df[xvar]>= xbins[i])&(df[xvar]< xbins[i+1])].copy()
        if i==len(xbins)-2: df1 = df[(df[xvar]>= xbins[i])&(df[xvar]<= xbins[i+1])].copy()

        for j in np.arange(0, len(ybins)-1, 1):
            df2 = df1[(df1[yvar]>= ybins[j])&(df1[yvar]< ybins[j+1])].copy()
            if j==len(ybins)-2: df2=df1[(df1[yvar]>= ybins[j])&(df1[yvar]<= ybins[j+1])].copy()
            count+=len(df2)

            if len(df2) >= thre:
                imsi=df2[[targetvar+str(x) for x in np.arange(-6,20+1,1)]].copy()
                imsi_med=imsi.loc[:,targetvar+'0':targetvar+'18'].median(skipna=True)

                if opt=='timing':
                    cs = CubicSpline(np.arange(0,18+1,1), imsi_med.values)
                    cubic=cs(np.arange(0,18+1,0.1))

                    if sum(n < 0 for n in imsi_med.values) ==0: #no negative eco val
                        df_vals.loc[str(ybins[j]),str(xbins[i])] = -1
                    else:
                        df_vals.loc[str(ybins[j]),str(xbins[i])] = np.argmax(cubic<0)

                if opt=='intensity': df_vals.loc[str(ybins[j]),str(xbins[i])] = np.min(imsi_med)
                ##########

            else:
                df_vals.loc[str(ybins[j]),str(xbins[i])]= np.nan


    print(" - count:", count)
    df_vals.to_csv('./imshow'+opt+'.dat', na_rep=-9999)


def add_regime(ax):
    ax.text(0.6,4.135,"Humid", fontsize=8, color='dimgrey',
        bbox=dict(facecolor='w', edgecolor='None', boxstyle='round,pad=.1'))
    ax.text(2.7,4.135,"Arid", fontsize=8, color='dimgrey',
        bbox=dict(facecolor='w', edgecolor='None', boxstyle='round,pad=.1'))
    # the x coords of this transformation are axes, and the y coord are data
    trans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    line = mpatches.FancyArrowPatch((0, 4.15), (.5, 4.15),
                                    arrowstyle="|-|", color='dimgrey',
                                    transform=trans, zorder=-1)
    line.set_clip_on(False)
    ax.add_patch(line)
    line = mpatches.FancyArrowPatch((.505, 4.15), (1, 4.15),
                                    arrowstyle="|-|", color='dimgrey',
                                    transform=trans, zorder=-1)
    line.set_clip_on(False)
    ax.add_patch(line)

    ax.text(4.07,2.7,"Trees", fontsize=8, rotation=270, color='dimgrey',
        bbox=dict(facecolor='w', edgecolor='None', boxstyle='round,pad=.1'))
    ax.text(4.07,.25,"Short veg.", fontsize=8, rotation=270, color='dimgrey',
        bbox=dict(facecolor='w', edgecolor='None', boxstyle='round,pad=.1'))
    # the x coords of this transformation are axes, and the y coord are data
    trans = mtransforms.blended_transform_factory(ax.transAxes, ax.transData)
    line = mpatches.FancyArrowPatch((1.045, 4.1), (1.045, 2.1),
                                    arrowstyle="|-|", color='dimgrey',
                                    transform=trans, zorder=-1)
    line.set_clip_on(False)
    ax.add_patch(line)
    line = mpatches.FancyArrowPatch((1.045, 2.1), (1.045, -.1),
                                    arrowstyle="|-|", color='dimgrey',
                                    transform=trans, zorder=-1)
    line.set_clip_on(False)
    ax.add_patch(line)


##### main ######################################
#load=load_fd()
#################################################

### prepare figure setting
fig= plt.figure(figsize=(6, 2.5), facecolor='w', edgecolor='k')
gs = gridspec.GridSpec(1, 2, width_ratios=[1,1],
                       left=0.1, bottom=0.05, top=.95, right=0.9,
                       wspace=0.3)

#### imshow for timing and Intensity
for i in range(2):
    print(" \n plotting", i)
    ax = fig.add_subplot(gs[i])
    ax.set_aspect(1)
    add_regime(ax)

    if i==0:
        opt='timing'
        vmin, vmax= 0, 8
    if i==1:
        opt='intensity'
        vmin, vmax= -.8, .2

    ### prepare plot data
    #open here to create plot data
    #create_imshow(load, targetvar='lai.modis', opt=opt)

    ### load plot data
    plot=pd.read_csv('./imshow_'+opt+'.dat',
                    header=0, index_col=0, na_values=-9999)
    plot=plot.iloc[1:,:]
    if i==0: plot=plot/10

    ### plotting
    im=plt.imshow(plot, cmap=custom_cmap(opt), vmin=vmin, vmax=vmax,
                  interpolation='none', extent=[0,4,0,4])

    plt.xticks(np.arange(0,4+1,1), ["0","0.5","1","2","4"], fontsize=8)
    plt.xlabel('DryIdx [-]', fontsize=9)
    if i==0:
        plt.ylabel('Tree dominance [-]', fontsize=9)
        plt.yticks(np.arange(0,4+1,1), ["0",".25",".50",".75","1"], fontsize=8)
    else: plt.yticks(np.arange(0,4+1,1), [""]*5, fontsize=8)
    plt.xlim(0,4)
    plt.ylim(0,4)

    if i==0:
        ax.text(-.5, 4.5, "a)", fontsize=10, weight='bold')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.3)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.tick_params(labelsize=8, length=2)
        cbar.set_ticks([0,2,4,6,8])
        cbar.set_label("Timing", fontsize=8, labelpad=2)

    if i==1:
        ax.text(-.5, 4.5, "b)", fontsize=10, weight='bold')
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.3)
        cbar = plt.colorbar(im, cax=cax)
        cbar.ax.tick_params(labelsize=8, length=2)
        cbar.set_ticks(np.arange(-.8,.21,.2))
        cbar.set_label("Intensity", fontsize=8, labelpad=2)


plt.show()
print("End.")

