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
