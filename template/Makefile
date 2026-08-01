OUTDIR = output
PDFLATEX = pdflatex -output-directory=$(OUTDIR) -interaction=nonstopmode
PASS = $(PDFLATEX) sections/01-example.tex; test -f $(OUTDIR)/01-example.pdf
ATTRACTOR ?= dejong

# Generate cover attractor PNG (requires python3 + matplotlib)
cover:
	python3 generate_cover.py --attractor $(ATTRACTOR)

# Build example document (generates cover first)
example: cover
	$(PASS)
	$(PASS)

# Build blank document
blank:
	$(PDFLATEX) sections/02-blank.tex; test -f $(OUTDIR)/02-blank.pdf
	$(PDFLATEX) sections/02-blank.tex; test -f $(OUTDIR)/02-blank.pdf

# Build everything
all: example blank

# Clean auxiliary files only
clean:
	rm -f $(OUTDIR)/*.aux $(OUTDIR)/*.log $(OUTDIR)/*.toc $(OUTDIR)/*.out
	rm -f $(OUTDIR)/*.bbl $(OUTDIR)/*.blg $(OUTDIR)/*.fls $(OUTDIR)/*.fdb_latexmk
	rm -f $(OUTDIR)/*.lol $(OUTDIR)/*.lof $(OUTDIR)/*.lot $(OUTDIR)/*.md5
	rm -f $(OUTDIR)/*.run.xml $(OUTDIR)/*-blx.bib $(OUTDIR)/*.bcf

# Full clean including PDFs and generated cover
distclean: clean
	rm -f $(OUTDIR)/*.pdf
	rm -f cover/attractor-image.png cover/attractor-image.pdf cover/attractor-image.tex cover/attractor.tex
	rm -f cover/attractor-image.aux cover/attractor-image.log

.PHONY: all example blank cover clean distclean
