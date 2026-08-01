PDFLATEX = pdflatex -interaction=nonstopmode -halt-on-error

# Build every topic
all: intro-ann statistical-foundation genai rnn statistics world-models world-models-beamer

## ---- Intro to ANNs ----
intro-ann: intro-ann/intro-ann.pdf intro-ann/main-pt-tufte.pdf

intro-ann/intro-ann.pdf: intro-ann/intro-ann.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/intro-ann.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/intro-ann.tex

intro-ann/main-pt-tufte.pdf: intro-ann/main-pt-tufte.tex
	$(PDFLATEX) -output-directory=intro-ann intro-ann/main-pt-tufte.tex

## ---- Statistical foundations of ML ----
statistical-foundation: intro-ann/statistical-foundation/found.pdf intro-ann/statistical-foundation/isl.pdf

intro-ann/statistical-foundation/found.pdf: intro-ann/statistical-foundation/found.tex
	$(PDFLATEX) -output-directory=intro-ann/statistical-foundation intro-ann/statistical-foundation/found.tex

intro-ann/statistical-foundation/isl.pdf: intro-ann/statistical-foundation/isl.tex
	$(PDFLATEX) -output-directory=intro-ann/statistical-foundation intro-ann/statistical-foundation/isl.tex

## ---- Generative models for images ----
genai: genai-imagen/genai-attractor.pdf genai-imagen/image-complete(deepseek).pdf

genai-imagen/genai-attractor.pdf: genai-imagen/genai-attractor.tex
	$(PDFLATEX) -output-directory=genai-imagen genai-imagen/genai-attractor.tex
	$(PDFLATEX) -output-directory=genai-imagen genai-imagen/genai-attractor.tex

genai-imagen/image-complete(deepseek).pdf: genai-imagen/image-complete(deepseek).tex
	$(PDFLATEX) -output-directory=genai-imagen "genai-imagen/image-complete(deepseek).tex"

## ---- Recurrent Neural Networks ----
rnn: rnn/rnn2.pdf rnn/rnn.pdf

rnn/rnn2.pdf: rnn/rnn2.tex
	$(PDFLATEX) -output-directory=rnn rnn/rnn2.tex

rnn/rnn.pdf: rnn/rnn.tex
	$(PDFLATEX) -output-directory=rnn rnn/rnn.tex

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

.PHONY: all intro-ann statistical-foundation genai rnn statistics world-models world-models-beamer template clean
