# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 17:08:01 2020

Python File used to store "secondary" definitions for frequent use in more 
significant definitions from other scripts.

@author: aargl
"""

### Imports
import geopandas as gpd
import pandas as pd
import numpy as np
import os
import datetime
from difflib import SequenceMatcher
import re 
from shapely.geometry import Polygon, MultiPolygon, shape, Point

### Definitions

def similar(a, b):
    """
    Similarity between the strings (identical=1, unique=0)
    
    Parameters
    ----------
    a : str
        A string.
    b : str
        Another string.

    Returns
    -------
    float
    

    """
    return SequenceMatcher(None, a, b).ratio()

def similar_string(string1,string2):
    """
    Seperates by sentence into individual words and determines the mean highest
    similarities scores relative to words in the other string - therby order 
    does not matter.

    Parameters
    ----------
    string1 : str
        A string.
    string2 : str
        Another string.

    Returns
    -------
    score : float
        "Best" mean score of similarity of words in strings1 and strings2.

    """
    # Get uniformity among strings and split on spaces
    strings_1 = string1.lower()
    strings_1 = re.split(' ',strings_1)
    strings_2 = string2.lower()
    strings_2 = re.split(' ',strings_2)
    
    # Go through strings_1 and compute the mean similarity score against strings_2
    str_mean_1 = 0
    N = len(strings_1)
    
    for str1 in strings_1:
        
        best_sim = 0
        
        for str2 in strings_2:
            
            sim = similar(str1,str2)
                        
            if sim > best_sim:
                
                best_sim = sim
                            
        str_mean_1 = str_mean_1 + best_sim/N  
    
    # Go through strings_2 and compute the mean similarity score against strings_1
    str_mean_2 = 0
    N = len(strings_2)
    
    for str2 in strings_2:
        
        best_sim = 0
        
        for str1 in strings_1:
            
            sim = similar(str2,str1)
            
            if sim > best_sim:
                
                best_sim = sim
                
        str_mean_2 = str_mean_2 + best_sim/N
        
    # Our score is the mid point of the similarity means.
    score = 0.5 * (str_mean_1 + str_mean_2)
    
    return score



# convert_3D_2D is used to flatten 3 dimensional polygons into their 2D coordinate system
# from (accessed: 03/07/2020): https://gist.github.com/rmania/8c88377a5c902dfbc134795a7af538d8
def convert_3D_2D(geometry):
    '''
    Takes a GeoSeries of 3D Multi/Polygons (has_z) and returns a list of 2D Multi/Polygons
    '''
    new_geo = []
    for p in geometry:
        if p.has_z:
            if p.geom_type == 'Polygon':
                lines = [xy[:2] for xy in list(p.exterior.coords)]
                new_p = Polygon(lines)
                new_geo.append(new_p)
            elif p.geom_type == 'MultiPolygon':
                new_multi_p = []
                for ap in p:
                    lines = [xy[:2] for xy in list(ap.exterior.coords)]
                    new_p = Polygon(lines)
                    new_multi_p.append(new_p)
                new_geo.append(MultiPolygon(new_multi_p))
    return new_geo


### Classes
    
class region():
    
    
    def __init__(self,name,iso_code):
        """
        Region class is used to store important data 
    
        Parameters
        ----------
        name : str
            The name of the region.
        string2 : str
            The Iternational Standardisation Organisation (ISO) geographic code.
    
        Returns
        -------
        self : region
            Initialises a region class.
        
        """
        
        self.name = name
        self.iso_code = iso_code
        
        return
        
    def add_mobility(self,dates,mob_retail_rec,mob_park,mob_groc,mob_transit,mob_work,mob_resident):
        """
        Add google mobility data into region during the 2020 COVID-19 pandemic.
        
        Parameters
        ----------
        dates : datetime
            The dates of the pandemic.
        mob_retail_rec : numpy array float
            Daily Mobility Retail & Recreation (% from baseline).
        mob_park : numpy array float
            Daily Mobility Park (% from baseline).
        mob_park : numpy array float
            Daily Mobility Grocery & Pharmacy (% from baseline).
        mob_transit : numpy array float
            Daily Mobility Transit Stations (% from baseline).
        mob_work : numpy array float
            Daily Mobility Workplace (% from baseline).
        mob_resident : numpy array float
            Daily Mobility Residential (% from baseline).
    
        Declare  
        -------
        mob_retail_rec_avg : float
            Mobility Retail & Recreation Average Post Lockdown (% from baseline)
        mob_retail_rec_dod : float    
            Mobility Retail & Recreation Rate of Change Post Lockdown (% from baseline per day)
        mob_park_avg : float
            Mobility Parks Average Post lockdown (% from baseline)
        mob_park_dod : float
            Mobility Park Rate of Change Post lockdown  (% from baseline per day)
        mob_groc_avg : float
            Mobility Grocery & Pharmacy Average Post Lockdown (% from baseline)
        mob_groc_dod : float 
            Mobility Grocery & Pharmacy Rate of Change Post Lockdown (% from baseline per day)
        mob_transit_avg : float
            Mobility Transit Stations Average Post lockdown (% from baseline)
        mob_transit_dod : float
            Mobility Transit Station Rate of Change Post lockdown  (% from baseline per day)
        mob_work_avg : float
            Mobility Workplaces Average Post lockdown (% from baseline)
        mob_work_dod : float
            Mobility Workplaces Rate of Change Post lockdown  (% from baseline per day)
        mob_resident_avg : float
            Mobility Residential Average Post Lockdown (% from Baseline)
        mob_resident_dod : float
            Mobility Residential Rate of Change Post Lockdown (% from Baseline)
        
        """
        # define new class members 
        self.dates_mob = dates
        self.mob_retail_rec = mob_retail_rec
        self.mob_park = mob_park
        self.mob_groc = mob_groc
        self.mob_transit = mob_transit
        self.mob_work = mob_work
        self.mob_resident = mob_resident
        
        # date at which the UK locked down, elms are the boolean elements of 
        # dates greater or equal to the lockdown date.
        uk_lockdown_date = datetime.datetime(2020,3,23)
        elms = dates >= uk_lockdown_date
    
        # Our "day" numeric vector, days since lockdown - used to perform linear regression
        x = np.linspace(0,len(elms)-1,len(elms))
        
        # ignore nan values subset
        elms_subset = (self.mob_retail_rec == self.mob_retail_rec)*elms 
        
        # check if we have at least one non-value for time-series + mobility data
        if len(elms_subset[elms_subset]) > 0:
            
            # We estimate the average rate of change by fitting a linear gradient
            self.mob_retail_rec_dod, _ = np.polyfit(x[elms_subset],self.mob_retail_rec[elms_subset],1) 
            # Find average mobility post lockdown
            self.mob_retail_rec_avg = np.mean(self.mob_retail_rec[elms_subset])
            
        else:
            
            # Otherwise if data has no points make outputs nan values
            self.mob_retail_rec_dod = np.nan    
            self.mob_retail_rec_avg = np.nan
        
        # rince and repeat for different declearation 
        elms_subset = (self.mob_park == self.mob_park)*elms  
        if len(elms_subset[elms_subset]) > 0:
            
            self.mob_park_dod, _ = np.polyfit(x[elms_subset],self.mob_park[elms_subset],1) 
            self.mob_park_avg = np.mean(self.mob_park[elms_subset])
            
        else:
            
            self.mob_park_dod = np.nan    
            self.mob_park_avg = np.nan
            
        elms_subset = (self.mob_groc == self.mob_groc)*elms  
        if len(elms_subset[elms_subset]) > 0:            
            
            self.mob_groc_dod, _ = np.polyfit(x[elms_subset],self.mob_groc[elms_subset],1)     
            self.mob_groc_avg = np.mean(self.mob_groc[elms_subset])
        
        else:
            
            self.mob_groc_dod = np.nan    
            self.mob_groc_avg = np.nan
            
        elms_subset = (self.mob_transit == self.mob_transit)*elms  
        
        if len(elms_subset[elms_subset])> 0:
            
            self.mob_transit_dod, _ = np.polyfit(x[elms_subset],self.mob_transit[elms_subset],1)
            self.mob_transit_avg = np.mean(self.mob_transit[elms_subset])
            
        else:
            
            self.mob_transit_dod = np.nan    
            self.mob_transit_avg = np.nan
            
        elms_subset = (self.mob_work == self.mob_work)*elms  
        
        if len(elms_subset[elms_subset])>0:
            
            self.mob_work_dod, _ = np.polyfit(x[elms_subset],self.mob_work[elms_subset],1)    
            self.mob_work_avg = np.mean(self.mob_work[elms_subset])
            
        else:
            
            self.mob_work_dod = np.nan    
            self.mob_work_avg = np.nan
            
        elms_subset = (self.mob_resident == self.mob_resident)*elms
        
        if len(elms_subset[elms_subset])>0:    
            
            self.mob_resident_dod, _ = np.polyfit(x[elms_subset],self.mob_resident[elms_subset],1)     
            self.mob_resident_avg = np.mean(self.mob_resident[elms_subset])   
            
        else:
            
            self.mob_resident_dod = np.nan    
            self.mob_resident_avg = np.nan
        
        return
    
    def add_income(self,gross_income_per_head):        
        """
        Add regional gross income per head.
        
        Parameters
        ----------
        gross_income_per_head : float
            The gross basic income per head for the region (£ pounds 2018).
    
        Declare  
        -------
        gross_income_per_head : float
            The gross basic income per head for the region (£ pounds 2018).
        
        """
        
        self.gross_income_per_head = gross_income_per_head
        
        return
    
    def add_covid_deaths(self,covid_death_rate):
        """
        Add the number of covid deaths per capita.
        
        Parameters
        ----------
        covid_death_rate : float
            The covid_death_rate average for the months of May and June (per 100,000 people).
    
        Declare  
        -------
        covid_death_rate : float
            The covid_death_rate average for the months of May and June (per 100,000 people).
        
        """
        
        self.covid_death_rate = covid_death_rate
        
        return
    
    def add_geobounds(self,poly,country,urbanisation):
        """
        Define region and categorise the geographic bounds and geography.  
        
        Parameters
        ----------
        poly : Polygon or MultiPolygon type from shapely module
            The borders of the region defined geographically on the OSGB36 grid (eastings, northings).
        country : str 
            The United Kingdom Country the region inhabits.
        urbanisation : str
            The 'urbanisation' of the region a binary choice between 'urban' and 'rural'.
            
        Declare  
        -------
        poly : Polygon or MultiPolygon type from shapely module
            The borders of the region defined geographically on the OSGB36 grid (eastings, northings).
        country : str 
            The United Kingdom Country the region inhabits.
        urbanisation : str
            The 'urbanisation' of the region a binary choice between 'urban' and 'rural'.
        
        """        
        self.poly = poly
        self.country = country
        self.urbanisation = urbanisation
        
        return       