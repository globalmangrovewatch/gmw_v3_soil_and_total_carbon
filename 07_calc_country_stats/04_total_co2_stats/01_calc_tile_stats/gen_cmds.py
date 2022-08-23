from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob

import rsgislib.tools.filetools
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class GenTaskCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        carbon_tiles = glob.glob(kwargs['carbon_tiles'])
        for carbon_tile in carbon_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(carbon_tile).replace("_total_co2_2018_2020", "")
            cntry_img = os.path.join(kwargs['cntry_uid_dir'], "{}_cnty.kea".format(tile_base_name))
            pxl_area_img = os.path.join(kwargs['pxl_area_dir'], "{}_pxl_area.kea".format(tile_base_name))
            gmw_ext_img = os.path.join(kwargs['gmw_ext_dir'], "{}_gmw_v314_mng_mjr_2020.kea".format(tile_base_name))

            out_file = os.path.join(kwargs['out_path'], "{}_total_co2_stats.json".format(tile_base_name))
            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict['carbon_tile'] = carbon_tile
                c_dict['country_ids_lut_file'] = kwargs['country_ids_lut_file']
                c_dict['cntry_img'] = cntry_img
                c_dict['pxl_area_img'] = pxl_area_img
                c_dict['gmw_ext_img'] = gmw_ext_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(carbon_tiles='/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_total_co2/*.tif',
                              cntry_uid_dir='/home/pete/Documents/gmw_v3_soil_total_carbon/data/countries/srtm_country_extents',
                              country_ids_lut_file='../../country_ids_lut.json',
                              pxl_area_dir='/home/pete/Documents/gmw_v3_soil_total_carbon/data/srtm_pxl_areas',
                              gmw_ext_dir='/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020',
                              out_path='/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/out_stats/total_co2/tile_stats')

        self.pop_params_db()
        self.create_shell_exe(
            run_script="run_exe_analysis.sh",
            cmds_sh_file="cmds_lst.sh",
            n_cores=50,
            db_info_file="pbpt_db_conn_info.json",
            )

if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = "python {}".format(py_script)

    process_tools_mod = "perform_analysis"
    process_tools_cls = "PerformAnalysis"

    create_tools = GenTaskCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./gmw_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
        )
    create_tools.parse_cmds()
