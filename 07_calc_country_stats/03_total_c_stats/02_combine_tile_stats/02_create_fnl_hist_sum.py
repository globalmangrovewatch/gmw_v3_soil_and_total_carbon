import rsgislib.tools.utils
import pandas
import numpy

country_ids_lut_file='../../country_ids_lut.json'
country_ids_lut = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)

gadm_lut_file ='../../gadm_lut.json'
gadm_lut = rsgislib.tools.utils.read_json_to_dict(gadm_lut_file)

country_agb_stats_file = 'country_total_c_hists.json'
country_agb_stats_lut = rsgislib.tools.utils.read_json_to_dict(country_agb_stats_file)


out_data = dict()
out_data['Country'] = list()
out_data['Country_Code'] = list()
out_data['0-250'] = list()
out_data['250-500'] = list()
out_data['500-750'] = list()
out_data['750-1000'] = list()
out_data['1000-1250'] = list()
out_data['1250-'] = list()


for cntry_id in country_ids_lut["val"].keys():
    country_c_arr = numpy.array(country_agb_stats_lut[cntry_id], dtype=numpy.uint32)
    tot_country_c = numpy.sum(country_c_arr)
    if tot_country_c > 0:
        cntry_code = country_ids_lut['val'][cntry_id]
        out_data['Country_Code'].append(cntry_code)
        out_data['Country'].append(gadm_lut['gid'][cntry_code])
        out_data['0-250'].append(numpy.sum(country_c_arr[0:10])/tot_country_c)
        out_data['250-500'].append(numpy.sum(country_c_arr[10:20])/tot_country_c)
        out_data['500-750'].append(numpy.sum(country_c_arr[20:30])/tot_country_c)
        out_data['750-1000'].append(numpy.sum(country_c_arr[30:40])/tot_country_c)
        out_data['1000-1250'].append(numpy.sum(country_c_arr[40:50])/tot_country_c)
        out_data['1250-'].append(numpy.sum(country_c_arr[50:])/tot_country_c)



df_stats = pandas.DataFrame.from_dict(out_data)
df_stats.to_csv("country_total_c_hists_summary.csv")
df_stats.to_feather("country_total_c_hists_summary.feather")
xlsx_writer = pandas.ExcelWriter("country_total_c_hists_summary.xlsx", engine='xlsxwriter')
df_stats.to_excel(xlsx_writer, sheet_name='tot_c_hist')
xlsx_writer.close()
