#python gen_cmds.py --check

rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_ag_c/*.kea" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum
rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_total_c/*.kea" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum
rsgischkgdalfile.py -i "/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_total_co2/*.kea" --printerrs --rmerr --nbands 1 --epsg 4326 --chkproj --readimg --chksum

