from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import numpy
import osgeo.gdal as gdal
import rsgislib.tools.utils

logger = logging.getLogger(__name__)


def calc_unq_val_pxl_areas(vals_img, pix_area_img, uid_img, gmw_img, unq_val_area_lut):
    img_vals_ds = gdal.Open(vals_img)
    if img_vals_ds is None:
        raise Exception("Could not open the values input image: '{}'".format(uid_img))
    img_vals_band = img_vals_ds.GetRasterBand(1)
    if img_vals_band is None:
        raise Exception("Failed to read the values image band: '{}'".format(uid_img))
    vals_arr = img_vals_band.ReadAsArray()
    img_vals_ds = None

    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image: '{}'".format(uid_img))
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band: '{}'".format(uid_img))
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    img_pixarea_ds = gdal.Open(pix_area_img)
    if img_pixarea_ds is None:
        raise Exception("Could not open the pixel area input image: '{}'".format(pix_area_img))
    img_pixarea_band = img_pixarea_ds.GetRasterBand(1)
    if img_pixarea_band is None:
        raise Exception("Failed to read the pixel area image band: '{}'".format(pix_area_img))
    pxl_area_arr = img_pixarea_band.ReadAsArray()
    img_pixarea_ds = None

    img_gmw_ds = gdal.Open(gmw_img)
    if img_gmw_ds is None:
        raise Exception("Could not open the GMW input image: '{}'".format(gmw_img))
    img_gmw_band = img_gmw_ds.GetRasterBand(1)
    if img_gmw_band is None:
        raise Exception("Failed to read the GMW image band: '{}'".format(gmw_img))
    gmw_arr = img_gmw_band.ReadAsArray()
    img_gmw_ds = None

    unq_pix_vals = numpy.unique(uid_arr)

    for unq_val in unq_pix_vals:
        if unq_val != 0:
            msk = numpy.zeros_like(uid_arr, dtype=bool)
            msk[(uid_arr == unq_val) & (uid_arr > 0) & (gmw_arr == 1)] = True

            unq_val_area_lut[unq_val]['count'] = numpy.sum(msk)
            unq_val_area_lut[unq_val]['area'] = numpy.sum(pxl_area_arr[msk])
            unq_val_area_lut[unq_val]['vals'] = numpy.sum(vals_arr[msk])
            unq_val_area_lut[unq_val]['vals_area'] = numpy.sum(vals_arr[msk] * pxl_area_arr[msk])


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):

        unq_vals = rsgislib.tools.utils.read_json_to_dict(self.params['country_ids_lut_file'])["val"].keys()

        tile_stats_lut = dict()

        for val in unq_vals:
            val = int(val)
            tile_stats_lut[val] = dict()
            tile_stats_lut[val]['count'] = 0
            tile_stats_lut[val]['area'] = 0.0
            tile_stats_lut[val]['vals'] = 0.0
            tile_stats_lut[val]['vals_area'] = 0.0

        calc_unq_val_pxl_areas(self.params["carbon_tile"], self.params["pxl_area_img"], self.params["cntry_img"], self.params["gmw_ext_img"], tile_stats_lut)

        for val in unq_vals:
            val = int(val)
            tile_stats_lut[val]['count'] = int(tile_stats_lut[val]['count'])
            tile_stats_lut[val]['area'] = float(tile_stats_lut[val]['area'])
            tile_stats_lut[val]['vals'] = float(tile_stats_lut[val]['vals'])
            tile_stats_lut[val]['vals_area'] = float(tile_stats_lut[val]['vals_area'])

        rsgislib.tools.utils.write_dict_to_json(tile_stats_lut, self.params["out_file"])


    def required_fields(self, **kwargs):
        return ["carbon_tile", "country_ids_lut_file", "cntry_img", "pxl_area_img", "gmw_ext_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = {"type": "file"}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
