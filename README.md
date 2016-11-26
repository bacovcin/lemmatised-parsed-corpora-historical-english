# Lemmatisation for the Parsed Corpora of Historical English
For Early Modern and Modern English, the MorphAdorner group has put together a
lemmatiser that is designed to deal with Modern English spelling and lexical
variation. For the PCEEC, PPCEME and PPCMBE, the scripts strip the text from the
parsed trees, run the resulting text through MorphAdorner and then reintegrates
the text into the trees.

For Middle and Old English, there are no existing lemmatisers. These scripts 
include a preliminary lemmatiser using data taken from the Middle English Dictionary 
(for Middle English) and from the Bosworth-Toller dictionary for Old English. 
In both cases, when the form is ambiguous between distinct lemmas, all compatible
lemmas are added to the parsed tree. In other words, the goal of the preliminary
lemmatiser is to be overly permissive and include as a lemma anything that could
possibly have that lemma rather than try to narrow down to the correct lemma for
a particular form.

# Steps
1. Make a symbolic link to a folder containing the Parsed Corpora of Historical English (see note below): *ln -s *path-to-corpora* corpora/*
2. Unzip morphadorner-2.0.1.zip: *unzip morphadorner/morphadorner-2.0.1.zip*
3. Run make: make

N.B. The corpora folder must contain the following directories:
corpora/PCEEC/*.ref
corpora/PPCEME/*.psd
corpora/PPCMBE/*.psd
corpora/PPCME2/*.psd

# Output
In the corpora-final directory, there will be three sub-directories for the three corpora: PCEEC, PPCEME, and PPCMBE. Each sub-directory will include .psd files in the CorpusSearch-compatible "deep format". The "deep format" replaces terminal nodes (under POS tags) with an ORTHO node for original orthography and a META node with metadata. The metadata here includes the standardised spelling, lemma and NUPOS tag from MorphAdorner.

Please let me know if you have any questions: bacovcin@ling.upenn.edu
