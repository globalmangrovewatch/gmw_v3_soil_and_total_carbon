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

        rsgislib.imagecalc.image_math(self.params["agb_img"], self.params["out_agc_img"], "b1*0.451", 'GTIFF', rsgislib.TYPE_32FLOAT)
        rsgislib.imageutils.pop_img_stats(self.params["out_agc_img"], use_no_data=True, no_data_val=0, calc_pyramids=True)

        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('soc', self.params["soc_img"], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('agc', self.params["out_agc_img"], 1))
        rsgislib.imagecalc.band_math(self.params["out_c_img"], "soc+agc", 'GTIFF', rsgislib.TYPE_32FLOAT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params["out_c_img"], use_no_data=True, no_data_val=0, calc_pyramids=True)

        rsgislib.imagecalc.image_math(self.params["out_c_img"], self.params["out_co2_img"], "b1*3.67", 'GTIFF', rsgislib.TYPE_32FLOAT)
        rsgislib.imageutils.pop_img_stats(self.params["out_co2_img"], use_no_data=True, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["soc_img", "agb_img", "gmw_img", "out_agc_img", "out_c_img", "out_co2_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_agc_img"]] = {
            "type":         "gdal_image",
            "n_bands":      1,
            "chk_proj":     True,
            "epsg_code":    4326,
            "read_img":     True,
            "calc_chk_sum": True,
            }

        files_dict[self.params["out_c_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        files_dict[self.params["out_c_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_agc_img"]):
            os.remove(self.params["out_agc_img"])

        if os.path.exists(self.params["out_c_img"]):
            os.remove(self.params["out_c_img"])

        if os.path.exists(self.params["out_co2_img"]):
            os.remove(self.params["out_co2_img"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
