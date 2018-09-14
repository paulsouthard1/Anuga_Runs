
# coding: utf-8



import os
import time
import sys
import anuga

from anuga import distribute, myid, numprocs, finalize


#------------------------------------------------------------------------------
# Do the domain creation on processor 0
#------------------------------------------------------------------------------
if myid == 0:
    # Create DEM from asc data
    anuga.asc2dem('11_fbe_c.asc', use_cache=False, verbose=True)

    # Create DEM from asc data
    anuga.dem2pts('11_fbe_c.dem', use_cache=False, 
                  verbose=True)


    bounding_polygon = anuga.read_polygon('channel.csv')


    domain = anuga.create_domain_from_regions(bounding_polygon,
    									boundary_tags={'exterior': [1]},
                                        maximum_triangle_area=1,
                                        mesh_filename='11f.msh',
                                        use_cache=False,
                                        verbose=True)


    #Name domain
    domain.set_name('11_fbe_c')
    domain.set_datadir('.')

    #Set quantities for domain, set dry bed
    domain.set_quantity('elevation', filename='11_fbe_c.pts')
    domain.set_quantity('friction',0.040)
    domain.set_quantity('stage',expression='elevation')


    #Define and set boundaries
    Br = anuga.Reflective_boundary(domain)      # Solid reflective wall
    Bt = anuga.Transmissive_boundary(domain)    # Continue all values on boundary
    domain.set_boundary({'exterior': Bt})

    # Setup inlet flow
    center = (538416.0, 4190718.0)
    radius = 10.0

    region0 = anuga.Region(domain, center=center, radius=radius)
    fixed_inflow = anuga.Inlet_operator(domain, region0 , Q=20)
else:
    domain = None

#------------------------------------------------------------------------------
# Now produce parallel domain
#------------------------------------------------------------------------------
domain = distribute(domain)

domain.set_store_vertices_uniquely(False)

for t in domain.evolve(yieldstep=500, finaltime=20000):
    if myid == 0:
        print domain.timestepping_statistics()

domain.sww_merge(delete_old=True)

finalize()