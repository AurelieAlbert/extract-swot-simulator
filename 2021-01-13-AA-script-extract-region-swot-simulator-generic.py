#!/usr/bin/env python

import xarray as xr
import numpy as np
import glob
import os
import sys


def check_data_region(data,region,file,latmin,latmax,lonmin,lonmax):
    ds=xr.open_dataset(file)
    if data == 'karin':
        latfile=ds.latitude
        lonfile=ds.longitude
    if data == 'nadir':
        latfile=ds.latitude_nadir
        lonfile=ds.longitude_nadir
    if region == 'NANFL':
        ind_region_all=np.where((latfile < latmax) & (latfile > latmin) & 
        (lonfile < lonmax) & (lonfile > lonmin))
        ind_region=ind_region_all[0]
    if region == 'MEDWEST':
        ind_region1=np.where((latfile < latmax) & (latfile > latmin) & 
        (lonfile < lonmax) & (lonfile > 0))
        ind_region2=np.where((latfile < latmax) & (latfile > latmin) & 
        (lonfile < 360) & (lonfile > lonmin+360))
        ind_region=np.concatenate((ind_region1[0],ind_region2[0]),axis=0)
    if len(ind_region) > 0:
        check=1
    else:
        check=0
    return check,ind_region
    

def check_data_nonan(data,file,ind_region):
    ds=xr.open_dataset(file)
    if data == 'karin':
        latfile=ds.latitude
        lonfile=ds.longitude
        ssh=ds.ssh_karin    
    if data == 'nadir':
        latfile=ds.latitude_nadir
        lonfile=ds.longitude_nadir
        ssh=ds.ssh_nadir    
    numlines_region_unique=np.unique(ind_region)
    check=0
    isdata_all=[]
    for k in np.arange(len(numlines_region_unique)):
        if data == 'karin':     
            isdata=np.where(np.isnan(ssh[numlines_region_unique[k],:])==False)
            if len(isdata[0])>0:
                check=1
                isdata_all.append(numlines_region_unique[k])
        if data == 'nadir':
            if np.isnan(ssh[numlines_region_unique[k]]) == False:
                check=1
                isdata_all.append(numlines_region_unique[k])
    return check,isdata_all



## parser and main
def script_parser():
    """Customized parser.
    """
    from optparse import OptionParser
    usage = "usage: %prog  --jsonfile name --dir dir"
    parser = OptionParser(usage=usage)
    parser.add_option('--reg', help="Region", dest="region", type="string", nargs=1)
    parser.add_option('--phase', help="Phase", dest="phase", type="string", nargs=1)
    parser.add_option('--data', help="Data", dest="data", type="string", nargs=1)
    return parser

def main():
    parser = script_parser()
    (options, args) = parser.parse_args()
    optdic=vars(options)

    region = optdic['region']
    phase = optdic['phase']
    data = optdic['data']
    simu='eNATL60-BLB002' # or eNATL60-BLBT02

    tdir='/work/ALT/swot/aval/wisa/tmp/inland_cleaning/swot_simulator_'+phase+'/'+simu+'-SSH-1h/'+data
    files=glob.glob(tdir+'/*/*nc')

    #parameters for the region to consider
    if (region == 'NANFL'):
        latmin=30
        latmax=40
        lonmin=-55+360
        lonmax=-40+360
    if (region == 'MEDWEST'):
        latmin=35.1
        latmax=44.4
        lonmin=-5.7
        lonmax=9.6

    for f in np.arange(len(files)):
        file=files[f]
        nfile=file.split('/')[-1]
        odir='/work/ALT/odatis/eNATL60/alberta/SWOT-sim/'+region+'/'+phase+'/'+data+'/'
        filename=odir+nfile
        if not os.path.exists(filename):
            check, ind_region = check_data_region(data,region,file,latmin,latmax,lonmin,lonmax)
            if check == 1:
                check2,isdata = check_data_nonan(data,file,ind_region)
                if check2 == 1:
                    print('extract data for file '+file)
                    ds=xr.open_dataset(file)
                    ds_regnonan=ds.isel(num_lines=isdata)
                    if not os.path.exists(odir):
                        os.makedirs(odir)
                    ds_regnonan.to_netcdf(path=filename,mode='w')

if __name__ == '__main__':
    sys.exit(main() or 0)


