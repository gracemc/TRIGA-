"""
This script will update the header files for PESTO observations so that they are compatible with
AIJ
"""
import glob
from astropy.io import fits
from astropy.time import Time, TimeDelta

file_list = glob.glob('*.fits.gz')

for i in range(len(file_list)):
    data, header = fits.getdata("{0}".format(file_list[i]), header=True)
    header.rename_keyword("CTRLTIME","DATE-OBS")
    #del header["NAXIS3"]
    timeutc=Time(header["DATE-OBS"], scale="utc",format="isot")
    header["Exposure"]=(header["EFF_EXP"]/1000.0, "The requested exposure time in sec")
    deltatime=TimeDelta(header["Exposure"],format="sec")
    timeutc-=deltatime
    header["DATE-OBS"]=(timeutc.isot,"UTC start of exposure date")

    fits.writeto("{0}".format(file_list[i]), data, header,overwrite=True)
