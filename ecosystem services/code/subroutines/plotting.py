# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 19:57:57 2020

File used for plot methods to produce various figures used in the overall analysis

@author: aargl
"""

### Imports
from matplotlib import pyplot as plt
from matplotlib import gridspec 
from matplotlib.patches import Patch
import matplotlib.colors as colors
import geopandas as gpd
import datetime


### Local Imports
from .plotting_secondary import *


def fig_1(geo_file,os_file,mob_temporal_file,save_dir):
    """
    Code used to plot figure 1 in the analysis, this figure illustrates the 
    geographic data.

    Parameters
    ----------
    geo_file: str
        The geo_file defineing regions.
    os_file : str
        The os geographic file necessary to draw os data overlay.
    
    save_dir : str
        The save directory for the figure.

    Plots and Saves
    -------
    Figure 1. fig_1.png

    """
    ### Load Data
    # Get Geographic Data
    gdf1 = gpd.read_file(geo_file)
    gdf2 = gpd.read_file(os_file)
    norm = colors.Normalize(vmin=gdf1['Mobility P'].min(), vmax=gdf1['Mobility P'].max())
    cbar = plt.cm.ScalarMappable(norm=norm, cmap='RdBu_r')
    mob_df = pd.read_csv(mob_temporal_file)
    
    ### Make Figure
    fig = plt.figure(figsize=(14,10))
    gs = gridspec.GridSpec(1,2,width_ratios=[1,1],height_ratios=[1.0],wspace=0.0,hspace=0.0)
    ax = fig.add_subplot(gs[0,0])
    gdf1[gdf1['Urbanisati']=='Urban'].plot(ax=ax,facecolor=[1,0,0,0.025],edgecolor='red',linewidth=0.25,label='Urban',zorder=1)
    gdf1[gdf1['Urbanisati']=='Rural'].plot(ax=ax,facecolor=[0,0,1,0.025],edgecolor='blue',linewidth=0.25,label='Rural',zorder=1)
    gdf2.plot(color='black',ax=ax,label='OS Greenspaces',linewidth=2.0,zorder=2)
    legend_elements = [Patch(facecolor=[1,0,0,0.025], edgecolor='red',linewidth=0.25,label='Urban'),Patch(facecolor=[0,0,1,0.025], edgecolor='blue',linewidth=0.25,label='Rural'),Patch(facecolor='black', edgecolor='black',linewidth=2,label='OS Greenspaces')] 
    ax.legend(handles=legend_elements,loc='upper left',framealpha=0)
    ax.set_xlim(0,675000)
    ax.set_ylim(0,1250000)
    ax.set_title('(a) Regions with Greenspace')
    ax.set_yticks([])
    ax.set_xticks([])

    
    ax = fig.add_subplot(gs[0,1])
    gdf1.plot(cmap='RdBu_r',column='Mobility P',ax=ax,legend=False)
    ax.set_xlim(0,675000)
    ax.set_ylim(0,1250000)
    ax.set_title('(b) Average Park Mob After LD')
    ax_cbar = fig.colorbar(cbar, ax=ax)
    ax_cbar.set_label('Google Park Mobility (% relative to Jan-Feb median)')
    ax.set_yticks([])
    ax.set_xticks([])
    figfile = save_dir + '/fig_1.png'
    plt.savefig(figfile,dpi=500)
    
    
    
    return
    
def fig_2(greenspace_metrics_gs_dist_added_file,save_dir):
    """

    Parameters
    ----------
    greenspace_metrics_gs_dist_added_file : str
        File used to produce figure 2.    
    save_dir : str
        The save directory for the figure.

    Returns
    -------
    Various Figures

    """
    # Read in data        
    data = pd.read_excel(greenspace_metrics_gs_dist_added_file)
    
    # Extract various metrics from data
    region_type = data.iloc[:,3]
    region_area = data.iloc[:,5]
    
    deaths = data.iloc[:,6]
    deaths = pd.to_numeric(deaths, errors='coerce')
    
    giph = data.iloc[:,7]
    
    mob_retail_rec_rate = data.iloc[:,9]
    mob_park_rate = data.iloc[:,11]
    
    gs_num = data.iloc[:,20]
    gs_area = data.iloc[:,21]
    gs_avg_area = data.iloc[:,22]
    gs_frac = data.iloc[:,23]
    gs_dist = data.iloc[:,72]
    
    gs_non_sport_num = data.iloc[:,24]
    gs_non_sport_area = data.iloc[:,25]
    gs_non_sport_avg_area = data.iloc[:,26]
    gs_non_sport_frac = data.iloc[:,27]
    
    gs_sport_num = data.iloc[:,28]
    gs_sport_area = data.iloc[:,29]
    gs_sport_avg_area = data.iloc[:,30]
    gs_sport_frac = data.iloc[:,31]
    
    # Run plotting functions
    
    gs_metric_scatter_plots(region_area,gs_num,gs_area,gs_avg_area,gs_frac,gs_dist, 'All','Region area (ha)',save_dir)
    gs_metric_scatter_plots(mob_park_rate,gs_num,gs_area,gs_avg_area,gs_frac,gs_dist, 'All','Rate of park mobility \n post lockdown',save_dir)
    # gs_metric_scatter_plots(mob_park_rate,gs_sport_num,gs_sport_area,gs_sport_avg_area,gs_sport_frac,[], 'Sport','Rate of park mobility \n post lockdown')
    # gs_metric_scatter_plots(mob_park_rate,gs_non_sport_num,gs_non_sport_area,gs_non_sport_avg_area,gs_non_sport_frac,[], 'Non-sport','Rate of park mobility \n post lockdown')
    
    gs_metric_scatter_plots(giph,gs_num,gs_area,gs_avg_area,gs_frac,gs_dist, 'All','Gross income per head',save_dir)
    # gs_metric_scatter_plots(giph,gs_sport_num,gs_sport_area,gs_sport_avg_area,gs_sport_frac,[], 'Sport','Gross income per head')
    # gs_metric_scatter_plots(giph,gs_non_sport_num,gs_non_sport_area,gs_non_sport_avg_area,gs_non_sport_frac,[], 'Non-sport','Gross income per head')      
    
    gs_metric_scatter_plots(deaths,gs_num,gs_area,gs_avg_area,gs_frac,gs_dist, 'All','COVID-19 Death Rate April-May \n (per 100,000)',save_dir)
    # gs_metric_scatter_plots(deaths,gs_sport_num,gs_sport_area,gs_sport_avg_area,gs_sport_frac,[], 'Sport','COVID-19 Death Rate April-May \n (per 100,000)')
    # gs_metric_scatter_plots(deaths,gs_non_sport_num,gs_non_sport_area,gs_non_sport_avg_area,gs_non_sport_frac,[], 'Non-sport','COVID-19 Death Rate April-May \n (per 100,000)')     
    
    
    gs_allmetrics_scatter_plots(mob_park_rate,giph,deaths,gs_num,gs_area,gs_frac,region_type,save_dir)
    gs_allmetrics_scatter_plots(mob_park_rate[region_type=='Urban'],giph[region_type=='Urban'],deaths[region_type=='Urban'],gs_num[region_type=='Urban'],gs_area[region_type=='Urban'],gs_frac[region_type=='Urban'],region_type,save_dir)
    gs_allmetrics_scatter_plots(mob_park_rate[region_type=='Rural'],giph[region_type=='Rural'],deaths[region_type=='Rural'],gs_num[region_type=='Rural'],gs_area[region_type=='Rural'],gs_frac[region_type=='Rural'],region_type,save_dir)
    
    # covid_deaths_wealth_scatter_plot(deaths,giph,region_type)
    # covid_deaths_wealth_scatter_plot(deaths[region_type=='Urban'],giph[region_type=='Urban'],region_type)
    # covid_deaths_wealth_scatter_plot(deaths[region_type=='Rural'],giph[region_type=='Rural'],region_type)
        
    return