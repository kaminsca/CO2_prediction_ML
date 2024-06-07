import h5py


def print_name(name, obj):
    if isinstance(obj, h5py.Dataset):
        print ('Dataset:', name)
    elif isinstance(obj, h5py.Group):
        print ('Group:', name)
    
f = h5py.File('.\data\SWIRL3CO2\GOSATTFTS2009060120090630_03C01SV0305.h5','r')
for item in f.keys():
    # print (item) #+ ":", f[item]
    f.visititems(print_name)
 
#Open the H5 file in read mode
# with h5py.File('.\data\SWIRL3CO2\GOSATTFTS2009060120090630_03C01SV0305.h5', 'r') as file:
    # print("Keys: %s" % file.keys())
    # a_group_key = list(file.keys())[0]
     
    # # Getting the data
    # data = list(file[a_group_key])
    # print('data: ', data)