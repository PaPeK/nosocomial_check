# Goal

* Get an overview of nosocomial infections from a review study.

* [x] transform the table in the pdf file in ./data/pone.0274248.s001.pdf into a csv_file called ./data/pone_review_S1_table.csv
* [x] create an interactive visualization via observable framework
  * Plot1: all nosokomial infections are displayed on a plot with x-axis=time, y-axis=prevalence (total_cases/ sample_size)
    * when hovering over the points you see [country, study the data is based on]
  * Plot2: same plot as Plot1 but with a dropdown menu, that lets you select the countries that you want to displayed
    * additionally, all countries that are selected, are listed and when clicking on them, they are removed from selection

# Setup

* the python dependencies are managed via "uv" package manager ("uv run", "uv add", ...)
* the observable framework is set up in nosok_framework
  * it contains currently some sample files that needs adjustment

# General Directives

* use mainly python to perform the computation

# Planned Implementation

* [x] Extract and validate the review table from the PDF, then save normalized study records to `data/pone_review_S1_table.csv`.
* [x] Replace the Observable sample content with a reusable data loader and prevalence calculation (`infected_cases / sample_size`).
* [x] Build the full time-versus-prevalence scatter plot with country and study details in point tooltips.
* [x] Add a country multi-select view with removable selected-country chips and filtered plot data.
* [x] Verify the CSV and both interactive views locally.
