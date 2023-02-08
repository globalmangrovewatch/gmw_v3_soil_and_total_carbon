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

        gmw_proj_tile_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["gmw_prj_lut"])
        gmw_proj_stats_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["gmw_prj_stats"])
        gmw_proj_tp_lvl_stats_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["gmw_prj_tp_lvl_stats"])
        gmw_overall_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["gmw_overall_stats"])

        imgs = glob.glob(kwargs["img_tiles"])
        for img in tqdm.tqdm(imgs):
            basename = rsgislib.tools.filetools.get_file_basename(img)
            tile_name = basename.split("_")[0]
            out_img = os.path.join(kwargs["out_path"], f"{basename}_fill.kea")

            gmw_tile = os.path.join(kwargs["gmw_ext"], f"{tile_name}_gmw_union.kea")
            if not os.path.exists(gmw_tile):
                raise Exception("GMW Tile now available: {}".format(gmw_tile))

            if not os.path.exists(out_img):
                tile_prj = gmw_proj_tile_lut[tile_name]
                tile_avg = float(gmw_proj_stats_lut[tile_prj][kwargs["stats_key"]]["avg"])
                if not (tile_avg > 0.0):
                    top_lvl_proj = tile_prj.split("-")[1]
                    print(top_lvl_proj)
                    tile_avg = float(gmw_proj_tp_lvl_stats_lut[kwargs["stats_key"]][top_lvl_proj]["avg"])
                    print(tile_avg)
                if not (tile_avg > 0.0):
                    tile_avg = float(gmw_overall_lut[kwargs["stats_key"]]["avg"])
                    print("OVERALL: {}".format(tile_avg))

                c_dict = dict()
                c_dict["soc_img"] = img
                c_dict["gmw_tile"] = gmw_tile
                c_dict["fill_val"] = tile_avg
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(
            img_tiles="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/soc_0_100m_gmw_tiles/*.kea",
            gmw_ext="/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v3_extent/gmw_union_srtm_rasters",
            gmw_prj_lut="../00_base_info/gmw_srtm_tiles_luts.json",
            gmw_prj_stats="../03_calc_proj_stats/gmw_v3_proj_stats.json",
            gmw_prj_tp_lvl_stats="../03_calc_proj_stats/gmw_v3_proj_top_lvl_stats.json",
            gmw_overall_stats="../03_calc_proj_stats/gmw_v3_overall_stats.json",
            stats_key="0_100",
            out_path="/home/pete/Documents/gmw_v3_soil_total_carbon/data/soc_20221216/soc_0_100m_gmw_tiles_filled",
        )


        self.pop_params_db()
        self.create_shell_exe(
            run_script="run_exe_analysis.sh",
            cmds_sh_file="cmds_lst.sh",
            n_cores=25,
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
