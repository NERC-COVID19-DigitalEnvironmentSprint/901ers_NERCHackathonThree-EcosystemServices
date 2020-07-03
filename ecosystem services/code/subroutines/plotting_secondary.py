# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 22:10:49 2020

File containing plotting functions for fig 2 in plotting.py

@author: aargl
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from scipy import stats

def gs_metric_scatter_plots(metric,gs_num,gs_area,gs_avg_area,gs_frac,gs_dist,xlab,ylab,save_dir):   
    
    """
    Produces 2x2 scatter plots of all greenspace metrics against metric of interest,
    (plots metric against greenspace distance in separate figure, this is only
    available for all greenspaces)
    
    Inputs:
        
        - metric, choose metric to compare against greenspace metrics 
        
        - Greenspace metrics:
            - gs_num, Number of greenspaces
            - gs_area, Area of all greenspaces (ha)
            - gs_avg_area, Average area of a greenspace (ha)
            - gs_frac, Fraction of land area that are greenspaces
            - gs_dist, Distance to nearest greenspace (m)
            
        - xlab, String for part of x-axis to indicate if it is 'All', 'Sport'
          or 'Non-sport' greenspaces
        
        - ylab, String for y-axis reflecting metric used
    
    """
    
    gs_num_rem = gs_num[~np.isnan(metric)]
    gs_area_rem = gs_area[~np.isnan(metric)]
    gs_avg_area_rem = gs_avg_area[~np.isnan(metric)]
    gs_frac_rem = gs_frac[~np.isnan(metric)]
    
    metric_rem = metric[~np.isnan(metric)]
  
    
    fig, axs = plt.subplots(2,2,figsize=(9,5.5))
    
    axs[0,0].scatter(gs_area, metric)
    m, b = np.polyfit(gs_area_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_area_rem, metric_rem)
    axs[0,0].plot(gs_area, m*gs_area+b, 'tab:orange')
    axs[0,0].set_xlabel(xlab+': Area of greenspaces (ha)')
    axs[0,0].set_ylabel(ylab)
    axs[0,0].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    # fig.tight_layout()
        
    axs[0,1].scatter(gs_num, metric)
    m, b = np.polyfit(gs_num_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_num_rem, metric_rem)
    axs[0,1].plot(gs_num, m*gs_num+b, 'tab:orange')
    axs[0,1].set_xlabel(xlab+': Number of greenspaces')
    axs[0,1].set_ylabel(ylab)
    axs[0,1].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    # fig.tight_layout()
    
    # fig = plt.figure()
    axs[1,0].scatter(gs_avg_area, metric)
    m, b = np.polyfit(gs_avg_area_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_avg_area_rem, metric_rem)
    axs[1,0].plot(gs_avg_area, m*gs_avg_area+b, 'tab:orange')
    axs[1,0].set_xlabel(xlab+': Avg. area of greenspace (ha)')
    axs[1,0].set_ylabel(ylab)
    axs[1,0].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    # fig.tight_layout()
    
    # fig = plt.figure()
    axs[1,1].scatter(gs_frac, metric)
    m, b = np.polyfit(gs_frac_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_frac_rem, metric_rem)
    axs[1,1].plot(gs_frac, m*gs_frac+b, 'tab:orange')
    axs[1,1].set_xlabel(xlab+': Fraction of greenspace')
    axs[1,1].set_ylabel(ylab)
    axs[1,1].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    fig.tight_layout()
    
    if len(gs_dist) > 0:
        
        gs_dist_rem = gs_dist[~np.isnan(metric)]    
        gs_dist_rem2 = gs_dist_rem[~np.isnan(gs_dist_rem)]
        metric_rem2 = metric_rem[~np.isnan(gs_dist_rem)]
        
        fig = plt.figure()
        plt.scatter(gs_dist, metric)
        m, b = np.polyfit(gs_dist_rem2, metric_rem2, 1)
        r,p = stats.pearsonr(gs_dist_rem2, metric_rem2)
        plt.plot(gs_dist, m*gs_dist+b, 'tab:orange')
        plt.xlabel(xlab+': Avg. distance to nearest greenspace (m)')
        plt.ylabel(ylab)
        plt.title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
        fig.tight_layout()
        
    figname = save_dir + '/gs_metric_scatter_plots.png'
    plt.savefig(figname,dpi=500)
        
    return
        


