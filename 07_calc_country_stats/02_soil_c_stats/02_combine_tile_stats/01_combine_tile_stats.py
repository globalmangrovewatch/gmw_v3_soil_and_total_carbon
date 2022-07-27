import glob
import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)
unq_cntry_vals = country_ids_lut["val"].keys()

gadm_lut_file ='../../gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)


glb_hist_data = numpy.zeros((201), dtype=numpy.uint32)

tile_stats_lut = dict()
tile_hist_lut = dict()
for val in unq_cntry_vals:
    tile_stats_lut[val] = dict()
    tile_stats_lut[val]['count'] = 0
    tile_stats_lut[val]['area'] = 0.0
    tile_stats_lut[val]['vals'] = 0.0
    tile_stats_lut[val]['vals_area'] = 0.0
    tile_hist_lut[val] = numpy.zeros((201), dtype=numpy.uint32)

stats_tiles = glob.glob('/home/pete/Documents/gmw_v3_soil_total_carbon/data/out_stats/total_soil_c/tile_stats/*.json')

for stats_tile_file in stats_tiles:
    stats_tile_lut = rsgislib.tools.utils.read_json_to_dict(stats_tile_file)
    
    for val in unq_cntry_vals:
        tile_stats_lut[val]['count'] += stats_tile_lut[val]['count']
        tile_stats_lut[val]['area'] += stats_tile_lut[val]['area']
        tile_stats_lut[val]['vals'] += stats_tile_lut[val]['vals']
        tile_stats_lut[val]['vals_area'] += stats_tile_lut[val]['vals_area']
        tile_hist_lut[val] = tile_hist_lut[val] + numpy.array(stats_tile_lut["hist"], dtype=numpy.uint32)
        glb_hist_data = glb_hist_data + numpy.array(stats_tile_lut["hist"], dtype=numpy.uint32)




out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['c_total'] = list()
out_data['c_avg'] = list()

for val in unq_cntry_vals:
    if tile_stats_lut[val]['count'] > 0:
        cntry_code = country_ids_lut['val'][val]
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['Country_Code'].append(cntry_code)
        out_data['c_total'].append(tile_stats_lut[val]['vals_area'])
        out_data['c_avg'].append(tile_stats_lut[val]['vals']/tile_stats_lut[val]['count'])


rsgislib.tools.utils.write_dict_to_json(tile_stats_lut, 'country_total_soil_c_stats.json')

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_feather("country_total_soil_c_stats.feather")
df_stats.to_csv("country_total_soil_c_stats.csv")
excel_sheet = 'tot_soil_c'
xls_writer = pandas.ExcelWriter("country_total_soil_c_stats.xlsx", engine='xlsxwriter')
df_stats.to_excel(xls_writer, sheet_name=excel_sheet)
xls_writer.save()

rsgislib.tools.utils.write_dict_to_json(tile_hist_lut, "country_total_soil_c_hists.json")

hist_bins = numpy.arange(0, 5025, 25)
glb_hist_data_dict = dict()
for i in range(201):
    glb_hist_data_dict[f"{hist_bins[i]}"] = [glb_hist_data[i]]

df_hist_stats = pandas.DataFrame.from_dict(glb_hist_data_dict)
xlsx_writer = pandas.ExcelWriter("glb_total_soil_c_hist.xlsx", engine='xlsxwriter')
df_hist_stats.to_excel(xlsx_writer, sheet_name='tot_soil_c_hist')
xlsx_writer.save()
