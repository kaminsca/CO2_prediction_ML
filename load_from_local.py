import h5py
import pandas as pd
import numpy as np
import os
import time

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
        data = {'date': pd.to_datetime(date,format='%m/%Y'),
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
    
def get_data_at_location(latitude, longitude):
    directory = '.\data\SWIRL3CO2'
    data_dicts = []
    array_idx = -1
    # start = time.time()

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with h5py.File(f, 'r') as file:
                # find lat/lon index on first time around
                if array_idx == -1:
                    # get index of location
                    lats = file['Data/geolocation/latitude'][()].flatten()
                    lons = file['Data/geolocation/longitude'][()].flatten()

                    lat_idx = np.where(lats == latitude)[0]
                    lon_idx = np.where(lons == longitude)[0]
                    array_idx = np.intersect1d(lat_idx, lon_idx)
                    print("Array index: ", array_idx)
                    
                    # Make sure lat_idx and lon_idx are not empty
                    if not array_idx:
                        raise ValueError("Latitude or longitude not in dataset")

                # metadata
                date = str(file['Attribute/metadata/month'][()].item()) + '/' + str(file['Attribute/metadata/year'][()].item())
                
                # consolidate data
                data = {'date': pd.to_datetime(date,format='%m/%Y'),
                        'latitude': latitude, 
                        'longitude': longitude,
                        'co2_average': file['Data/latticeInformation/XCO2BiasCorrectedAverage'][()].flatten()[array_idx][0],
                        'co2_minimum': file['Data/latticeInformation/XCO2BiasCorrectedMinimum'][()].flatten()[array_idx][0],
                        'co2_maximum': file['Data/latticeInformation/XCO2BiasCorrectedMaximum'][()].flatten()[array_idx][0],
                        'co2_median': file['Data/latticeInformation/XCO2BiasCorrectedMedian'][()].flatten()[array_idx][0],
                        'co2_std_dev': file['Data/latticeInformation/XCO2BiasCorrectedStandardDeviation'][()].flatten()[array_idx][0],
                        'num_observation_points': file['Data/latticeInformation/numObservationPoints'][()].flatten()[array_idx][0]
                        }
                data_dicts.append(data)
    combined_df = pd.DataFrame(data_dicts)
    # print("\n--- %s seconds ---" % (time.time() - start))
    return combined_df


# if __name__ == '__main__':
    # setup :)
    # file = '.\data\SWIRL3CO2\GOSATTFTS2009060120090630_03C01SV0305.h5'
    
    # if debug:
    #     show_file(file)
    #     print('---------------- ------------------')

    # df = get_relevant_data(file)
    # if debug:
    #     print(df)
    #     print(df[df.num_observation_points > 0])

    # data = get_data_at_location(83.75, -76.25)
    # if debug:
        # print(data)
