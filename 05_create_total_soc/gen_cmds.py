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
        if not os.path.exists(kwargs["out_path"]):
            os.mkdir(kwargs["out_path"])

        imgs = glob.glob(kwargs["img_low_tiles"])
        for img in tqdm.tqdm(imgs):
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile_name = basename.split("_")[0]

            upper_img = os.path.join(kwargs["img_up_dir"], f"{tile_name}_soil_30_100cm_2018_2020_fill.tif")
            out_img = os.path.join(kwargs["out_path"], f"{tile_name}_total_soil_2018_2020.tif")

            if not os.path.exists(upper_img):
                raise Exception("Upper tile not available: {}".format(upper_img))

            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["low_soc_img"] = img
                c_dict["up_soc_img"] = upper_img
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            img_low_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soil_carbon_tiles/2018_2020_0cm_30cm_filled/*.tif",
            img_up_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soil_carbon_tiles/2018_2020_30cm_100cm_filled/",
            out_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soil_carbon_tiles/2018_2020_total_soc",
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
