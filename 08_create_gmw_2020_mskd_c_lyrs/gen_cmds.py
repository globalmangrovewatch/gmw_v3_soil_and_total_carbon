import logging
import os
import glob
import rsgislib.tools.filetools

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        imgs = glob.glob(kwargs['input_imgs'])
        for img in imgs:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(img).replace(kwargs['base_rm'], "")
            gmw_ext_img = os.path.join(kwargs['gmw_ext_dir'], f"{tile_base_name}_gmw_v314_mng_mjr_2020.kea")
            out_img = os.path.join(kwargs['gmw_ext_dir'], f"{tile_base_name}{kwargs['out_name']}.kea")
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["img"] = img
                c_dict["gmw_ext"] = gmw_ext_img
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(input_imgs="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/soc_0_100m_gmw_tiles_filled/*.kea",
                              base_rm="_soc_0_100cm_fill",
                              out_name="_soil_c",
                              gmw_ext_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020",
                              out_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/202302_fnl_2020_rasters/kea/soil_c")

        self.gen_command_info(input_imgs="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_total_c/*.kea",
                              base_rm="_total_c_gmw_2020",
                              out_name="_total_c",
                              gmw_ext_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020",
                              out_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/202302_fnl_2020_rasters/kea/total_c")

        self.gen_command_info(input_imgs="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_total_co2/*.kea",
                              base_rm="_total_co2_gmw_2020",
                              out_name="_total_co2",
                              gmw_ext_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020",
                              out_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/202302_fnl_2020_rasters/kea/total_co2")

        self.gen_command_info(input_imgs="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/total_carbon_tiles/gmw_2020_ag_c/*.kea",
                              base_rm="_ag_c_gmw_2020",
                              out_name="_abv_grd_c",
                              gmw_ext_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/mng_mjr_2020",
                              out_dir="/home/pete/Documents/gmw_v3_soil_total_carbon/data/202302_fnl_2020_rasters/kea/abv_grd_c")

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=25,  # The number of cores to use for analysis.
            db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "ProcessCmd"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./pbpt_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()

