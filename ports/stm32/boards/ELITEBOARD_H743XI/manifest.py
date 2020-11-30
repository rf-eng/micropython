include("$(PORT_DIR)/boards/manifest.py")
freeze("$(MPY_DIR)/extmod/upyscripts_eliteboard/adafruit_drivers/lib")
freeze("$(MPY_DIR)/extmod/upyscripts_eliteboard/adafruit_drivers", ("adafruit_hts221.py", "adafruit_lis3mdl.py", "adafruit_lps2x.py", "adafruit_lsm6ds.py"))