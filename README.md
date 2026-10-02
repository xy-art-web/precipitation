# Walmart Store Density in the U.S.

Walmart is the largest retail chain in the United States, but its spatial footprint is far from evenly distributed. This repository processes thousands of store location coordinates across the contiguous United States, maps them using an Albers Equal Area projection, and generates a hexagonal binning density map to reveal how Walmart dominates specific geographic corridors.

It is the submission for Assignment 2: one published dataset of geographical points, one high-density thematic visualization, and every data processing step documented.

![Walmart Store Density Map](out/walmart_map_final.png)

## The phenomenon

From its historical origins in Bentonville, Arkansas, Walmart's expansion pattern shows an intense concentration throughout the American South, Midwest, and Eastern Seaboard. Rather than spreading uniformly, stores cluster heavily along major interstate highways and around sprawling suburban hubs, while leaving vast, sparse gaps across the mountainous West.

The visualization captures this national retail landscape in a single view:
* **Hexagonal Binning**: Aggregates nearby store coordinates into hexagonal grids, preventing overplotting and visually emphasizing high-density retail clusters.
* **Equal Area Projection**: Uses the Albers Equal Area Conic projection to ensure landmasses and store densities are rendered without latitude distortion.
* **Geographic Graticules**: Overlays precise latitude and longitude gridlines to provide clear spatial reference points across the map.
* **Inset Sub-maps**: Alaska (AK) and Hawaii (HI) are clearly outlined in the bottom-left corner to complete the 50-state geographical context.

## The source

The raw dataset comes from store location records containing store name, city, state, latitude (`lat`), and longitude (`lng`).

* **Raw Data File**: `data/walmart.csv`
* **Total Records Analyzed**: Over 4,600+ store coordinates across mainland US.

## Code structure

The complete data pipeline is contained in a single standalone Python script `us_states_heatmap.py`:

* `albers_projection(lon, lat)` converts geographic coordinates (longitude/latitude) into planar coordinates using the Albers Equal Area formula.
* `hexbin(...)` aggregates coordinates into standard hexagonal grid cells and maps store counts to a purple-to-blue color scale.
* `plot(...)` draws state boundaries, Alaska/Hawaii insets, and curvature-aligned latitude/longitude gridlines (`25°N` to `50°N`, `120°W` to `70°W`).

The script declares its own dependencies inline, requiring no manual environment configuration.

## How to run it

Run the script directly using `uv`:

```bash
uv run us_states_heatmap.py
