# ML Notes

Personal machine learning and deep learning study notes, written in LaTeX using
the [Tufte-handout](https://ctan.org/pkg/tufte-latex) document class.

Everything lives in per-topic directories, with a single root `Makefile` that
builds every document. Compiled PDFs are committed to the repo, while LaTeX
auxiliary files are gitignored.

## Documents

| Directory / file | Topic | Lang | Status |
| --- | --- | --- | --- |
| `intro-ann/intro-ann.tex` | Introduction to Deep Learning (perceptron, MLP, backprop, regularization, UAT) | EN | Canonical |
| `intro-ann/main-pt-tufte.tex` | Same introduction | PT | Canonical |
| `intro-ann/statistical-foundation/found.tex` | Foundations of probability & statistical learning | EN | Canonical |
| `intro-ann/statistical-foundation/isl.tex` | Statistical learning + intro to ANNs | EN | Older variant of `found` |
| `intro-ann/old-version/main-en.tex` | Earlier draft of the intro | EN | Archived |
| `intro-ann/old-version/main-pt.tex` | Earlier draft of the intro | PT | Archived |
| `genai-imagen/genai-attractor.tex` | Generative models for images (VAE, GAN, diffusion, style transfer) | PT | Canonical |
| `genai-imagen/image-complete(deepseek).tex` | Complete generative models notes (adds flow & energy models) | PT | Canonical |
| `genai-imagen/old-version/genai.tex` | Earlier draft | PT | Archived |
| `rnn/rnn2.tex` | Recurrent Neural Networks — mathematical foundations | EN | Canonical |
| `rnn/rnn.tex` | Earlier RNN draft | EN | Archived |
| `rnn/recurrents.tex` | Short RNN intro | PT | Archived |
| `statistics/probability-ml.tex` | Probability, Monte Carlo methods, statistical learning | PT | Canonical |
| `world-models/world_models.tex` | World Models survey (handout) | EN | Canonical |
| `world-models/world_models_beamer.tex` | World Models (beamer slides) | PT | Canonical |

## Structure

```
├── Makefile                 builds every document
├── README.md
├── intro-ann/               intro to deep learning (EN/PT)
│   ├── statistical-foundation/   probability & statistical learning
│   └── old-version/              archived drafts
├── genai-imagen/            deep generative models for images
│   ├── cover/               generated cover image
│   ├── generate_cover.py    cover generation script
│   └── old-version/         archived draft
├── rnn/                     recurrent neural networks
├── statistics/              probability & statistical learning (PT)
├── world-models/            world models survey (handout + slides)
├── template/                reusable starting point for new documents
└── resources/               shared TikZ figures, grouped by topic
    ├── base/                perceptron, MLP, backprop, UAT figures
    ├── gan/                 GAN figures
    ├── rnns/                LSTM/SSM plots
    └── style-transfer/      CNN/style-transfer figures
```

## Prerequisites

- **TeX Live** with the `tufte-handout` class, `pgfplots`, `tikz`, `natbib`,
  and `bibtex` (for `world-models`).
- **Python 3 + matplotlib** — only needed to regenerate cover images
  (`template/` and `genai-imagen/`).

## Building

The root `Makefile` builds every document. Compilation runs from the repo root
so the shared figures under `resources/` resolve correctly; PDFs are written
next to their `.tex` source.

```bash
make all                     # build everything
make intro-ann               # intro to deep learning (EN + PT)
make statistical-foundation  # probability & statistical learning
make genai                   # generative models
make rnn                     # RNN notes
make statistics              # probability & statistics (PT)
make world-models            # world models handout (runs bibtex)
make world-models-beamer     # world models slides
make template                # compile the template example + blank docs
make clean                   # remove LaTeX auxiliary files
```

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
