export function countrySelector(countries) {
  const form = document.createElement("form");
  form.className = "country-selector";
  const selected = new Set();

  const select = document.createElement("select");
  select.setAttribute("aria-label", "Add a country");
  select.innerHTML = '<option value="">Add a country…</option>';
  for (const country of countries) {
    const option = document.createElement("option");
    option.value = option.textContent = country;
    select.append(option);
  }

  const chips = document.createElement("div");
  chips.className = "country-chips";
  chips.setAttribute("aria-live", "polite");

  function update() {
    form.value = [...selected];
    chips.replaceChildren(...[...selected].map((country) => {
      const chip = document.createElement("button");
      chip.type = "button";
      chip.className = "country-chip";
      chip.textContent = `${country} ×`;
      chip.setAttribute("aria-label", `Remove ${country}`);
      chip.addEventListener("click", () => {
        selected.delete(country);
        update();
        form.dispatchEvent(new Event("input", {bubbles: true}));
      });
      return chip;
    }));
  }

  select.addEventListener("change", () => {
    if (select.value) selected.add(select.value);
    select.value = "";
    update();
    form.dispatchEvent(new Event("input", {bubbles: true}));
  });

  form.append(select, chips);
  update();
  return form;
}
