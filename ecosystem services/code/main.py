# -*- coding: utf-8 -*-
"""
Spyder Editor

This is the main script for the entire analysis.

@author: aargl
"""
### Imports
import os

### Local Imports
from subroutines import Collate, fig_1, fig_2

        
            
if __name__ == '__main__':
    
    
    ### Key directories
    # Main Script Location
    dir_main = os.path.dirname(os.path.realpath(__file__)) 
    # Unprocessed Data Location
    dir_data_raw = os.path.join(dir_main,'data','raw') 
    # Processed Data Location
    dir_data_processed = os.path.join(dir_main,'data','processed') 
    # Figure Location
    dir_figure = os.path.join(dir_main,'figures')
    
    ### Raw datafiles
    datafile_mobility = dir_data_raw+'/UK_mobility_town_plus_county.xlsx' 
    datafile_iso_1 = dir_data_raw+'/gadm36_GBR_2.shp'
    datafile_counties = dir_data_raw + '/Boundary-line-ceremonial-counties_region.shp'
    datafile_districts = dir_data_raw + '/district_borough_unitary_region.shp'
    datafile_greenspaces = dir_data_raw + '/GB_GreenspaceSite.shp'
    datafile_income = dir_data_raw + '/UK_GDHI per head of population at 2018 prices.xlsx'
    datafile_covid = dir_data_raw + '/UK_COVID_death.xlsx'
    
    ### Collate Raw Data
    # Gather Raw Data, if true collates raw data into processed. Saves time
    # for plotting and analysis when you already have the data and is False.
    process_raw_check = False
    
    if process_raw_check == True:
    
        prepare_data = Collate()                            # Start collating data from /data/raw/
        prepare_data.add_mobility(datafile_mobility)        # Add google mobility data
        prepare_data.add_iso_1(datafile_iso_1)              # Find regions that are mostly consistent with mobility data
        prepare_data.add_counties(datafile_counties)        # Find more regions for mobility data
        prepare_data.add_district(datafile_districts)       # Again 
        prepare_data.add_covid_deaths(datafile_covid)       # Define COVID death rate by region
        prepare_data.add_income(datafile_income)            # Define gross income by region
        prepare_data.add_ospark_areas(datafile_greenspaces) # Define OS Greenspace park regions
        prepare_data.define_regions()                       # Make geographic data consistent with one another
        prepare_data.makegeopanda()                         # Make geopandas of regions for use in the line bellow
        prepare_data.define_intersection()                  # Calculate intersection of OS Greenspace and Mobility regions
        prepare_data.savedata(dir_data_processed)           # Save relevant data as csv in /data/processed/
        
    ### Define Processed datafile
    datafile_general = dir_data_processed + '/greenspace_metrics.csv'
    geo_file = dir_data_processed + '/greenspace_metrics_geographic.shp'
    mob_temporal_file = dir_data_processed+'/region_mobility_over_time.csv'
    greenspace_metrics_gs_dist_added_file = dir_data_processed+'/greenspace_metrics (timestamp_1650)_gs_dist_added.xlsx'
    
    ### Produce Figures
    fig_1(geo_file,datafile_greenspaces,mob_temporal_file,dir_figure)
    #fig_2(greenspace_metrics_gs_dist_added_file,dir_figure)
    