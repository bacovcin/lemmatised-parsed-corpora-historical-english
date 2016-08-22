# Generate raw text files from trees
mkdir corpora-in
mkdir corpora-in/PCEEC
mkdir corpora-in/PPCEME
mkdir corpora-in/PPCMBE
python lemmatisation-scripts/strip-txt.py corpora/PCEEC/corpus/psd/*.ref
python lemmatisation-scripts/strip-txt.py corpora/PPCEME-RELEASE-3/corpus/psd/*/*.psd
python lemmatisation-scripts/strip-txt.py corpora/PPCMBE2-RELEASE-1/corpus/psd/*.psd

# Lemmatise all of the raw text files
mkdir corpora-out
mkdir corpora-out/PCEEC
mkdir corpora-out/PPCEME
mkdir corpora-out/PPCMBE
cd morphadorner
source ../lemmatisation-scripts/adornPCEEC.sh
source ../lemmatisation-scripts/adornPPCEME.sh
source ../lemmatisation-scripts/adornPPCMBE.sh
cd ../

# Add lemmatisation to current trees
mkdir corpora-final
mkdir corpora-final/PCEEC
mkdir corpora-final/PPCEME
mkdir corpora-final/PPCMBE
python lemmatisation-scripts/recombine.py corpora/PCEEC/corpus/psd/*.ref
python lemmatisation-scripts/recombine.py corpora/PPCEME-RELEASE-3/corpus/psd/*/*.psd
python lemmatisation-scripts/recombine.py corpora/PPCMBE2-RELEASE-1/corpus/psd/*.psd

# Clean intermediate files
rm -r corpora-in
rm -r corpora-out
