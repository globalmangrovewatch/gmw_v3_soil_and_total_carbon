from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob

import rsgislib.tools.filetools

logger = logging.getLogger(__name__)


class GenTaskCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs["out_path"]):
            os.mkdir(kwargs["out_path"])

        imgs = glob.glob(kwargs["ref_tiles"])
        for img in imgs:
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile_name = basename.split("_")[0]
            out_img = os.path.join(kwargs["out_path"], f"{tile_name}{kwargs['out_img_name']}.kea")

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["tile_img"] = img
                c_dict["vals_img"] = kwargs['soil_c_img']
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            ref_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/agb_mng_mjr_2020_tif/*.tif",
            soil_c_img="/home/pete/Documents/gmw_v3_soil_total_carbon/data/base_soil_data/sol_soc.tha_mangroves.typology_m_30m_s30..100cm_2018..2020_global_v0.1.tif",
            out_img_name="_soil_30_100cm_2018_2020",
            out_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soil_carbon_tiles/2018_2020_30cm_100cm",
        )

        self.gen_command_info(
            ref_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/agb_mng_mjr_2020_tif/*.tif",
            soil_c_img="/home/pete/Documents/gmw_v3_soil_total_carbon/data/base_soil_data/sol_soc.tha_mangroves.typology_m_30m_s0..30cm_2018..2020_global_v0.1.tif",
            out_img_name="_soil_0_30cm_2018_2020",
            out_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soil_carbon_tiles/2018_2020_0cm_30cm",
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
