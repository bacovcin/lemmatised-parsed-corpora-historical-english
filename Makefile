pceectargs:= $(addprefix corpora-final/PCEEC/,$(addsuffix .psd,$(basename $(notdir $(wildcard corpora/PCEEC/*.ref)))))
ppcme2targs:= $(addprefix corpora-final/PPCME/,$(addsuffix .psd,$(basename $(notdir $(wildcard corpora/PPCME2/*.psd)))))
ppcemetargs:= $(addprefix corpora-final/PPCEME/,$(notdir $(wildcard corpora/PPCEME/*.psd)))
ppcmbetargs:= $(addprefix corpora-final/PPCMBE/,$(notdir $(wildcard corpora/PPCMBE/*.psd)))
pceecins := $(addprefix corpora-in/PCEEC/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PCEEC/*.ref)))))
ppcemeins := $(addprefix corpora-in/PPCEME/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PPCEME/*.psd)))))
ppcmbeins := $(addprefix corpora-in/PPCMBE/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PPCMBE/*.psd)))))
pceecouts := $(addprefix corpora-out/PCEEC/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PCEEC/*.ref)))))
ppcemeouts := $(addprefix corpora-out/PPCEME/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PPCEME/*.psd)))))
ppcmbeouts := $(addprefix corpora-out/PPCMBE/,$(addsuffix .txt,$(basename $(notdir $(wildcard corpora/PPCMBE/*.psd)))))
corpora-in/PCEEC/%.txt : corpora/PCEEC/%.ref lemmatisation-scripts/strip-txt.py
	@echo --- Striping text from $< ---
	@mkdir -p $(@D)
	python $(word 2,$^) $<

corpora-in/PPCEME/%.txt : corpora/PPCEME/%.psd lemmatisation-scripts/strip-txt.py
	@echo --- Striping text from $< ---
	@mkdir -p $(@D)
	python $(word 2,$^) $<

corpora-in/PPCMBE/%.txt : corpora/PPCMBE/%.psd lemmatisation-scripts/strip-txt.py
	@echo --- Striping text from $< ---
	@mkdir -p $(@D)
	python $(word 2,$^) $<

corpora-in/PPCME/%.txt : corpora/PPCME2/%.psd lemmatisation-scripts/strip-txt-lemmalist.py
	@echo --- Striping text from $< ---
	@mkdir -p $(@D)
	python $(word 2,$^) $<

corpora-out/PPCME/%.txt : corpora-in/PPCME/%.txt lemmatisation-scripts/lemmalist-lemmatisation-MED.py
	@echo --- Lemmatising $< ---
	@mkdir -p $(@D)
	python $(word 2,$^) $<

$(pceecouts) : dummy-PCEEC.txt

dummy-PCEEC.txt : $(pceecins) morphadorner/emeplaintext.properties morphadorner/data/emelexicon.lex morphadorner/data/emetransmat.mat morphadorner/data/emesuffixlexicon.lex morphadorner/data/ememergedspellingpairs.tab morphadorner/data/ncfmergedspellingpairs.tab morphadorner/data/standardspellings.txt morphadorner/data/spellingsbywordclass.txt
	@echo --- Lemmatising $< ---
	@mkdir -p $(@D) && \
	cd morphadorner && \
	java -Xmx8g -Xss1m -cp :bin/:dist/*:lib/* \
		edu.northwestern.at.morphadorner.MorphAdorner \
		-p emeplaintext.properties \
		-l data/emelexicon.lex \
		-t data/emetransmat.mat \
		-u data/emesuffixlexicon.lex \
		-a data/ememergedspellingpairs.tab \
		-a data/ncfmergedspellingpairs.tab \
		-s data/standardspellings.txt \
		-w data/spellingsbywordclass.txt \
		-o ../corpora-out/PCEEC \
		../corpora-in/PCEEC/*.txt && \
	cd ../

$(ppcemeouts) : dummy-PPCEME.txt

dummy-PPCEME.txt : $(ppcemeins) morphadorner/emeplaintext.properties morphadorner/data/emelexicon.lex morphadorner/data/emetransmat.mat morphadorner/data/emesuffixlexicon.lex morphadorner/data/ememergedspellingpairs.tab morphadorner/data/ncfmergedspellingpairs.tab morphadorner/data/standardspellings.txt morphadorner/data/spellingsbywordclass.txt
	@echo --- Lemmatising $@ ---
	@mkdir -p $(@D) && \
	cd morphadorner && \
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
		../corpora-in/PPCEME/*.txt && \
	cd ../


$(ppcmbeouts) : dummy-PPCMBE.txt
	
dummy-PPCMBE.txt : $(ppcmbeins) lemmatisation-scripts/eccoplaintext.properties morphadorner/data/eccolexicon.lex morphadorner/data/ncftransmat.mat morphadorner/data/eccosuffixlexicon.lex morphadorner/data/ncfmergedspellingpairs.tab morphadorner/data/eccomergedspellingpairs.tab morphadorner/data/standardspellings.txt morphadorner/data/spellingsbywordclass.txt
	@echo --- Lemmatising $@ ---
	@mkdir -p $(@D) && \
	cd morphadorner && \
	java -Xmx8g -Xss1m -cp :bin/:dist/*:lib/* \
		edu.northwestern.at.morphadorner.MorphAdorner \
		-p ../lemmatisation-scripts/eccoplaintext.properties \
		-l data/eccolexicon.lex \
		-t data/ncftransmat.mat \
		-u data/eccosuffixlexicon.lex \
		-a data/ncfmergedspellingpairs.tab \
		-a data/eccomergedspellingpairs.tab \
		-s data/standardspellings.txt \
		-w data/spellingsbywordclass.txt \
		-o ../corpora-out/PPCMBE \
		../corpora-in/PPCMBE/*.txt && \
	cd ../

.INTERMEDIATE : $(pceecins) $(pceecouts) dummy-PCEEC.txt $(ppcemeins) $(ppcemeouts) dummy-PPCEME.txt $(ppcmbeins) $(ppcmbeouts) dummy-PPCMBE.txt 

$(pceectargs) : corpora-final/PCEEC/%.psd : lemmatisation-scripts/recombine.py corpora-out/PCEEC/%.txt 
	@echo --- Recombining PCEEC ---
	@mkdir -p $(@D)
	python $< $(addprefix corpora/PCEEC/,$(addsuffix .ref,$(basename $(notdir $@))))

$(ppcmbetargs) : corpora-final/PPCMBE/%.psd : lemmatisation-scripts/recombine.py corpora-out/PPCMBE/%.txt
	@echo --- Recombining PPCMBE ---
	@mkdir -p $(@D)
	python $< $(addprefix corpora/PPCMBE/,$(notdir $@))

$(ppcemetargs) : corpora-final/PPCEME/%.psd : lemmatisation-scripts/recombine.py corpora-out/PPCEME/%.txt 
	@echo --- Recombining PPCEME ---
	@mkdir -p $(@D)
	python $< $(addprefix corpora/PPCEME/,$(notdir $@))

$(ppcme2targs) : corpora-final/PPCME/%.psd : lemmatisation-scripts/recombine-lemmalist.py corpora-out/PPCME/%.txt
	@echo --- Recombining PPCME2 ---
	@mkdir -p $(@D)
	python $< $(addprefix corpora/PPCME2/,$(notdir $@))

all : $(pceectargs) $(ppcemetargs) $(ppcmbetargs) $(ppcme2targs)
