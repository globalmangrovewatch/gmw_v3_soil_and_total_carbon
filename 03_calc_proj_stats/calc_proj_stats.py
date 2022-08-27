import os
import rsgislib.tools.utils

gmw_tile_stats_0_100 = "/home/pete/Documents/gmw_v3_soil_total_carbon/data/gmw_v2_soil_carbon_data/soc_0_100m_gmw_tiles_stats"

gmw_proj_lut_file = "../00_base_info/gmw_srtm_projects_luts.json"
gmw_proj_lut = rsgislib.tools.utils.read_json_to_dict(gmw_proj_lut_file)

gmw_proj_stats = dict()

top_lvl_0_100_stats = dict()

for gmw_proj in gmw_proj_lut:
    top_lvl_proj = gmw_proj.split("-")[1]
    if top_lvl_proj not in top_lvl_0_100_stats:
        top_lvl_0_100_stats[top_lvl_proj] = dict()
        top_lvl_0_100_stats[top_lvl_proj]["sum"] = 0
        top_lvl_0_100_stats[top_lvl_proj]["count"] = 0

overall_0_100_stats = dict()
overall_0_100_stats["sum"] = 0
overall_0_100_stats["count"] = 0
for gmw_proj in gmw_proj_lut:
    top_lvl_proj = gmw_proj.split("-")[1]

    proj_0_100_stats = dict()
    proj_0_100_stats["sum"] = 0
    proj_0_100_stats["count"] = 0

    for gmw_tile in gmw_proj_lut[gmw_proj]:
        gmw_tile_stats_0_100_file = os.path.join(gmw_tile_stats_0_100, f"{gmw_tile}_soc_0_100cm_stats.json")
        if os.path.exists(gmw_tile_stats_0_100_file):
            gmw_tile_stats_0_100_stats = rsgislib.tools.utils.read_json_to_dict(gmw_tile_stats_0_100_file)
            proj_0_100_stats["sum"] += gmw_tile_stats_0_100_stats["sum"]
            proj_0_100_stats["count"] += gmw_tile_stats_0_100_stats["count"]
            top_lvl_0_100_stats[top_lvl_proj]["sum"] += gmw_tile_stats_0_100_stats["sum"]
            top_lvl_0_100_stats[top_lvl_proj]["count"] += gmw_tile_stats_0_100_stats["count"]
            overall_0_100_stats["sum"] += gmw_tile_stats_0_100_stats["sum"]
            overall_0_100_stats["count"] += gmw_tile_stats_0_100_stats["count"]

    if proj_0_100_stats["sum"] > 0:
        proj_0_100_stats["avg"] = proj_0_100_stats["sum"] / proj_0_100_stats["count"]
    else:
        proj_0_100_stats["avg"] = 0.0

    gmw_proj_stats[gmw_proj] = dict()
    gmw_proj_stats[gmw_proj]["0_100"] = proj_0_100_stats

for gmw_proj in gmw_proj_lut:
    top_lvl_proj = gmw_proj.split("-")[1]

    if top_lvl_0_100_stats[top_lvl_proj]["count"] > 0:
        top_lvl_0_100_stats[top_lvl_proj]["avg"] = top_lvl_0_100_stats[top_lvl_proj]["sum"] /top_lvl_0_100_stats[top_lvl_proj]["count"]

overall_0_100_stats["avg"] = overall_0_100_stats["sum"] /overall_0_100_stats["count"]


top_lvl_stats = {"0_100": top_lvl_0_100_stats}
overall_lvl_stats = {"0_100": overall_0_100_stats}

rsgislib.tools.utils.write_dict_to_json(gmw_proj_stats, "gmw_v3_proj_stats.json")
rsgislib.tools.utils.write_dict_to_json(top_lvl_stats, "gmw_v3_proj_top_lvl_stats.json")
rsgislib.tools.utils.write_dict_to_json(overall_lvl_stats, "gmw_v3_overall_stats.json")
