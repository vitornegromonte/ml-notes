# ML Notes

Personal machine learning study notes in LaTeX, using the
[Tufte-handout](https://ctan.org/pkg/tufte-latex) document class.

## Structure

```
├── intro-ann/            Introduction to Artificial Neural Networks (EN/PT, several versions)
│   ├── deepseek.tex      EN, most complete version
│   ├── main-en-tufte.tex / main-pt-tufte.tex
│   ├── v2.tex / v3.tex   earlier iterations
│   ├── old-version/      earliest drafts (plain article class)
│   └── statistical-foundation/   probability & statistical learning foundations
├── genai-imagen/         Deep generative models for images (PT)
├── rnn/                  Recurrent Neural Networks
├── statistics/           Probability, Monte Carlo methods, statistical learning (PT)
├── world-models/         World Models survey (handout + beamer slides)
├── template/             Reusable starting point for new Tufte-style documents
├── resources/            Shared TikZ figures, grouped by topic (base, gan, rnns, style-transfer)
└── Makefile              Builds every document
```

## Building

The root `Makefile` builds every document. Compilation runs from the repo
root so shared figures under `resources/` resolve correctly; PDFs land next to
their `.tex` source.

```bash
make all                 # build every topic
make intro-ann           # ANN notes (deepseek, main-en, main-pt)
make genai               # generative models
make rnn                 # RNN notes
make statistics          # probability & statistics
make world-models        # world models handout (runs bibtex)
make world-models-beamer # world models slides
make template            # compile the template example + blank docs
make clean               # remove LaTeX auxiliary files
```

Compiled PDFs are committed to the repo; LaTeX auxiliary files (`*.aux`, `*.log`,
`*.toc`, ...) are gitignored.

## Template

The `template/` directory is a clean, reusable starting point for new
Tufte-style LaTeX documents. It includes:

- **`tufte-notes.sty`** — shared style package (color scheme, common packages, TikZ styles)
- **`sections/01-example.tex`** — illustrated usage example
- **`sections/02-blank.tex`** — minimal blank starter
- **`resources/tikz/`** — reusable TikZ figure fragments
- **`resources/images/`** — raster image assets
- **`references/template.bib`** — sample bibliography file
- **`Makefile`** — build system (compiles into `output/`)

### Quick start

```bash
cd template
make all       # compile the example and blank documents (generates cover first)
make example   # just the example document
make clean     # remove auxiliary files
make distclean # remove auxiliary files + PDFs + generated cover
```
