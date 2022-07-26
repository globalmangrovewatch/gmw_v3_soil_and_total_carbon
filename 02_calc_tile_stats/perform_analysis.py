from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.tools.utils

import numpy
import osgeo.gdal as gdal

logger = logging.getLogger(__name__)

def calc_stats(vals_img, gmw_img):
    img_vals_ds = gdal.Open(vals_img)
    if img_vals_ds is None:
        raise Exception("Could not open the values input image: '{}'".format(uid_img))
    img_vals_band = img_vals_ds.GetRasterBand(1)
    if img_vals_band is None:
        raise Exception("Failed to read the values image band: '{}'".format(uid_img))
    vals_arr = img_vals_band.ReadAsArray()
    img_vals_ds = None

    img_gmw_ds = gdal.Open(gmw_img)
    if img_gmw_ds is None:
        raise Exception("Could not open the GMW input image: '{}'".format(gmw_img))
    img_gmw_band = img_gmw_ds.GetRasterBand(1)
    if img_gmw_band is None:
        raise Exception("Failed to read the GMW image band: '{}'".format(gmw_img))
    gmw_arr = img_gmw_band.ReadAsArray()
    img_gmw_ds = None

    msk = numpy.zeros_like(gmw_arr, dtype=bool)
    msk[(vals_arr > 0) & (gmw_arr == 1)] = True

    val_stats_lut = dict()
    val_stats_lut['count'] = numpy.sum(msk)
    val_stats_lut['sum'] = numpy.sum(vals_arr[msk])

    return val_stats_lut

class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        stats_lut = calc_stats(self.params["tile_img"], self.params["gmw_tile"])

        if stats_lut['count'] > 0:
            stats_lut["avg"] = stats_lut['sum'] / stats_lut['count']
        else:
            stats_lut["avg"] = 0.0

        rsgislib.tools.utils.write_dict_to_json(stats_lut, self.params["out_file"])

    def required_fields(self, **kwargs):
        return ["tile_img", "gmw_tile", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = "file"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
