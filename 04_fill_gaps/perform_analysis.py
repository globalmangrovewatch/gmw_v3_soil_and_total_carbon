from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)

class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('gmw', self.params["gmw_tile"], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('soc', self.params["soc_img"], 1))

        exp = "gmw==1?soc>0?soc:{}:0".format(self.params["fill_val"])
        print(exp)

        rsgislib.imagecalc.band_math(self.params["out_img"], exp, 'KEA', rsgislib.TYPE_16UINT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params["out_img"], use_no_data=True, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["soc_img", "gmw_tile", "fill_val", "out_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
