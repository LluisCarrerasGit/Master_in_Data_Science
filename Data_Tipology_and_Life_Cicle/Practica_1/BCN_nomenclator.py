# -*- coding: utf-8 -*-
"""

@author: Lluís Carreras González
@subject: Tipologia i cicle de vida de les dades
@studies: Master in Data Science

This file scraps the meaning and more info of the streets of Barcelona and saves the data 
in a CSV file.

"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# First, get the codes of the streets in Barcelona from a csv file downloaded from 
# the opendata service from Ajuntament de Barcelona.
street_info = urlopen("http://opendata-ajuntament.barcelona.cat/data/dataset/d7802fd1-cdfb-4562-9148-d18722d7e2d8/resource/2b010e59-6952-4b27-9c4e-47fcaf64c916/download")
with open('CARRERER.csv','wb') as output:
    output.write(street_info.read())

# Convert the CSV data in a pandas dataframe
street_codes_df = pd.read_csv("CARRERER.csv", encoding="utf8") 

# Select the columns we are interested in. 
street_codes_df = street_codes_df.iloc[:, [0, 2, 3, 4]]      

# Scrap the info for every street and save it in a list.
streets = []
for index, row in street_codes_df.iterrows():
    
    # The street codes must have 6 digits, adding zeroes to the left if necesary.
    code = str(row['CODI_VIA'])   
    formated_code = ("00000" + code)[-6:]
    url = "http://w10.bcn.cat/APPS/nomenclator/ficha.do?codic=" + formated_code + "&idioma=0"
    #Example: "http://w10.bcn.cat/APPS/nomenclator/ficha.do?codic=029400&idioma=0"
    
    # Scrapping snipet...
    try:
        html = urlopen(url)
        bsObj = BeautifulSoup(html)
        tags_list = bsObj.findAll("td", {"class":"textonoticia"})
        text_list = [tag.get_text() for tag in tags_list] 
        
        new_street = []
        new_street.append(code)
        
        description = text_list[1]
        new_street.append(description)
        
        aproving_date = text_list[3]
        new_street.append(aproving_date)
        
        former_names = text_list[4]
        new_street.append(former_names)
        
        districts = text_list[5].strip()
        new_street.append(districts)
        
        streets.append(new_street)
    except:
        pass

# Create a new dataframe from the info scrapped.  
labels = ['CODI', 'DESCRIPCIO', 'DATA_APROVACIO', 'NOMS_ANTERIORS', 'DISTRICTES']         
streets_df = pd.DataFrame.from_records(streets, columns=labels)

# Create a new dataframe that mixes the information from the two dataframes 
street_info_df = pd.concat([street_codes_df, streets_df], axis=1)
street_info_df = street_info_df.iloc[:, [0, 1, 2, 3, 5, 6, 7, 8]]

# Save the data from the datafrae into a CSV file.
street_info_df.to_csv('BCN_nomenclator.csv', sep='\t', encoding='utf-8')
