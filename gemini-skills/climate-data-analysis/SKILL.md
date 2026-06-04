---
name: climate-data-analysis
description: Climate and Earth system data analysis using xarray, cartopy, cfgrib, and CMIP6/ERA5 datasets. Use for loading NetCDF/GRIB climate data, computing climatologies, spatial aggregation, anomaly detection, bias correction, and publication-quality climate maps. Best for atmospheric, oceanic, and land surface data analysis.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# Climate Data Analysis

## Overview

Climate data analysis involves working with large multi-dimensional gridded datasets from reanalyses (ERA5, MERRA-2), climate model outputs (CMIP6), observational datasets (GPCC, GHCN), and satellite products. This skill covers the complete workflow from data access to publication-quality visualization.

## When to Use This Skill

- Loading and processing NetCDF or GRIB climate datasets
- Computing climatologies, anomalies, and trends
- Spatial and temporal aggregation of climate variables
- Creating climate maps with proper projections (cartopy)
- Accessing CMIP6 model outputs and ERA5 reanalysis data
- Bias correction of climate model outputs
- Calculating climate indices (ENSO, NAO, drought indices)
- Downscaling or regridding climate data

## Quick Start

### Loading Climate Data with xarray

```python
import xarray as xr
import numpy as np

# Load a NetCDF file
ds = xr.open_dataset("era5_temperature_2020.nc")
print(ds)

# Select a variable and time slice
t2m = ds["t2m"]  # 2m temperature in Kelvin
t2m_celsius = t2m - 273.15  # Convert to Celsius

# Compute annual mean
annual_mean = t2m_celsius.groupby("time.year").mean("time")

# Spatial subset (Europe)
europe = t2m_celsius.sel(
    latitude=slice(75, 35),
    longitude=slice(-15, 45)
)
print(f"Shape: {europe.shape}")
print(f"Time range: {europe.time.values[0]} to {europe.time.values[-1]}")
```

### Climate Climatology and Anomalies

```python
import xarray as xr
import numpy as np

ds = xr.open_dataset("monthly_temperature.nc")
temp = ds["temperature"]

# Compute 30-year climatology (1991-2020 standard)
clim = temp.sel(time=slice("1991", "2020")).groupby("time.month").mean("time")

# Compute anomalies
anomalies = temp.groupby("time.month") - clim

# Rolling trend (10-year)
trend = anomalies.rolling(time=120, center=True).mean()

print(f"Climatology shape: {clim.shape}")
print(f"Anomaly mean: {float(anomalies.mean()):.4f}")
```

### ERA5 Data Access via CDS API

```python
import cdsapi

client = cdsapi.Client()

# Download ERA5 monthly mean 2m temperature
client.retrieve(
    "reanalysis-era5-single-levels-monthly-means",
    {
        "product_type": "monthly_averaged_reanalysis",
        "variable": ["2m_temperature", "total_precipitation"],
        "year": [str(y) for y in range(2000, 2024)],
        "month": [f"{m:02d}" for m in range(1, 13)],
        "time": "00:00",
        "format": "netcdf",
        "area": [90, -180, -90, 180],  # Global
    },
    "era5_monthly_2000_2023.nc",
)
```

### Climate Maps with Cartopy

```python
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_dataset("temperature_anomaly.nc")
anomaly = ds["t2m_anomaly"].isel(time=0)

fig, ax = plt.subplots(
    figsize=(14, 7),
    subplot_kw={"projection": ccrs.Robinson()}
)

# Plot data
im = anomaly.plot(
    ax=ax,
    transform=ccrs.PlateCarree(),
    cmap="RdBu_r",
    robust=True,
    cbar_kwargs={"label": "Temperature Anomaly (°C)", "shrink": 0.8},
    add_colorbar=True,
)

# Add geographic features
ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
ax.add_feature(cfeature.BORDERS, linewidth=0.3, linestyle="--")
ax.add_feature(cfeature.LAND, facecolor="lightgray", alpha=0.3)
ax.gridlines(draw_labels=True, dms=True, x_inline=False, y_inline=False)

ax.set_title("Global Temperature Anomaly", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("climate_map.png", dpi=200, bbox_inches="tight")
print("Climate map saved.")
```

### CMIP6 Data Access via Pangeo

