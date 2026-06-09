all:
	pdflatex main-en.tex
	pdflatex main-pt.tex

clean:
	rm -f *.aux *.log *.toc *.out *.md5 *.lol *.lof *.lot *.fls *.fdb_latexmk

.PHONY: all clean
