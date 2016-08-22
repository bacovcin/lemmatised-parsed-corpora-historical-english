#!/bin/bash
java -Xmx8g -Xss1m -cp :bin/:dist/*:lib/* \
	edu.northwestern.at.morphadorner.MorphAdorner \
	-p emeplaintext.properties \
	-l data/emelexicon.lex \
	-t data/emetransmat.mat \
	-u data/emesuffixlexicon.lex \
	-a data/ememergedspellingpairs.tab \
	-s data/standardspellings.txt \
	-w data/spellingsbywordclass.txt \
	-o ../corpora-out/PPCEME \
	../corpora-in/PPCEME/*.txt
