#python gen_cmds.py --check

rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_ag_c/*.tif" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum
rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_total_c/*.tif" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum
rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_total_co2/*.tif" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum

