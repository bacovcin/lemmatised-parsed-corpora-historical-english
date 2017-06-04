import sys
import os
from PTree import *

def isFloat(x):
    try:
        float(x)
        return True
    except:
        if x in ['-','...']:
            return True
        else:
            return False

def extract_lemmas(tree):
    common_abbr = {'Mr':'Mister',
                   'Mr.':'Mister',
                   'Dr':'Doctor',
                   'Dr.':'Doctor',
                   'Mrs':'Mistress',
                   'Mrs.':'Mistress',
                   'Revd':'Reverend',
                   'Revd.':'Reverend',
                   'etc':'etcetera',
                   'etc.':'etcetera',
                   'St':'Saint',
                   'St.':'Saint'}
    pos_groups = {
        'WADV+P':'WADV+P',
        'OTHER+N':'OTHER+N',
        'Q+VAN':'Q+VAN',
        'WD+ADV':'WD+ADV',
        'Q+N':'Q+N',
        '.':'.|,|\'|"',
        ',':'.|,|\'|"',
        '\'':'.|,|\'|"',
        '"':'.|,|\'|"',
        '$':'$',
        'ADJ':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADJR':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADJS':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADV':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADVR':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADVS':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADV+P':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADV+WARD':'ADJ|ADJR|ADJS|ADV|ADVR|ADVS|ADV+P|ADV+WARD',
        'ADV+VAG':'ADV+VAG',
        'ADJ+N':'ADJ+N',
        'ALSO':'ALSO',
        'BAG':'BAG|BE|BED|BEI|BEN|BEP',
        'BE':'BAG|BE|BED|BEI|BEN|BEP',
        'BED':'BAG|BE|BED|BEI|BEN|BEP',
        'BEI':'BAG|BE|BED|BEI|BEN|BEP',
        'BEN':'BAG|BE|BED|BEI|BEN|BEP',
        'BEP':'BAG|BE|BED|BEI|BEN|BEP',
        'C':'C',
        'CONJ':'CONJ',
        'D':'D',
        'D+OTHER':'D+OTHER',
        'DAG':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DAN':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DO':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DOD':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DOI':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DON':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'DOP':'DAG|DAN|DO|DOD|DOI|DON|DOP',
        'ELSE':'ELSE',
        'EX':'EX',
        'FOR':'FOR',
        'FOR+TO':'FOR+TO',
        'FP':'FP',
        'FW':'FW',
        'HAG':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HAN':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HV':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HVD':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HVI':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HVN':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'HVP':'HAG|HAN|HV|HVD|HVI|HVN|HVP',
        'INTJ':'INTJ',
        'LB':'LB',
        'LS':'LS',
        'MAN':'MAN',
        'MD':'MD|MD0',
        'MD0':'MD|MD0',
        'N':'N|N$|NS|NS$|NX',
        'N$':'N|N$|NS|NS$|NX',
        'NS':'N|N$|NS|NS$|NX',
        'NS$':'N|N$|NS|NS$|NX',
        'NX':'N|N$|NS|NS$|NX',
        'NEG':'NEG',
        'NPR':'NPR|NPR$|NPRS|NPRS$',
        'NPR$':'NPR|NPR$|NPRS|NPRS$',
        'NPRS':'NPR|NPR$|NPRS|NPRS$',
        'NPRS$':'NPR|NPR$|NPRS|NPRS$',
        'NUM':'NUM|NUM$',
        'NUM$':'NUM|NUM$',
        'ONE':'ONE|ONES|ONE$',
        'ONES':'ONE|ONES|ONE$',
        'ONE$':'ONE|ONES|ONE$',
        'OTHER':'OTHER|OTHER$|OTHERS|OTHERS$',
        'OTHER$':'OTHER|OTHER$|OTHERS|OTHERS$',
        'OTHERS':'OTHER|OTHER$|OTHERS|OTHERS$',
        'OTHERS$':'OTHER|OTHER$|OTHERS|OTHERS$',
        'P':'P',
        'P+N':'P+N',
        'P+ADVR+Q':'P+ADVR+Q',
        'PRO':'PRO|PRO$',
        'PRO$':'PRO|PRO$',
        'PRO+N':'PRO+N',
        'Q':'Q|Q$|QR|QS',
        'Q$':'Q|Q$|QR|QS',
        'QR':'Q|Q$|QR|QS',
        'QS':'Q|Q$|QR|QS',
        'Q+WADV':'Q+WADV',
        'Q+NS':'Q+NS',
        'RP':'RP',
        'RP+WARD':'RP+WARD',
        'SUCH':'SUCH',
        'TO':'TO',
        'VAG':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VAN':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VB':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VBD':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VBI':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VBN':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'VBP':'VAG|VAN|VB|VBD|VBI|VBN|VBP',
        'WADV+ADV':'WADV+ADV',
        'WADV':'WADV|WD|WPRO|WPRO$|WQ',
        'WD':'WADV|WD|WPRO|WPRO$|WQ',
        'WPRO':'WADV|WD|WPRO|WPRO$|WQ',
        'WPRO$':'WADV|WD|WPRO|WPRO$|WQ',
        'WQ':'WADV|WD|WPRO|WPRO$|WQ',
        'WARD':'WARD',
        'X':'X'
                 }
    lemmas = []
    if 'ORTHO' in [x.name for x in tree.content]:
        ortho = ''
        lemma = ''
        pos = tree.name.split('_')[0].split('-')[0]
        for x in tree.content:
            if x.name == 'ORTHO':
                ortho = x.content.lower()
            elif x.name == 'META':
                for y in x.content:
                    if y.name == 'LEMMA':
                        lemma = y.content.lower()
        if tree.name == '$':
            lemma = 'GEN'
        elif tree.name in ['NPR$','NPRS$']:
            lemma = lemma[:-1].split("'")[0]
        elif tree.name == 'FW':
            lemma = ortho
        if pos not in pos_groups and '+' in pos:
            pos_groups[pos] = pos
        try:
            lemmas.append((pos_groups[pos], ortho, common_abbr[lemma]))
        except KeyError:
            lemmas.append((pos_groups[pos], ortho, lemma))
    elif tree.height > 0:
        for child in tree.content:
            if child.height > 0:
                lemmas += extract_lemmas(child)
    return lemmas

