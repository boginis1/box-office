# Box Office

Mini hotel revenue-management simulator for group booking decisions.

## What it does

The simulator presents realistic group booking scenarios (including each hotel's
current occupancy and ADR pace) and asks:

**To Take or Not Take?**

After each user response, it reveals a displacement analysis, recommendation,
and a plain-language explanation of why the decision was right or wrong.

## Run (web page)

Open `index.html` in your browser, or serve locally:

```bash
python3 -m http.server 8000
```

Then visit `http://localhost:8000`.

## Run (CLI)

```bash
python3 simulator.py
```

## Decision logic

For each scenario, the simulator compares:

- **Group contribution** = `(Group ADR + Ancillary - Variable Cost) × Group Room Nights - Meeting Space Cost`
- **Displaced transient contribution** = `(Transient ADR - Variable Cost) × Displaced Room Nights`

If group contribution is greater than or equal to displaced transient contribution,
it recommends **TAKE**. Otherwise, it recommends **DO NOT TAKE**.
