import h5py
import pandas as pd
import numpy as np

debug = True

def print_name(name, obj, filter_metadata=True):
    if ('Metadata' in name or 'metadata' in name) and filter_metadata:
        return
    if isinstance(obj, h5py.Dataset):
        print ('Dataset:', name)
    elif isinstance(obj, h5py.Group):
        print ('Group:', name)
    
def show_file(file_path):
    f = h5py.File(file_path,'r')
    for item in f.keys():
        f.visititems(print_name)

def get_relevant_data(file_path):
    with h5py.File(file_path, 'r') as file:
        # metadata
        month = str(file['Attribute/metadata/month'][()].item())
        year = str(file['Attribute/metadata/year'][()].item())
        date = month + '/' + year

        if debug:
            print(date)

        # actual data
        lats = file['Data/geolocation/latitude'][()]
        lons = file['Data/geolocation/longitude'][()]
        co2_avg = file['Data/latticeInformation/XCO2BiasCorrectedAverage'][()]
        co2_min = file['Data/latticeInformation/XCO2BiasCorrectedMinimum'][()]
        co2_max = file['Data/latticeInformation/XCO2BiasCorrectedMaximum'][()]
        co2_med = file['Data/latticeInformation/XCO2BiasCorrectedMedian'][()]
        co2_std = file['Data/latticeInformation/XCO2BiasCorrectedStandardDeviation'][()]
        co2_num_obs = file['Data/latticeInformation/numObservationPoints'][()]

        # consolidate data
        data = {'date': date,
                'latitude': lats.flatten(), 
                'longitude': lons.flatten(),
                'co2_average': co2_avg.flatten(),
                'co2_minimum': co2_min.flatten(),
                'co2_maximum': co2_max.flatten(),
                'co2_median': co2_med.flatten(),
                'co2_std_dev': co2_std.flatten(),
                'num_observation_points': co2_num_obs.flatten()
                }
        df = pd.DataFrame(data)
        return df

if __name__ == '__main__':
    # setup :)
    file = '.\data\SWIRL3CO2\GOSATTFTS2009060120090630_03C01SV0305.h5'
    
    if debug:
        show_file(file)
        print('---------------- ------------------')

    df = get_relevant_data(file)
    if debug:
        print(df)
