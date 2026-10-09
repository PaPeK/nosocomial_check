# Nosocomial infections overview

An interactive [Observable Framework](https://observablehq.com/framework/) dashboard for the study-level data in the review's Supplementary Table S1. It plots each study's infection prevalence over time and supports filtering by country.

## Project files

```text
data/
  pone.0274248.s001.pdf          Source supplementary table
  pone_review_S1_table.csv       Extracted study-level dataset
extract_review_table.py          Reproducible PDF-to-CSV extraction command
main.py                          Alias for the extraction command
nosok_framework/
  src/index.md                   Dashboard page and two plots
  src/data/pone_review_S1_table.csv.js
                                 Loader that makes the root CSV available to Observable
  src/components/country-selector.js
                                 Country dropdown and removable selection chips
  package.json                   Observable Framework scripts and JavaScript dependencies
pyproject.toml                   Python project configuration for uv
TODO.md                          Project goals and implementation status
```

The CSV columns are `study`, `sample_size`, `infected_cases`, `prevalence`, `country`, `who_region`, and `year`. Prevalence is calculated as `infected_cases / sample_size`.

## Installation

You need Python 3.10 or newer, [uv](https://docs.astral.sh/uv/), Node.js 18 or newer, npm, and Poppler's `pdftotext` command.

On macOS with Homebrew:

```sh
brew install uv poppler node
```

On Debian/Ubuntu:

```sh
sudo apt install poppler-utils nodejs npm
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install the dashboard's JavaScript dependencies:

```sh
cd nosok_framework
npm install
```

## Refresh the dataset

From the repository root, regenerate the CSV from the supplied PDF:

```sh
uv run python extract_review_table.py
```

`main.py` provides the same command:

```sh
uv run python main.py
```

The extractor checks that every record has a valid year and no more infected cases than participants before it writes the CSV.

## Run the visualization

Start the Observable development server:

```sh
cd nosok_framework
npm run dev
```

Open the local address printed by the command (normally <http://localhost:3000>). The page contains:

1. An all-studies scatter plot with year on the x-axis and prevalence on the y-axis. Hovering a point reveals its country and study.
2. A country-filtered scatter plot. Use the dropdown to add countries; click a country chip to remove it. With no countries selected, the plot is empty.

To produce a static build instead of running the development server:

```sh
cd nosok_framework
npm run build
```

The generated site is written to `nosok_framework/dist/`.

## Data note

The 400 extracted records sum to 29,159,630 participants, matching the total printed in the PDF. Their infected-case sum is 555,997, while the PDF's final aggregate states 555,995; the CSV preserves the individual table rows unchanged.
