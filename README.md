# Application of MorphAdorner to Parsed Corpora of Historical English
Application of the MorphAdorner Parser to the Parsed Corpora of Historical English

# Steps
1. Make a symbolic link to a folder containing the Parsed Corpora of Historical English (see note below): *ln -s *path-to-corpora* corpora/*
2. Unzip morphadorner-2.0.1.zip: *unzip morphadorner/morphadorner-2.0.1.zip*
3. Run make.sh: *bash make.sh*

N.B. The corpora folder must contain the following directories:
corpora/PCEEC/corpus/psd/
corpora/PPCEME-RELEASE-3/corpus/psd/penn1/
corpora/PPCEME-RELEASE-3/corpus/psd/penn2/
corpora/PPCEME-RELEASE-3/corpus/psd/helsinki/
corpora/PPCMBE2-RELEASE-1/corpus/psd/

# Output
In the corpora-final directory, there will be three sub-directories for the three corpora: PCEEC, PPCEME, and PPCMBE. Each sub-directory will include .psd files in the CorpusSearch-compatible "deep format". The "deep format" replaces terminal nodes (under POS tags) with an ORTHO node for original orthography and a META node with metadata. The metadata here includes the standardised spelling, lemma and NUPOS tag from MorphAdorner.

Please let me know if you have any questions: bacovcin@ling.upenn.edu
