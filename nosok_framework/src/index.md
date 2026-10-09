---
toc: false
---

```js
import {countrySelector} from "./components/country-selector.js";

const studies = (await FileAttachment("data/pone_review_S1_table.csv").csv({typed: true}))
  .map((study, index) => ({
    ...study,
    id: index,
    year: +study.year,
    prevalence: +study.prevalence
  }));
const countries = [...new Set(studies.map((study) => study.country))].sort();
const studyTooltip = (study) => [
  `Study: ${study.study}`,
  `Country: ${study.country}`,
  `WHO region: ${study.who_region}`,
  `Year: ${study.year}`,
  `Prevalence: ${d3.format(".1%")(study.prevalence)}`,
  `Infected cases: ${d3.format(",")(study.infected_cases)} of ${d3.format(",")(study.sample_size)}`
].join("\n");
const summary = {
  studies: studies.length,
  countries: countries.length,
  sampleSize: d3.sum(studies, (study) => study.sample_size),
  infectedCases: d3.sum(studies, (study) => study.infected_cases)
};
```

# Nosocomial infections overview

This dashboard visualizes the individual studies reported in Supplementary Table S1 of the review. Prevalence is calculated as infected cases divided by total sample size.

<div class="grid grid-cols-4">
  <div class="card"><span class="metric">${summary.studies}</span><br>study records</div>
  <div class="card"><span class="metric">${summary.countries}</span><br>countries or study locations</div>
  <div class="card"><span class="metric">${d3.format(",")(summary.sampleSize)}</span><br>participants</div>
  <div class="card"><span class="metric">${d3.format(",")(summary.infectedCases)}</span><br>infected cases</div>
</div>

## All studies

Each of the ${summary.studies} points represents one study record. Hover over a point to see its country and study citation.

<div class="card">${resize((width) => Plot.plot({
  width,
  height: 460,
  marginLeft: 56,
  grid: true,
  x: {label: "Study year", domain: [1999.5, 2021.5], tickFormat: d3.format("d")},
  y: {label: "Prevalence", percent: false, domain: [0, 1]},
  color: {legend: true, label: "WHO region"},
  marks: [
    Plot.dot(studies, {
      x: "year", y: "prevalence", fill: "who_region", r: 4, opacity: 0.72,
      title: studyTooltip, tip: true
    }),
    Plot.ruleY([0])
  ]
}))}</div>

## Compare selected countries

Use the dropdown to add one or more countries. Click a country chip to remove it. The plot remains empty until a country is selected.

```js
const selectedCountries = view(countrySelector(countries));
```

```js
const showMeanLines = view(Inputs.button("Show / hide country means", {
  value: false,
  reduce: (visible) => !visible
}));
```

```js
const filteredStudies = studies.filter((study) => selectedCountries.includes(study.country));
const countryMeans = d3.rollups(
  filteredStudies,
  (countryStudies) => d3.mean(countryStudies, (study) => study.prevalence),
  (study) => study.country
).map(([country, prevalence]) => ({country, prevalence}));
```

<div class="card">${resize((width) => Plot.plot({
  width,
  height: 460,
  marginLeft: 56,
  grid: true,
  x: {label: "Study year", domain: [1999.5, 2021.5], tickFormat: d3.format("d")},
  y: {label: "Prevalence", percent: false, domain: [0, 1]},
  color: {legend: true, label: "Country"},
  marks: [
    Plot.dot(filteredStudies, {
      x: "year", y: "prevalence", fill: "country", r: 5, opacity: 0.8,
      title: studyTooltip, tip: true
    }),
    ...(showMeanLines ? [Plot.ruleY(countryMeans, {
      y: "prevalence", stroke: "country", strokeWidth: 2, opacity: 0.85,
      title: (mean) => `${mean.country} mean prevalence: ${d3.format(".1%")(mean.prevalence)}`,
      tip: true
    })] : []),
    Plot.ruleY([0])
  ]
}))}</div>

<p class="source-note">Source: extracted from <code>pone.0274248.s001.pdf</code>. The 400 extracted rows sum to 29,159,630 participants, matching the PDF total. Their infected-case sum is 555,997; the PDF’s final aggregate reports 555,995.</p>

<style>
.metric { font-size: 1.8rem; font-weight: 700; }
.country-selector { display: grid; gap: 0.75rem; margin: 1rem 0; }
.country-selector select { max-width: 22rem; padding: 0.45rem; }
.country-chips { display: flex; flex-wrap: wrap; gap: 0.45rem; }
.country-chip { border: 1px solid var(--theme-foreground-focus); border-radius: 999px; background: var(--theme-background-alt); color: var(--theme-foreground); cursor: pointer; padding: 0.3rem 0.6rem; }
.source-note { color: var(--theme-foreground-muted); font-size: 0.9rem; }
</style>
