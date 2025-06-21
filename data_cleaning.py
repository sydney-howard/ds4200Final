# import libraries
import pandas as pd

# load the data
df = pd.read_csv("co2-emissions-vs-gdp.csv")
region_df = pd.read_csv("ipbes_regions_subregions_1.1.csv") # additional region data

# filter valid years and non-null values
df_filtered = df[
    (df["Year"] >= 1975) &
    (df["Annual CO₂ emissions (per capita)"].notna()) &
    (df["GDP per capita"].notna()) &
    (df["Population (historical)"].notna()) &
    (df["Entity"] != "World")
].copy()

# rename columns for consistency
df_filtered = df_filtered.rename(columns={
    "Entity": "Country",
    "Code": "ISO3",
    "Annual CO₂ emissions (per capita)": "CO2_per_capita",
    "GDP per capita": "GDP_per_capita",
    "Population (historical)": "Population",
    "World regions according to OWID": "Region_OWID"
})

# clean and rename region mapping file
region_df = region_df.rename(columns={
    "ISO_3166_alpha_3": "ISO3",
    "Region": "Region_IPBES",
    "Sub-Region": "Subregion_IPBES"
})

# merge on ISO3 to bring in additional regions
merged_df = pd.merge(
    df_filtered,
    region_df[["ISO3", "Region_IPBES", "Subregion_IPBES"]],
    on="ISO3",
    how="left"
)

# prioritize IPBES regions, fallback to OWID
merged_df["Region"] = merged_df["Region_IPBES"].combine_first(merged_df["Region_OWID"])

# columns
final_df = merged_df[[
    "Year", "Country", "ISO3", "CO2_per_capita", "GDP_per_capita",
    "Population", "Region", "Subregion_IPBES"
]]

# save final csv to be used in vega-lite
final_df.to_csv("gdp_vs_co2.csv", index=False)


