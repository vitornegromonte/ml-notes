PDFLATEX = pdflatex -interaction=nonstopmode -halt-on-error

# Build every topic
all: intro-ann genai rnn statistics world-models world-models-beamer

## ---- Intro to ANNs ----
intro-ann: intro-ann/deepseek.pdf intro-ann/main-en-tufte.pdf intro-ann/main-pt-tufte.pdf

intro-ann/deepseek.pdf: intro-ann/deepseek.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/deepseek.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/deepseek.tex

intro-ann/main-en-tufte.pdf: intro-ann/main-en-tufte.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/main-en-tufte.tex

intro-ann/main-pt-tufte.pdf: intro-ann/main-pt-tufte.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/main-pt-tufte.tex

## ---- Generative models for images ----
genai: genai-imagen/genai-si-tufte-attractor.pdf

genai-imagen/genai-si-tufte-attractor.pdf: genai-imagen/genai-si-tufte-attractor.tex
	$(PDFLATEX) -output-directory=genai-imagen genai-imagen/genai-si-tufte-attractor.tex
	$(PDFLATEX) -output-directory=genai-imagen genai-imagen/genai-si-tufte-attractor.tex

## ---- Recurrent Neural Networks ----
rnn: rnn/rnn2.pdf

rnn/rnn2.pdf: rnn/rnn2.tex
	$(PDFLATEX) -output-directory=rnn rnn/rnn2.tex

## ---- Probability & statistics ----
statistics: statistics/probability-ml.pdf

statistics/probability-ml.pdf: statistics/probability-ml.tex
	$(PDFLATEX) -output-directory=statistics statistics/probability-ml.tex
	$(PDFLATEX) -output-directory=statistics statistics/probability-ml.tex

## ---- World models (handout + beamer) ----
world-models: world-models/world_models.pdf

world-models/world_models.pdf: world-models/world_models.tex world-models/references.bib
	$(PDFLATEX) -output-directory=world-models world-models/world_models.tex
	cd world-models && bibtex world_models
	$(PDFLATEX) -output-directory=world-models world-models/world_models.tex
	$(PDFLATEX) -output-directory=world-models world-models/world_models.tex

world-models-beamer: world-models/world_models_beamer.pdf

world-models/world_models_beamer.pdf: world-models/world_models_beamer.tex
	$(PDFLATEX) -output-directory=world-models world-models/world_models_beamer.tex
	$(PDFLATEX) -output-directory=world-models world-models/world_models_beamer.tex

## ---- Reusable template ----
template:
	$(MAKE) -C template

clean:
	rm -f *.aux *.log *.toc *.out *.md5 *.lol *.lof *.lot *.fls *.fdb_latexmk
	rm -f intro-ann/*.aux intro-ann/*.log intro-ann/*.toc intro-ann/*.out intro-ann/*.md5
	rm -f intro-ann/statistical-foundation/*.aux intro-ann/statistical-foundation/*.log intro-ann/statistical-foundation/*.toc intro-ann/statistical-foundation/*.out
	rm -f genai-imagen/*.aux genai-imagen/*.log genai-imagen/*.toc genai-imagen/*.out
	rm -f rnn/*.aux rnn/*.log rnn/*.toc rnn/*.out
	rm -f statistics/*.aux statistics/*.log statistics/*.toc statistics/*.out
	rm -f world-models/*.aux world-models/*.log world-models/*.toc world-models/*.out world-models/*.bbl world-models/*.blg

.PHONY: all intro-ann genai rnn statistics world-models world-models-beamer template clean
