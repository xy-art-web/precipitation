# Process

## Tools

I used Gemini as an AI coding collaborator to assist with data processing, geographic projection calculations, and script generation. Specifically, Gemini helped implement the custom Albers Equal Area Conic projection formula (`albers_projection()`) in Python using NumPy, set up Matplotlib's `hexbin()` visualization, overlay geographic latitude/longitude gridlines, and draft initial project documentation.

## Kept

I kept the hexagonal binning (`hexbin()`) spatial aggregation method using a custom purple-to-blue colormap. Initially, plotting over 4,600 individual store locations as scatter points caused severe overplotting and visual clutter in densely populated metropolitan areas. Switching to hexagonal grid cells clearly highlights national store density corridors and regional retail concentrations while preserving background map readability.

## Rejected

I rejected rendering raw latitude and longitude coordinates directly on a standard rectangular grid. Unprojected geographic coordinates resulted in significant visual distortion, stretching northern states horizontally and misrepresenting spatial density across different latitudes. I replaced it with the Albers Equal Area Conic projection (`lat_1=29.5`, `lat_2=45.5`) to preserve accurate area proportions across the continental United States. Additionally, I rejected an earlier documentation draft that omitted what data was lost during visualization, explicitly adding that hexagonal binning sacrifices individual store locations in exchange for density clarity.
