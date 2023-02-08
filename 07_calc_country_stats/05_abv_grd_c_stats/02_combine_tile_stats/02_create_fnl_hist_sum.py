import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_agb_stats_file = 'country_abv_grd_c_hists.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)


out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['0-700'] = list()
out_data['700-1400'] = list()
out_data['1400-2100'] = list()
out_data['2100-2800'] = list()
out_data['2800-3500'] = list()
out_data['3500-'] = list()


for cntry_id in country_ids_lut["val"].keys():
    country_c_arr = numpy.array(country_agb_stats_lut[cntry_id], dtype=numpy.uint32)
    tot_country_c = numpy.sum(country_c_arr)
    if tot_country_c > 0:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['0-700'].append(numpy.sum(country_c_arr[0:28]) / tot_country_c)
        out_data['700-1400'].append(numpy.sum(country_c_arr[28:56]) / tot_country_c)
        out_data['1400-2100'].append(numpy.sum(country_c_arr[56:84]) / tot_country_c)
        out_data['2100-2800'].append(numpy.sum(country_c_arr[84:112]) / tot_country_c)
        out_data['2800-3500'].append(numpy.sum(country_c_arr[112:140]) / tot_country_c)
        out_data['3500-'].append(numpy.sum(country_c_arr[140:]) / tot_country_c)

df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("country_total_co2_hists_summary.csv")
df_stats.to_feather("country_total_co2_hists_summary.feather")
xlsx_writer = pandas.ExcelWriter("country_total_co2_hists_summary.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='tot_c_hist')
xlsx_writer.close()