def gs_allmetrics_scatter_plots(mob_park_rate,giph,deaths,gs_num,gs_area,gs_frac,region_type,save_dir): 
    
    """
    Produces 3x3 scatter plots of 3 greenspace metrics against park mobility rate
    post lockdown (row 1), gross income per head (row 2), COVID-19 death rate (row 3).
    Separates rural (blue) from urban (red) by colour
    
    Inputs:
        
        - mob_park_rate, Park mobility rate of increase post lockdown 
        
        - giph, Gross income per head
        
        - deaths, COVID-19 death rate per 100,000 for April and May
        
        - Greenspace metrics:
            - gs_num, Number of greenspaces
            - gs_area, Area of all greenspaces (ha)
            - gs_frac, Fraction of land area that are greenspaces
            
        - region_type, Specifies whether region is rural or urban
    
    """
    
    xlab = 'All'  
    fig, axs = plt.subplots(3,3,figsize=(16,7.65))
    
      
    ylab = 'Rate of park mobility \n post lockdown'
    
    gs_num_rem = gs_num[~np.isnan(mob_park_rate)]
    gs_area_rem = gs_area[~np.isnan(mob_park_rate)]
    gs_frac_rem = gs_frac[~np.isnan(mob_park_rate)]
    metric_rem = mob_park_rate[~np.isnan(mob_park_rate)]
    
    metric = mob_park_rate.copy()
    
    axs[0,0].scatter(gs_area[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[0,0].scatter(gs_area[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_area_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_area_rem, metric_rem)
    axs[0,0].plot(gs_area, m*gs_area+b, 'tab:orange')
    axs[0,0].set_xlabel(xlab+': Area of greenspaces (ha)')
    axs[0,0].set_ylabel(ylab)
    axs[0,0].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
        
    axs[0,1].scatter(gs_num[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[0,1].scatter(gs_num[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_num_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_num_rem, metric_rem)
    axs[0,1].plot(gs_num, m*gs_num+b, 'tab:orange')
    axs[0,1].set_xlabel(xlab+': Number of greenspaces')
    axs[0,1].set_ylabel(ylab)
    axs[0,1].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    axs[0,2].scatter(gs_frac[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[0,2].scatter(gs_frac[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_frac_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_frac_rem, metric_rem)
    axs[0,2].plot(gs_frac, m*gs_frac+b, 'tab:orange')
    axs[0,2].set_xlabel(xlab+': Fraction of greenspace')
    axs[0,2].set_ylabel(ylab)
    axs[0,2].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    
    ylab = 'Gross income per head'
    
    gs_num_rem = gs_num[~np.isnan(giph)]
    gs_area_rem = gs_area[~np.isnan(giph)]
    gs_frac_rem = gs_frac[~np.isnan(giph)]
    metric_rem = giph[~np.isnan(giph)]
    
    metric = giph.copy()
    
    axs[1,0].scatter(gs_area[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[1,0].scatter(gs_area[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_area_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_area_rem, metric_rem)
    axs[1,0].plot(gs_area, m*gs_area+b, 'tab:orange')
    axs[1,0].set_xlabel(xlab+': Area of greenspaces (ha)')
    axs[1,0].set_ylabel(ylab)
    axs[1,0].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
        
    axs[1,1].scatter(gs_num[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[1,1].scatter(gs_num[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_num_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_num_rem, metric_rem)
    axs[1,1].plot(gs_num, m*gs_num+b, 'tab:orange')
    axs[1,1].set_xlabel(xlab+': Number of greenspaces')
    axs[1,1].set_ylabel(ylab)
    axs[1,1].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    axs[1,2].scatter(gs_frac[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[1,2].scatter(gs_frac[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_frac_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_frac_rem, metric_rem)
    axs[1,2].plot(gs_frac, m*gs_frac+b, 'tab:orange')
    axs[1,2].set_xlabel(xlab+': Fraction of greenspace')
    axs[1,2].set_ylabel(ylab)
    axs[1,2].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    
    ylab = 'COVID-19 Death Rate \n April-May (per 100,000)'
    
    gs_num_rem = gs_num[~np.isnan(deaths)]
    gs_area_rem = gs_area[~np.isnan(deaths)]
    gs_frac_rem = gs_frac[~np.isnan(deaths)]
    metric_rem = deaths[~np.isnan(deaths)]
    
    metric = deaths.copy()
    
    axs[2,0].scatter(gs_area[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[2,0].scatter(gs_area[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_area_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_area_rem, metric_rem)
    axs[2,0].plot(gs_area, m*gs_area+b, 'tab:orange')
    axs[2,0].set_xlabel(xlab+': Area of greenspaces (ha)')
    axs[2,0].set_ylabel(ylab)
    axs[2,0].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
        
    axs[2,1].scatter(gs_num[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[2,1].scatter(gs_num[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_num_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_num_rem, metric_rem)
    axs[2,1].plot(gs_num, m*gs_num+b, 'tab:orange')
    axs[2,1].set_xlabel(xlab+': Number of greenspaces')
    axs[2,1].set_ylabel(ylab)
    axs[2,1].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    axs[2,2].scatter(gs_frac[region_type=='Rural'], metric[region_type=='Rural'],c='tab:blue')
    axs[2,2].scatter(gs_frac[region_type=='Urban'], metric[region_type=='Urban'],c='tab:red')
    m, b = np.polyfit(gs_frac_rem, metric_rem, 1)
    r,p = stats.pearsonr(gs_frac_rem, metric_rem)
    axs[2,2].plot(gs_frac, m*gs_frac+b, 'tab:orange')
    axs[2,2].set_xlabel(xlab+': Fraction of greenspace')
    axs[2,2].set_ylabel(ylab)
    axs[2,2].set_title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    fig.tight_layout()
    figname = save_dir + '/fig2.png'
    plt.savefig(figname,dpi=500)
    
    return

def covid_deaths_wealth_scatter_plot(deaths,giph,region_type,save_dir):
    
    """
    Produces scatter plot of gross income per head against COVID-19 death rate,
    separates rural from urban by colour
    
    Inputs:
        
        - deaths, COVID-19 death rate per 100,000 for April and May 
        
        - giph, Gross income per head
            
        - region_type, Specifies whether region is rural or urban
    
    """
    
    fig = plt.figure()
    
    giph_rem = giph[~np.isnan(giph)]
    deaths_rem = deaths[~np.isnan(giph)]
    giph_rem2 = giph_rem[~np.isnan(deaths_rem)]
    deaths_rem2 = deaths_rem[~np.isnan(deaths_rem)]
     
    plt.scatter(deaths[region_type=='Rural'], giph[region_type=='Rural'],c='tab:blue',label='Rural')
    plt.scatter(deaths[region_type=='Urban'], giph[region_type=='Urban'],c='tab:red',label='Urban')
    m, b = np.polyfit(deaths_rem2, giph_rem2, 1)
    r,p = stats.pearsonr(deaths_rem2, giph_rem2)
    plt.plot(deaths, m*deaths+b, 'tab:orange')
    plt.xlabel('COVID-19 Death Rate April-May (per 100,000)')
    plt.ylabel('Gross income per head')
    plt.title('Correlation: '+f'{r:.4f}'+', Significance: '+f'{p:.4f}')
    
    plt.legend()
    fig.tight_layout()
    figname = save_dir + '/covid_deaths_wealth_scatter_plot.png'
    plt.savefig(figname,dpi=500)
    
    return