if __name__ == '__main__':
    ourlemmas = []
    for f in sys.argv:
        if f[-3:] in ['ref','psd']:
            print('Extracting from: '+f.split('/')[-1])
            # Load relevant files
            trees = ParseFiles([f])

            for key in trees:
                for tree in trees[key]:
                    ourlemmas += extract_lemmas(tree)

    print('\nBuilding the database...')
    lemmadb = {}
    for lemma in ourlemmas:
        fl = (lemma[1],lemma[2])
        try:
            if fl not in lemmadb[lemma[0]]:
                lemmadb[lemma[0]].append(fl)
        except:
            lemmadb[lemma[0]] = [fl]

    print('\nWriting out POSes...\n')
    outfile = open('extracted-lemma-list.txt','w')
    for key in lemmadb:
        print('Writing out '+key+'...')
        outfile.write('###'+key+'\n')
        if key == 'FW':
            outfile.write('---FW\n')
            continue
        elif key == 'NPR|NPR$|NPRS|NPRS$':
            outfile.write('---NPR\n')
            continue
        keylemmas = {}
        for fl in lemmadb[key]:
            try:
                if fl[0] not in keylemmas[fl[1]]:
                    keylemmas[fl[1]].append(fl[0])
            except:
                keylemmas[fl[1]] = [fl[0]]
        for lemma in sorted(keylemmas.keys()):
            outfile.write(lemma+'\t'+' '.join(keylemmas[lemma])+'\n')
