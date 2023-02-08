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

        imgs = glob.glob(kwargs["img_tiles"])
        for img in imgs:
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile_name = basename.split("_")[0]
            out_file = os.path.join(kwargs["out_path"], f"{basename}_stats.json")

            gmw_tile = os.path.join(kwargs["gmw_ext"], f"{tile_name}_gmw_union.kea")
            if not os.path.exists(gmw_tile):
                raise Exception("GMW Tile now available: {}".format(gmw_tile))

            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict["tile_img"] = img
                c_dict["gmw_tile"] = gmw_tile
                c_dict["out_file"] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            img_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/soc_0_100m_gmw_tiles/*.kea",
            gmw_ext="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/gmw_union_srtm_rasters",
            out_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/soc_0_100m_gmw_tiles_stats",
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