```python
import intake
import xarray as xr

# Access CMIP6 catalog
catalog = intake.open_esm_datastore(
    "https://storage.googleapis.com/cmip6/pangeo-cmip6.json"
)

# Search for specific model output
cat_subset = catalog.search(
    experiment_id=["historical", "ssp585"],
    table_id="Amon",
    variable_id="tas",
    member_id="r1i1p1f1",
    source_id="CESM2",
)

# Load datasets
dsets = cat_subset.to_dataset_dict(zarr_kwargs={"consolidated": True})
print(list(dsets.keys()))

# Historical temperature
hist = dsets["CMIP.NCAR.CESM2.historical.Amon.gn"]
ssp585 = dsets["ScenarioMIP.NCAR.CESM2.ssp585.Amon.gn"]

# Global mean temperature
global_mean_hist = hist["tas"].mean(["lat", "lon"])
global_mean_ssp585 = ssp585["tas"].mean(["lat", "lon"])
```

### Spatial Statistics

```python
import xarray as xr
import numpy as np

def area_weighted_mean(da: xr.DataArray) -> xr.DataArray:
    """Compute area-weighted spatial mean (accounts for grid cell size)."""
    weights = np.cos(np.deg2rad(da.lat))
    weights.name = "weights"
    return da.weighted(weights).mean(["lat", "lon"])

ds = xr.open_dataset("global_temperature.nc")
temp = ds["temperature"]

# Area-weighted global mean temperature
global_temp = area_weighted_mean(temp)
print(f"Global mean temperature: {float(global_temp.mean()):.2f} K")

# Trend calculation
from scipy import stats
time_num = np.arange(len(global_temp))
slope, intercept, r, p, se = stats.linregress(time_num, global_temp.values)
print(f"Trend: {slope*10:.3f} K/decade (p={p:.4f})")
```

### Climate Indices

```python
import xarray as xr
import numpy as np

def calculate_nino34(sst: xr.DataArray) -> xr.DataArray:
    """Calculate Niño 3.4 index (ENSO indicator)."""
    # Niño 3.4 region: 5°S-5°N, 170°W-120°W
    nino34_region = sst.sel(
        lat=slice(-5, 5),
        lon=slice(190, 240)  # 170W-120W in 0-360 coords
    )
    # Area-weighted mean
    weights = np.cos(np.deg2rad(nino34_region.lat))
    nino34 = nino34_region.weighted(weights).mean(["lat", "lon"])
    # Remove climatology
    clim = nino34.groupby("time.month").mean("time")
    return nino34.groupby("time.month") - clim

def calculate_drought_index(precip: xr.DataArray, window: int = 12) -> xr.DataArray:
    """Simplified SPI (Standardized Precipitation Index)."""
    rolling_precip = precip.rolling(time=window).sum()
    mean = rolling_precip.groupby("time.month").mean("time")
    std = rolling_precip.groupby("time.month").std("time")
    spi = (rolling_precip.groupby("time.month") - mean) / std
    return spi
```

### Regridding with xesmf

```python
import xarray as xr
import xesmf as xe

# Regrid from coarse to fine grid (or vice versa)
ds_coarse = xr.open_dataset("cmip6_model_1deg.nc")
ds_fine = xr.open_dataset("observations_0.25deg.nc")

# Create regridder
regridder = xe.Regridder(ds_coarse, ds_fine, "bilinear")

# Apply regridding
ds_regridded = regridder(ds_coarse)
print(f"Regridded shape: {ds_regridded['tas'].shape}")
```

## Key Datasets

| Dataset | Variable | Resolution | Access |
|---------|----------|-----------|--------|
| ERA5 | All atmospheric vars | 0.25°, hourly | CDS API |
| CMIP6 | Climate model outputs | 1°, monthly | Pangeo/ESGF |
| GPCC | Precipitation | 0.25°, monthly | FTP |
| HadCRUT5 | Temperature | 5°, monthly | UK Met Office |
| MODIS | Land surface | 500m, daily | NASA |

## Dependencies

```bash
pip install xarray netCDF4 cartopy matplotlib scipy
pip install cdsapi  # ERA5 access
pip install intake intake-esm  # CMIP6 catalog
pip install xesmf  # Regridding
conda install -c conda-forge cfgrib eccodes  # GRIB support
```
