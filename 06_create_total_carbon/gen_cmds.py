from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob
import tqdm
import rsgislib.tools.filetools
import rsgislib.tools.utils

logger = logging.getLogger(__name__)


class GenTaskCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs["out_c_path"]):
            os.mkdir(kwargs["out_c_path"])

        if not os.path.exists(kwargs["out_co2_path"]):
            os.mkdir(kwargs["out_co2_path"])

        imgs = glob.glob(kwargs["img_tiles"])
        for img in tqdm.tqdm(imgs):
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile_name = basename.split("_")[0]

            agb_img = os.path.join(kwargs["agb_dir"], f"{tile_name}_agb_gmw_v314_mng_mjr_2020.tif")
            gmw_img = os.path.join(kwargs["gmw_ext_dir"], f"{tile_name}_gmw_v314_mng_mjr_2020.kea")
            out_agc_img = os.path.join(kwargs["out_c_path"], f"{tile_name}_ag_c_gmw_2020.tif")
            out_c_img = os.path.join(kwargs["out_c_path"], f"{tile_name}_total_c_gmw_2020.tif")
            out_co2_img = os.path.join(kwargs["out_co2_path"], f"{tile_name}_total_co2_gmw_2020.tif")

            if not os.path.exists(agb_img):
                raise Exception("AGB tile not available: {}".format(agb_img))

            if not os.path.exists(gmw_img):
                raise Exception("gmw tile not available: {}".format(gmw_img))

            if not os.path.exists(out_agc_img) or not os.path.exists(out_c_img) or not os.path.exists(out_co2_img):
                c_dict = dict()
                c_dict["soc_img"] = img
                c_dict["agb_img"] = agb_img
                c_dict["gmw_img"] = gmw_img
                c_dict["out_agc_img"] = out_agc_img
                c_dict["out_c_img"] = out_c_img
                c_dict["out_co2_img"] = out_co2_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            img_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/soc_0_100m_gmw_tiles_filled/*.tif",
            agb_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/agb_mng_mjr_2020_tif",
            gmw_ext_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020",
            out_ag_c_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_ag_c",
            out_c_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_total_c",
            out_co2_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/total_carbon_tiles/gmw_2020_total_co2",
        )

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
