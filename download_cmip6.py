import cdsapi
import os
import time

c = cdsapi.Client()

models = ["canesm5", "access_cm2", "mpi_esm1_2_lr"]
scenarios = ["historical", "ssp245", "ssp585"]
variables = ["eastward_near_surface_wind", "northward_near_surface_wind"]

output_dir = "cmip6_wind_data"
os.makedirs(output_dir, exist_ok=True)

def download_file(model, scenario, var, year):
    # Short name for file
    v_short = "u" if "eastward" in var else "v"
    file_name = f"{model}_{scenario}_{v_short}_{year}.zip"
    file_path = os.path.join(output_dir, file_name)

    if os.path.exists(file_path):
        return

    print(f">>> Pulling: {model} | {scenario} | {v_short} | {year}")

    try:
        c.retrieve(
            "projections-cmip6",
            {
                "format": "zip",
                "temporal_resolution": "monthly",
                "experiment_id": scenario,
                "variable": var, # ONLY ONE VARIABLE
                "model": model,
                "member_id": "r1i1p1f1",
                "year": str(year), # ONLY ONE YEAR
                "month": [f"{m:02d}" for m in range(1, 13)]
            },
            file_path)
    except Exception as e:
        print(f"ERROR on {file_name}: {e}")

# Triple loop: Model -> Scenario -> Year
for model in models:
    for scenario in scenarios:
        start, end = (1990, 2015) if scenario == "historical" else (2015, 2051)
        for year in range(start, end):
            for var in variables:
                download_file(model, scenario, var, year)
                time.sleep(2) # Short gap