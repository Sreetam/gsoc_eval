#importing libraries
import glob
import scipy.signal as ss
import numpy as np
import matplotlib.pyplot as plt
import h5py as hp
from pytz import timezone as ptz
from pytz import utc as utc
from datetime import datetime as dt
import pandas as pd


l = glob.glob("./*.h5")# The file path can be changed according to requirements
# print("File number you want to process: ")# This is a user input if the user wants to process any other files in
                                            # the folder. Uncomment if there is a user choice involved.
a = 0       # If there was a choice, it would be replaced by some search function which would search the file and
            # put its index value in a
h5name = l[a]
print("\nFile to be processed: "+h5name+"\n")
ti = int(h5name[2:21])
ti = ti / (10)**8
date = dt.utcfromtimestamp(ti)
timeAtCERN = utc.localize(date, is_dst=None).astimezone(ptz('CET'))
print("UTC time:",date)                    #UTC timestamp
print("CERN time:", timeAtCERN)            #CERN timestamp


file = hp.File(h5name,'r')
path = []
gord = []
size = []
shpe = []
dtyp = []               #changing the column headings lead to encoding problems.
def reading(name, obj): #a nice roundabout is making arrays and later integrating them into the framework
    path.append(name)
    if isinstance(obj, hp.Dataset):
        gord.append('Dataset')        #checking if its a group or a dataset
        size.append(obj.size)
        shpe.append(obj.shape)
        try:
            dtyp.append(obj.dtype)
        except TypeError:
            dtyp.append("Unsupported Datatype")      #in case if things go wrong
    else:
        gord.append('Group')
        size.append('')
        shpe.append('')
        dtyp.append('')
        
file.visititems(reading)          #recursively calling visititems

df = pd.DataFrame()               #declaring the dataframe
df['Name'] = np.array(path)
df['Type'] = np.array(gord)
df['Size'] = np.array(size)
df['Shape'] = shpe
df['Datatype'] = np.array(dtyp)
df.to_csv('output.csv', sep=',')  #much more simple than using csv library


img1D = file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData"]         #Retrieving 1D image data
ih = file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight"][0]
iw = file["/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth" ][0]
img2D = np.reshape(img1D, (ih,iw))                                              #Reshaping image
filteredImage = ss.medfilt(img2D)                                               #Filtering image
plt.imshow(filteredImage)
plt.savefig("Filtered_Image.png")

