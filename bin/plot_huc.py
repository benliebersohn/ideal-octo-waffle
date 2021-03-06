#!/usr/bin/env python3
"""Plots watersheds and their context within a HUC.
"""
import os,sys
import logging
import numpy as np
from matplotlib import pyplot as plt
import shapely

import rasterio.rio.clip

import workflow.hilev
import workflow.ui
import workflow.files
import workflow.plot


def get_args():
    parser = workflow.ui.get_basic_argparse(__doc__)
    workflow.ui.huc_source_options(parser)
    workflow.ui.dem_source_options(parser)
    workflow.ui.huc_args(parser)
    return parser.parse_args()

def get_huc(args):
    workflow.ui.setup_logging(args.verbosity, args.logfile)

    sources = workflow.files.get_sources(args)

    # collect data
    hucs, centroid = workflow.hilev.get_hucs(args.HUC, sources['HUC'], False)
    rivers = workflow.hilev.get_rivers(args.HUC, sources['HUC'])
    dem_profile, dem = workflow.hilev.get_dem(args.HUC, sources)

    # simple triangulation for elevation data
    footprint = shapely.ops.cascaded_union(list(hucs.polygons())).simplify(10)
    
    args.refine_max_area = footprint.area / 1000.
    mesh_points2, mesh_tris = workflow.hilev.triangulate(footprint, None, args, False)

    # elevate to 3D
    mesh_points3 = workflow.hilev.elevate(mesh_points2, dem, dem_profile)
    return centroid, hucs, rivers, (mesh_points3, mesh_tris)
    
def plot(centroid, hucs, rivers, triangulation):
    # plot
    fig = plt.figure(figsize=(4,5))
    ax = fig.add_subplot(111)
    mappable = workflow.plot.triangulation(*triangulation, linewidth=0)
    fig.colorbar(mappable, orientation="horizontal", pad=0.1)
    workflow.plot.hucs(hucs, 'k', linewidth=0.7)
    workflow.plot.rivers(rivers, color='white', linewidth=0.5)
    ax.set_aspect('equal', 'datalim')
    ax.set_xlabel('')
    ax.set_xticklabels([round(0.001*tick) for tick in ax.get_xticks()])
    plt.ylabel('')
    ax.set_yticklabels([round(0.001*tick) for tick in ax.get_yticks()])
    #plt.savefig('my_mesh')
    plt.show()
        

if __name__ == '__main__':
    args = get_args()
    centroid, hucs, rivers, triangulation = get_huc(args)
    plot(centroid, hucs, rivers, triangulation)
        

    
    
    
