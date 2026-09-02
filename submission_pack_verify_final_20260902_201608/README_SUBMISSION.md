# Submission pack — Chaos, Solitons & Fractals

This package contains the clean LaTeX source and supporting files for the manuscript
prepared for *Chaos, Solitons & Fractals*.

## Manuscript

- `manuscript/main.tex` — main LaTeX entry point
- `manuscript/sections/` — active manuscript sections
- `manuscript/images/` — figures and the graphical abstract
- `manuscript/references.bib` — bibliography
- `manuscript/cas-sc.cls`, `manuscript/cas-common.sty` — local CAS template files
- `manuscript/main.pdf` — compiled manuscript for visual checking

The source compiles from the `manuscript` directory with:

```text
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

## Additional submission files

- `Highlights.txt` — separate Highlights upload
- `Graphical_Abstract.pdf` — separate graphical-abstract upload
- `Graphical_Abstract_Legend.txt` — short legend for the graphical abstract
- `Cover_Letter_Draft.md` — draft cover letter for Editorial Manager

## Reproducibility

The analysis software and configuration files are publicly available at:

https://github.com/dreyvinixz/RMT_Planar_Networks_Volatility_Forecasting_Brazil

Suggested software citation:

RMT Planar Networks & Volatility Forecasting Contributors. (2026). *RMT Planar Networks & Volatility Forecasting — Brazil* (Version 0.1.0) [Computer software]. https://github.com/dreyvinixz/RMT_Planar_Networks_Volatility_Forecasting_Brazil

Raw B3/BovDBv2 market data are not redistributed in this package. Their provenance,
access conditions and schema are documented in the public repository.
