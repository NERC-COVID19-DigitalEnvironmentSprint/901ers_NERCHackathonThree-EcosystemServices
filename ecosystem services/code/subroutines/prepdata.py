# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 17:05:50 2020

The prepdata file contains definitions that can be helpful in complying for a 
general format.

@author: aargl
"""

### Imports
import geopandas as gpd
import pandas as pd
import numpy as np
import datetime

### Local Imports
from .secondary import similar_string, convert_3D_2D, region

### Classes

class Collate():
    
    def __init__(self):
        """
        Collate class allows for various regional datasets to be made
        consistent with the mobility data.

        Returns
        -------
        None.

        """

        return
        
    
    def add_iso_1(self,datafile):
        
        
        self.dataframe_iso_1 = gpd.read_file(datafile)
        self.dataframe_iso_1 = self.dataframe_iso_1.to_crs('EPSG:27700')
        self.__iso_name = np.array(self.dataframe_iso_1.iloc[:,6].astype(str))
        self.__iso_country = np.array(self.dataframe_iso_1.iloc[:,3].astype(str))
        self.__iso_description = np.array(self.dataframe_iso_1.iloc[:,9].astype(str))
        self.__iso_poly = np.array(self.dataframe_iso_1.iloc[:,-1])
        self.__num_iso = len(self.__iso_name)
        
        return    
    
    
    def add_counties(self,datafile):
             
        self.dataframe_counties = gpd.read_file(datafile)
        self.__county_name = np.array(self.dataframe_counties.iloc[:,0].astype(str))
        self.__county_description = np.array(self.dataframe_counties.iloc[:,1].astype(str))
        self.__county_poly = np.array(self.dataframe_counties.iloc[:,2])
        self.__num_counties = len(self.__county_name)
        
        return
    
    def add_district(self,datafile):
             
        self.dataframe_districts = gpd.read_file(datafile)
        self.__district_name = np.array(self.dataframe_districts.iloc[:,0].astype(str))
        self.__district_description = np.array(self.dataframe_districts.iloc[:,2].astype(str))
        self.__district_poly = np.array(self.dataframe_districts.iloc[:,-1])
        self.__num_districts = len(self.__district_name)
        
        return
    
    
    def add_ospark_areas(self,datafile):
                
        self.dataframe_osgreen = gpd.read_file(datafile)
        self.dataframe_osgreen.geometry = convert_3D_2D(self.dataframe_osgreen.geometry)
        self.__osgreen_type = np.array(self.dataframe_osgreen.iloc[:,1])
        self.__osgreen_type1 = np.array(self.dataframe_osgreen.iloc[:,3])
        self.__num_park_areas = len(self.__osgreen_type)
        
        return
    
    
    def add_mobility(self,datafile):
        
        self.mobility_dataframe = pd.read_excel(datafile)
        self.__region_name_mob_r = np.array(self.mobility_dataframe.iloc[:,2].astype(str))
        region_name_mob = np.unique(self.__region_name_mob_r)
        
        self.num_regions = len(region_name_mob)
        
        self.__iso_code = np.zeros(self.num_regions,dtype=list)
        self.region_name = np.zeros(self.num_regions,dtype=list)
        
        for reg1 in range(0,self.num_regions):
            
            for reg2 in range(0,len(self.__region_name_mob_r)):
                
                if region_name_mob[reg1] == self.__region_name_mob_r[reg2]:
                    
                    self.__iso_code[reg1] = self.mobility_dataframe.iloc[reg2,4]
                    self.region_name[reg1] = self.__region_name_mob_r[reg2]
                    
                    break
                
        return
    
    
    def add_income(self,datafile):
        
        self.income_dataframe = pd.read_excel(datafile)
        self.__income_name = np.array(self.income_dataframe.iloc[1:,2].astype(str))
        self.__gross_income_per_head = np.array(self.income_dataframe.iloc[1:,3])
        self.__num_income = len(self.__income_name)
        
        return
    
    def add_covid_deaths(self,datafile):
        
        self.covid_dataframe = pd.read_excel(datafile)
        self.__covid_name = np.array(self.covid_dataframe.iloc[1:,0].astype(str))
        self.__covid_death_rate = np.array(self.covid_dataframe.iloc[1:,2])
        self.__num_covid = len(self.__covid_name)
        
        return
    
        
    def define_regions(self):
        
        self.regions = np.zeros(self.num_regions,dtype=region)
        
        for reg1 in range(0,self.num_regions):
            
            name = self.region_name[reg1]
            self.regions[reg1] = region(self.region_name[reg1],self.__iso_code[reg1])

            elms = (self.__region_name_mob_r == name)
            dates_1 = np.array(self.mobility_dataframe.iloc[elms,6].astype(str))
            D = len(dates_1)
            dates = np.zeros(D,dtype=datetime.datetime)
            for d in range(0,D):
                
                dates[d] = datetime.datetime.strptime(dates_1[d].split('T')[0],'%Y-%m-%d')   
                
            
            mob_retail_rec = np.array(self.mobility_dataframe.iloc[elms,7])
            mob_park = np.array(self.mobility_dataframe.iloc[elms,9])
            mob_groc = np.array(self.mobility_dataframe.iloc[elms,8])
            mob_transit = np.array(self.mobility_dataframe.iloc[elms,10])
            mob_work = np.array(self.mobility_dataframe.iloc[elms,11])
            mob_resident = np.array(self.mobility_dataframe.iloc[elms,12])
            self.regions[reg1].add_mobility(dates,mob_retail_rec,mob_park,mob_groc,mob_transit,mob_work,mob_resident)
            
            # compare strings
            wrong = ['Merseyside','South Yorkshire','Tyne and Wear','West Yorkshire','West Midlands','Greater Manchester','North East Lincolnshire']
            str_check = np.zeros(self.__num_iso)     
            check = False
            
            for reg2 in range(0,self.__num_iso):
                
                if all(item != self.region_name[reg1] for item in wrong):
                    
                    check = True
                    
                    if self.region_name[reg1] == 'Isle of Anglesey':
                                            
                       str_check[reg2] = similar_string('Anglesey',self.__iso_name[reg2])
                        
                    else:
                        
                       str_check[reg2] = similar_string(self.region_name[reg1],self.__iso_name[reg2])
                        
                        
            urb_def = ['Metropolitan Borough','Metropolitan Borough (City)','Unitary Authority (City)','Unitary District (City)','Unitary Authority']
            met_regions = ['Greater London','Belfast','Cardiff','Newport','Blackpool']
            rural_regions = ['East Riding of Yorkshire','Wrexham Principal Area ','Worcestershire','Windsor and Maidenhead','Wiltshire','West Berkshire','Vale of Glamorgan','Torfaen Principal Area','South Gloucestershire','Shropshire','Rhondda Cynon Taff ','Redcar and Cleveland','Pembrokeshire','Northumberland','North Somerset','Neath Port Talbot Principle Area','Merthyr Tydfil County Borough','Isle of Wight','Isle of Anglesey','Gwynedd','Flintshire','Denbighshire','County Durham','Cornwall','Powys','Conwy Principal Area','Carmarthenshire','Ceredigion']
            
            if check == False:
                
                country = 'England'
                urbanisation = 'Urban'
               
                if self.region_name[reg1] == 'North East Lincolnshire':
                    
                    str_check = np.zeros(self.__num_districts)
                    
                    for reg2 in range(0,self.__num_districts):
                        
                        str_check[reg2] = similar_string(self.region_name[reg1],self.__district_name[reg2])
                    
                    elms = str_check == max(str_check)
                    self.regions[reg1].add_geobounds(self.__district_poly[elms][0],country,urbanisation)    
                    
                else:

                    str_check = np.zeros(self.__num_counties)
                    for reg2 in range(0,self.__num_counties):
                        
                        str_check[reg2] = similar_string(self.region_name[reg1],self.__county_name[reg2])
                
                    elms = str_check == max(str_check)                        
                    
                    self.regions[reg1].add_geobounds(self.__county_poly[elms][0],country,urbanisation)    
                
                
            else:


                elms = str_check == max(str_check)                
                country = self.__iso_country[elms][0]
                urbanisation = self.__iso_description[elms][0]
                
                if (((any(urb==urbanisation for urb in urb_def) or any(met == self.region_name[reg1] for met in met_regions)) and all(rul != self.region_name[reg1] for rul in rural_regions))):
                    
                    urbanisation = 'Urban'
                    
                else:
                    
                    urbanisation = 'Rural'  
                    
                poly = self.__iso_poly[elms][0]
                self.regions[reg1].add_geobounds(poly,country,urbanisation)   
                
        wrong = ['Borough of Halton','Bracknell Forest','Bridgend County Borough','Windsor and Maidenhead','Slough','West Dunbartonshire Council','Torfaen Principal Area','West Dunbartonshire Council ','West Berkshire','Rhondda Cynon Taff','Caerphilly County Borough','Carmarthenshire','Ceredigion','Denbighshire','East Ayrshire Council','East Dunbartonshire Council','Flintshire','Herefordshire','Leicestershire','Moray','North Ayrshire Council','Middlesbrough','Merthyr Tydfil County Borough','Redcar and Cleveland','Renfrewshire','Pembrokeshire','Reading']
        for reg1 in range(0,self.num_regions):
            
            str_check = np.zeros(self.__num_income)
            
            if all(item != self.region_name[reg1] for item in wrong):
            
                for reg2 in range(0,self.__num_income):
                    
                    if self.__income_name[reg2] == self.__income_name[reg2]:
                        
                        str_check[reg2] = similar_string(self.region_name[reg1],self.__income_name[reg2])
                        
                    elms = str_check == max(str_check)
                    
                            
            else:
                        
                elms = str_check == -1                    
            
            if len(elms[elms==False]) < self.__num_income - 1:
                self.regions[reg1].add_income(np.mean(self.__gross_income_per_head[elms]))
            
            elif len(elms[elms==False]) == self.__num_income:
                
                self.regions[reg1].add_income(np.nan)
                
            else:
                self.regions[reg1].add_income(self.__gross_income_per_head[elms][0])

        wrong = ['Aberdeen City','Shetland Islands','South Ayrshire Council','West Lothian','West Midlands','South Lanarkshire','Aberdeenshire','West Lothian','West Dunbartonshire Council','Angus Council','Antrim and Newtownabbey','Ards and North Down','East Lothian Council','Fermanagh and Omagh','Inverclyde','Lisburn and Castlereagh','North Ayrshire Council','Orkney','Perth and Kinross','Renfrewshire','Scottish Borders','Na h-Eileanan an Iar','Moray','Midlothian','Mid and East Antrim','Edinburgh','Mid Ulster','Highland Council','Glasgow City','Fife','Falkirk','East Renfrewshire Council','East Dunbartonshire Council','East Ayrshire Council','Dundee City Council','Dumfries and Galloway','Derry and Strabane','Clackmannanshire','Causeway Coast and Glens','Belfast','Armagh City, Banbridge and Craigavon','Armagh City, Banbridge and Craigavon','Argyll and Bute Council']
        for reg1 in range(0,self.num_regions):
            
            str_check = np.zeros(self.__num_covid)
            
            if all(item != self.region_name[reg1] for item in wrong):
            
                for reg2 in range(0,self.__num_covid):
                    
            
                    if self.__covid_name[reg2] == self.__covid_name[reg2]:
                        
                        str_check[reg2] = similar_string(self.region_name[reg1],self.__covid_name[reg2])
                        
                    
                    elms = str_check == max(str_check)
                    
            else:
                        
                elms = str_check == -1                    
            if len(elms[elms==False]) == self.__num_covid:
                
                self.regions[reg1].add_covid_deaths(np.nan)
                
            else:
                
                self.regions[reg1].add_covid_deaths(self.__covid_death_rate[elms][0])


        return
        
        
            
            
    def makegeopanda(self):
        names = []
        country = []
        urbanisation = []
        iso_3166_2_code = []
        geometry = []
        
        for reg in range(0,self.num_regions):
            
            names.append(self.regions[reg].name)
            country.append(self.regions[reg].country)
            urbanisation.append(self.regions[reg].urbanisation)
            iso_3166_2_code.append(self.regions[reg].iso_code) 
            geometry.append(self.regions[reg].polynomial)
            
        df = pd.DataFrame({'name':names,'country':country,'urbanisation':urbanisation,'iso_3166_2_code':iso_3166_2_code,'geometry':geometry})       
        
        self.dataframe_regions = gpd.GeoDataFrame(df,geometry='geometry',crs='EPSG:27700')
        self.dataframe_regions['area'] = self.dataframe_regions['geometry'].area
        
        return
    
    def define_intersection(self):
        
        sport_labels = ['Bowling Green','Golf Course','Tennis Court','Playing Field','Other Sports Facility']
        park_labels = ['Allotments Or Community Growing Spaces','Playing Field','Cemetery','Public Park Or Garden','Play Space','Religious Grounds']
        m2_to_ha = 0.0001
        
        self.alloments_area = np.zeros(self.num_regions)
        self.alloments_num = np.zeros(self.num_regions)
        self.bowling_area = np.zeros(self.num_regions)
        self.bowling_num = np.zeros(self.num_regions)
        self.cemetery_area = np.zeros(self.num_regions)
        self.cemetery_num = np.zeros(self.num_regions)
        self.golf_area = np.zeros(self.num_regions)
        self.golf_num = np.zeros(self.num_regions)
        self.other_sports_area = np.zeros(self.num_regions)
        self.other_sports_num = np.zeros(self.num_regions)
        self.play_space_area = np.zeros(self.num_regions)
        self.play_space_num = np.zeros(self.num_regions)
        self.play_field_area = np.zeros(self.num_regions)
        self.play_field_num = np.zeros(self.num_regions)
        self.park_area = np.zeros(self.num_regions)
        self.park_num = np.zeros(self.num_regions)
        self.religious_area = np.zeros(self.num_regions)
        self.religious_num = np.zeros(self.num_regions)
        self.tennis_area = np.zeros(self.num_regions)
        self.tennis_num = np.zeros(self.num_regions)
        self.total_sports_area = np.zeros(self.num_regions)
        self.total_sports_num = np.zeros(self.num_regions)
        self.total_nonsports_area = np.zeros(self.num_regions)
        self.total_nonsports_num = np.zeros(self.num_regions)
        self.total_greenspace_area = np.zeros(self.num_regions)
        self.total_greenspace_num = np.zeros(self.num_regions)
        self.region_area = np.zeros(self.num_regions)
        
        for reg in range(0,1):#self.num_regions):
            
            if self.regions[reg].country != 'Northern Ireland':
                
                
                
                polys1  = gpd.GeoSeries(self.dataframe_regions.iloc[reg,4])
                df1 = np.linspace(1,len(polys1),len(polys1))
                dataframe_regions_copy = pd.DataFrame({'df1':df1,'geometry1':polys1})
                reg_poly = gpd.GeoDataFrame(dataframe_regions_copy,geometry='geometry1',crs='EPSG:27700')
                intersection = gpd.overlay(reg_poly,self.dataframe_osgreen,how='intersection')
                intersection['area1'] = intersection['geometry'].area
                category = np.array(intersection.iloc[:,2].astype(str))
                areas = np.array(intersection.iloc[:,-1])*m2_to_ha

                self.total_greenspace_num[reg] = len(category)
                self.region_area[reg] = self.dataframe_regions.iloc[reg,5]*m2_to_ha
         
                for cat in range(0,int(self.total_greenspace_num[reg])):
                    
                    if category[cat] == 'Allotments Or Community Growing Spaces':
                    
                        self.alloments_area[reg] = self.alloments_area[reg] + areas[cat]
                        self.alloments_num[reg] = self.alloments_num[reg] + 1
                        
                    elif category[cat] == 'Bowling Green':
                        
                        self.bowling_area[reg] = self.bowling_area[reg] + areas[cat]
                        self.bowling_num[reg] = self.bowling_num[reg] + 1
                        
                    elif category[cat] == 'Cemetery':
                                                
                        self.cemetery_area[reg] = self.cemetery_area[reg] + areas[cat]
                        self.cemetery_num[reg] = self.cemetery_num[reg] + 1
                        
                        
                    elif category[cat] == 'Golf Course':
                        
                        self.golf_area[reg] = self.golf_area[reg] + areas[cat]
                        self.golf_num[reg] = self.golf_num[reg] + 1
                        
                    elif category[cat] == 'Other Sports Facility':
                        
                        self.other_sports_area[reg] = self.other_sports_area[reg] + areas[cat]
                        self.other_sports_num[reg] = self.other_sports_num[reg] + 1
    
                        
                    elif category[cat] == 'Play Space':
                        
                        self.play_space_area[reg] = self.play_space_area[reg] + areas[cat]
                        self.play_space_num[reg] = self.play_space_num[reg] + 1
                        
                    elif category[cat] == 'Playing Field':
                        
                        self.play_field_area[reg] = self.play_field_area[reg] + areas[cat]
                        self.play_field_num[reg] = self.play_field_num[reg] + 1
    
                    elif category[cat] == 'Religious Grounds':
                        
                        self.religious_area[reg] = self.religious_area[reg] + areas[cat]
                        self.religious_num[reg] = self.religious_num[reg] + 1
                        
                    elif category[cat] == 'Public Park Or Garden':
                        
                        self.park_area[reg] = self.park_area[reg] + areas[cat]
                        self.park_num[reg] = self.park_num[reg] + 1
                        
                    elif category[cat] == 'Tennis Court':
                        
                        self.tennis_area[reg] = self.tennis_area[reg] + areas[cat]
                        self.tennis_num[reg] = self.tennis_num[reg] + 1
                        
                    if any(sport == category[cat] for sport in sport_labels):
                        
                        self.total_sports_area[reg] = self.total_sports_area[reg] + areas[cat]
                        self.total_sports_num[reg] = self.total_sports_num[reg] + 1
                     
                    if any(park == category[cat] for park in park_labels):
                        
                        self.total_nonsports_area[reg] = self.total_nonsports_area[reg] + areas[cat]
                        self.total_nonsports_num[reg] = self.total_nonsports_num[reg] + 1

                    
                    self.total_greenspace_area[reg] = self.total_greenspace_area[reg] + areas[cat]
            
                print(self.total_greenspace_area[reg]/self.region_area[reg])
                
    def savedata(self,save_dir):
        
        names = []
        names_mob = []
        country = []
        urbanisation = []
        iso_3166_2_code = []
        geometry = []
        area = []
        covid_deaths = []
        income = []     
        date_mob = []
        mob_retail_rec = []
        mob_park = []
        mob_groc =[]
        mob_transit = []
        mob_work = []
        mob_resident = []
        mob_retail_rec_avg = []
        mob_retail_rec_dod = []
        mob_park_avg = []
        mob_park_dod = []
        mob_groc_avg = []
        mob_groc_dod = []
        mob_transit_avg = []
        mob_transit_dod = []
        mob_work_avg = []
        mob_work_dod = []        
        mob_resident_avg = []
        mob_resident_dod = []
        total_greenspace_num = []
        total_greenspace = []
        total_greenspace_avg = []
        total_greenspace_frac = []
        total_nonsports_num = []
        total_nonsports = []
        total_nonsports_avg = []
        total_nonsports_frac = []
        total_sports_num = []
        total_sports = []
        total_sports_avg = []
        total_sports_frac = []
        alloments_num = []
        alloments = []
        alloments_avg = []
        alloments_frac = []
        bowling_num = []
        bowling = []
        bowling_avg = []
        bowling_frac = []
        cemetery_num = []
        cemetery = []
        cemetery_avg = []
        cemetery_frac = []
        golf_num = []
        golf = []
        golf_avg = []
        golf_frac = []
        other_num = []
        other = []
        other_avg = []
        other_frac = []
        religious_num = []
        religious = []
        religious_avg = []
        religious_frac = []
        tennis_num = []
        tennis = []
        tennis_avg = []
        tennis_frac = []
        park_num = []
        park = []
        park_avg = []
        park_frac = []
        play_field_num = []
        play_field = []
        play_field_avg = []
        play_field_frac = []
        play_space_num = []
        play_space = []
        play_space_avg = []
        play_space_frac = []
        
        
        
        for reg in range(0,self.num_regions):
            
            if self.regions[reg].country != 'Northern Ireland':
            
                names.append(self.regions[reg].name)
                country.append(self.regions[reg].country)
                urbanisation.append(self.regions[reg].urbanisation)
                iso_3166_2_code.append(self.regions[reg].iso_code) 
                geometry.append(self.regions[reg].polynomial)
                area.append(self.region_area[reg]) 
                covid_deaths.append(self.regions[reg].covid_death_rate)
                income.append(self.regions[reg].gross_income_per_head)
                mob_retail_rec_avg.append(self.regions[reg].mob_retail_rec_avg)
                mob_retail_rec_dod.append(self.regions[reg].mob_retail_rec_dod)
                mob_park_avg.append(self.regions[reg].mob_park_avg)
                mob_park_dod.append(self.regions[reg].mob_park_dod)
                mob_groc_avg.append(self.regions[reg].mob_groc_avg)
                mob_groc_dod.append(self.regions[reg].mob_groc_dod)
                mob_transit_avg.append(self.regions[reg].mob_transit_avg)
                mob_transit_dod.append(self.regions[reg].mob_transit_dod)
                mob_work_avg.append(self.regions[reg].mob_work_avg)
                mob_work_dod.append(self.regions[reg].mob_work_dod)
                mob_resident_avg.append(self.regions[reg].mob_resident_avg)
                mob_resident_dod.append(self.regions[reg].mob_resident_dod)
                total_greenspace_num.append(self.total_greenspace_num[reg])
                total_greenspace.append(self.total_greenspace_area[reg])
                total_greenspace_avg.append(self.total_greenspace_area[reg]/self.total_greenspace_num[reg])
                total_greenspace_frac.append(self.total_greenspace_area[reg]/self.region_area[reg])
                total_nonsports_num.append(self.total_nonsports_num[reg])
                total_nonsports.append(self.total_nonsports_area[reg])
                total_nonsports_avg.append(self.total_nonsports_area[reg]/self.total_nonsports_num[reg])
                total_nonsports_frac.append(self.total_nonsports_area[reg]/self.region_area[reg])
                total_sports_num.append(self.total_sports_num[reg])
                total_sports.append(self.total_sports_area[reg])
                total_sports_avg.append(self.total_sports_area[reg]/self.total_sports_num[reg])
                total_sports_frac.append(self.total_sports_area[reg]/self.region_area[reg])
                alloments_num.append(self.alloments_num[reg])
                alloments.append(self.alloments_area[reg])
                alloments_avg.append(self.alloments_area[reg]/self.alloments_num[reg])
                alloments_frac.append(self.alloments_area[reg]/self.region_area[reg])
                bowling_num.append(self.bowling_num[reg])
                bowling.append(self.bowling_area[reg])
                bowling_avg.append(self.bowling_area[reg]/self.bowling_num[reg])
                bowling_frac.append(self.bowling_area[reg]/self.region_area[reg])
                cemetery_num.append(self.cemetery_num[reg])
                cemetery.append(self.cemetery_area[reg])
                cemetery_avg.append(self.cemetery_area[reg]/self.cemetery_num[reg])
                cemetery_frac.append(self.cemetery_area[reg]/self.region_area[reg])
                golf_num.append(self.golf_num[reg])
                golf.append(self.golf_area[reg])
                golf_avg.append(self.golf_area[reg]/self.golf_num[reg])
                golf_frac.append(self.golf_area[reg]/self.region_area[reg])
                other_num.append(self.other_sports_num[reg])
                other.append(self.other_sports_area[reg])
                other_avg.append(self.other_sports_area[reg]/self.other_sports_num[reg])
                other_frac.append(self.other_sports_area[reg]/self.region_area[reg])        
                religious_num.append(self.religious_num[reg])
                religious.append(self.religious_area[reg])
                religious_avg.append(self.religious_area[reg]/self.religious_num[reg])
                religious_frac.append(self.religious_area[reg]/self.region_area[reg])
                tennis_num.append(self.tennis_num[reg])
                tennis.append(self.tennis_area[reg])
                tennis_avg.append(self.tennis_area[reg]/self.tennis_num[reg])
                tennis_frac.append(self.tennis_area[reg]/self.region_area[reg])
                park_num.append(self.park_num[reg])
                park.append(self.park_area[reg])
                park_avg.append(self.park_area[reg]/self.park_num[reg])
                park_frac.append(self.park_area[reg]/self.region_area[reg])
                play_field_num.append(self.play_field_num[reg])
                play_field.append(self.play_field_area[reg])
                play_field_avg.append(self.play_field_area[reg]/self.play_field_num[reg])
                play_field_frac.append(self.play_field_area[reg]/self.region_area[reg])
                play_space_num.append(self.play_space_num[reg])
                play_space.append(self.play_space_area[reg])
                play_space_avg.append(self.play_space_area[reg]/self.play_space_num[reg])
                play_space_frac.append(self.play_space_area[reg]/self.region_area[reg])
                
                num_days = len(self.regions[reg].dates_mob)
                
                for day in range(0,num_days):
                    
                    names_mob.append(self.regions[reg].name)
                    date_mob.append(self.regions[reg].dates_mob[day].strftime('%d/%m/%Y'))
                    mob_retail_rec.append(self.regions[reg].mob_retail_rec[day])
                    mob_park.append(self.regions[reg].mob_park[day])
                    mob_groc.append(self.regions[reg].mob_groc[day])
                    mob_transit.append(self.regions[reg].mob_transit[day])
                    mob_work.append(self.regions[reg].mob_work[day])
                    mob_resident.append(self.regions[reg].mob_resident[day])
        
        dataframedict = {'Reigion Name':names,'Country':country,'Urbanisation':urbanisation,'iso_3166_2_code':iso_3166_2_code,'Reigion Area (ha)':area,'COVID-19 Death Rate April-May (per 100,000)':covid_deaths,'Gross Income Per Head (2018 pounds)':income,'Mobility Retail & Recreation Average Post Lockdown (% from baseline)':mob_retail_rec_avg,'Mobility Retail & Recreation Rate of Change Post Lockdown (% from baseline per day)':mob_retail_rec_dod,'Mobility Parks Average Post lockdown (% from baseline)':mob_park_avg,'Mobility Park Rate of Change Post lockdown  (% from baseline per day)':mob_park_dod,\
                         'Mobility Grocery & Pharmacy Average Post Lockdown (% from baseline)':mob_groc_avg,'Mobility Grocery & Pharmacy Rate of Change Post Lockdown (% from baseline per day)':mob_groc_dod,'Mobility Transit Stations Average Post lockdown (% from baseline)':mob_transit_avg,'Mobility Transit Station Rate of Change Post lockdown  (% from baseline per day)':mob_transit_dod,'Mobility Workplaces Average Post lockdown (% from baseline)':mob_work_avg,'Mobility Workplaces Rate of Change Post lockdown  (% from baseline per day)':mob_work_dod,\
                         'Mobility Residential Average Post Lockdown (% from Baseline)':mob_resident_avg,'Mobility Residential Rate of Change Post Lockdown (% from Baseline)':mob_resident_dod,'Greenspace Number':total_greenspace_num,'Greenspace Area (ha)':total_greenspace,'Greenspace Average Area (ha)':total_greenspace_avg,'Greenspace Fraction':total_greenspace_frac,'Greenspace (non-sport) Number':total_nonsports_num,'Greenspace (non-sport) Area (ha)':total_nonsports,'Greenspace (non-sport) Average Area (ha)':total_nonsports_avg,'Greenspace (non-sport) Fraction':total_nonsports_frac,\
                         'Greenspace (sport) Number':total_sports_num,'Greenspace (sport) Area (ha)':total_sports,'Greenspace (sport) Average Area (ha)':total_sports_avg,'Greenspace (sport) Fraction':total_sports_frac,'Alloments Number':alloments_num,'Alloments Area (ha)':alloments,'Alloments Average Area (ha)':alloments_avg,'Alloments Fraction':alloments_frac,'Bowling Number':bowling_num,'Bowling Area (ha)':bowling,'Bowling Average Area (ha)':bowling_avg,'Bowling Fraction':bowling_frac,'Cemetery Number':cemetery_num,'Cemetery Area (ha)':cemetery,\
                         'Cemetery Average Area (ha)':cemetery_avg,'Cemetery Fraction':cemetery_frac,'Golf Course Number':golf_num,'Golf Course Area (ha)':golf,'Golf Course Average Aera':golf_avg,'Golf Course Fraction':golf_frac,'Other Sport Number':other_num,'Other Sport Area (ha)':other,'Other Sport Average Area (ha)':other_avg,'Other Sport Fraction':other_frac,'Religious Grounds Number':religious_num,'Religious Grounds Area (ha)':religious,'Religious Grounds Average Area (ha)':religious_avg,'Religious Grounds Fraction':religious_frac,'Tennis Court Number':tennis_num,\
                         'Tennis Court Area (ha)':tennis,'Tennis Court Average Area (ha)':tennis_avg,'Tennis Court Fraction':tennis_frac,'Public Park or Garden Number':park_num,'Public Park or Garden Area (ha)':park,'Public Park or Garden Average Area (ha)':park_avg,'Public Park or Garden Fraction':park_frac,'Playing Field Number':play_field_num,'Playing Field Area (ha)':play_field,'Playing Field Average Area (ha)':play_field_avg,'Playing Field Fraction':play_field_frac,'Play Space Number':play_space_num,'Play Space Area (ha)':play_space,'Play Space Average Aera':play_space_avg,\
                         'Play Space Fraction':play_field_frac}
        
        df = pd.DataFrame(dataframedict)       
        filename_csv = save_dir+'/greenspace_metrics_last.csv'
        df.to_csv(filename_csv)
        geographic_csv = save_dir+'/greenspace_metrics_geographic.shp'
        dgf = gpd.GeoDataFrame(df,geometry=geometry,crs='EPSG:27700')
        dgf.to_file(geographic_csv)
        dataframedict_temporal = {'Reigion Name':names_mob,'Dates':date_mob,'Mobility Retail & Recreation (% from Baseline)':mob_retail_rec,'Mobility Parks (% from Baseline)':mob_park,'Mobility Grocery & Pharmacy (% from Baseline)':mob_groc,'Mobility Transit Stations (% from Baseline)':mob_transit,'Mobility Workplaces (% from Baseline)':mob_work,'Mobility Residential (% from baseline)':mob_resident}
        df_temporal = pd.DataFrame(dataframedict_temporal)
        filename_temporal_csv = save_dir+'/region_mobility_over_time_last.csv'
        df_temporal.to_csv(filename_temporal_csv)
        return