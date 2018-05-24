"""Configuration"""

import sys,os
import fiona
import rasterio

rcParams = { "data dir" : "/Users/uec/research/water/data/meshing/data",
             "dem data dir" : "dem",
             "HUC data dir" : "hydrologic_units",
             "packages data dir" : "packages",
             "hydro data dir" : "hydrography",
             "NED file templates" : ["USGS_NED_13_%s%s_IMG","%s%s"],
             "NED base URL" : "https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/13/IMG/",
             "HUC file templates" : ["WBD_%s_HU2_Shape",],
             "HUC base URL" : "https://prd-tnm.s3.amazonaws.com/StagedProducts/Hydrography/WBD/HU2/Shape/",
             "epsg" : 5070, # default Albers equal area conic
             }


def default_crs():
    return fiona.crs.from_epsg(rcParams['epsg'])


def huc_str(huc):
    """Converts a huc int or string to a standard-format huc string."""
    if type(huc) is str:
        if len(huc)%2 == 1:
            huc = "0"+huc
    elif type(huc) is int:
        digits = math.ceil(math.log10(huc))
        if digits % 2 == 1:
            digits += 1
        huc = ("%%0%ii"%digits)%huc
    else:
        raise RuntimeError("Cannot convert type %r to huc"%type(huc))
    return huc

def huc_path(huc):
    """Returns the path to the fully resolved final HUC.  If projected, in the standard coordinate system."""
    huc = huc_str(huc)
    huc2 = huc[0:2]
    filebase = "WBDHU%i.shp"%len(huc)
    return os.path.join(rcParams['data dir'], rcParams['HUC data dir'], rcParams['HUC file templates'][0]%huc2, filebase)


def load_huc(huc):
    """Reads a file to get a huc"""
    huc = huc_str(huc)
    filename = huc_path(huc)
    with fiona.open(filename, 'r') as fid:
        matching = [h for h in fid if h['properties']['HUC%i'%len(huc)] == huc]
        profile = fid.profile
    if len(matching) is not 1:
        raise RuntimeError("Invalid collection of HUC?")
    return profile, matching[0]

def load_dem(filename, index=1):
    """Reads a file to get an image raster"""
    with rasterio.open(filename, 'r') as fid:
        profile = fid.profile.copy()
        array = fid.read(index)
    return profile, array

def bounds_from_profile(profile):
    """Uses a profile to determine a raster bounds.  

    Note that if you have a file, this is equivalent to fid.bounds and
    that should be preferred.
    """
    xmin, ymax = profile['affine'] * (0,0)
    xmax, ymin = profile['affine'] * (profile['width'], profile['height'])
    return [xmin, ymin, xmax, ymax]
