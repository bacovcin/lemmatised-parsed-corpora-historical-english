import sys
from os import path as ospath
from PTree import *

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

def add_lemmas(tree, lemma_chars, lemmas, lemma_association):
    num_lemmas = {'one':'1',
                  'two':'2',
                  'three':'3',
                  'four':'4',
                  'five':'5',
                  'six':'6',
                  'seven':'7',
                  'eight':'8',
                  'nine':'9',
                  'ten':'10',
                  'eleven':'11',
                  'twelve':'12',
                  'thirteen':'13',
                  'fourteen':'14',
                  'fifteen':'15',
                  'sixteen':'16',
                  'seventeen':'17',
                  'eighteen':'18',
                  'nineteen':'19',
                  'twenty':'20'}
    pos_lemmas = {'NEG':'not',
                  'BAG':'be',
                  'BE':'be',
                  'BED':'be',
                  'BEI':'be',
                  'BEN':'be',
                  'BEP':'be',
                  'DAG':'do',
                  'DAN':'do',
                  'DO':'do',
                  'DOD':'do',
                  'DOI':'do',
                  'DON':'do',
                  'DOP':'do',
                  'HAG':'have',
                  'HAN':'have',
                  'HV':'have',
                  'HVD':'have',
                  'HVI':'have',
                  'HVN':'have',
                  'HVP':'have',
                  'ONE':'1',
                  'ONE$':'1',
                  'OTHER':'other',
                  'OTHER$':'other',
                  'OTHERS':'other',
                  'OTHERS$':'other',
                  'SUCH':'such',
                  'TO':'to',
                  'FOR':'for',
                  'FOR+TO':'for+to',
                  'ELSE':'else'}
    pro_lemmas = {'my':'i',
                  'mine':'i',
                  'thy':'thou',
                  'thine':'thou',
                  'his':'he',
                  'her':'she',
                  "it's":'it',
                  'its':'it',
                  'our':'we',
                  'your':'you',
                  'their':'they',
                  'it|be':'it'
                 }
    self_lemmas = {'myself':'i+self',
                   'thyself':'thou+self',
                   'yourself':'you+self',
                   'himself':'he+self',
                   'herself':'she+self',
                   'itself':'it+self',
                   'ourselves':'we+self',
                   'yourselves':'you+self',
                   'themselves':'they+self'}
    if tree.name in ['ID','CODE','METADATA']:
        return tree, lemma_chars, lemma_association
    if tree.height == 0 and tree.content != '0' and tree.content[0] != '*':
        full_text = tree.content
        if len(full_text) > 1 and full_text[-1] == '@':
            if full_text[0] == '@':
                text = full_text[1:-1]
            else:
                text = full_text[:-1]
        elif len(full_text) > 1 and full_text[0] == '@':
            text = full_text[1:]
        elif len(full_text) > 1 and '_' in full_text:
            text = ''.join(full_text.split('_'))
        else:
            text = full_text
        if tree.name in pos_lemmas.keys():
            ortho = PTree('ORTHO',full_text)
            metas = [PTree('LEMMA',pos_lemmas[tree.name])]
            j = len(text)
            while j > 0:
                lemma_chars.pop(0)
                lemma_association.pop(0)
                j -= 1
            return PTree(tree.name,[ortho, PTree('META',metas)]), lemma_chars, lemma_association 
        elif 'NPR' in tree.name:
            ortho = PTree('ORTHO',full_text)
            metas = [PTree('LEMMA','-'.join([y.capitalize() for y in
                                             ' '.join([x.capitalize() for x in
                                             full_text.split(' ')]).split('-')]))]
            j = len(text)
            while j > 0:
                lemma_chars.pop(0)
                lemma_association.pop(0)
                j -= 1
            return PTree(tree.name,[ortho, PTree('META',metas)]), lemma_chars, lemma_association 
        else:
            match_found = 0
            cur_text = ''
            cur_ass = []
            j = 0
            while match_found != 1:
                cur_text += lemma_chars.pop(0)
                cur_ass += [lemma_association.pop(0)]
                if text == cur_text:
                    ortho = PTree('ORTHO',full_text)
                    lemma = '+'.join([lemmas[x][4] for x in set(cur_ass)])
                    if 'PRO' in tree.name and lemma in pro_lemmas:
                        lemma = pro_lemmas[lemma]
                    elif tree.name == 'PRO+N' and lemma in self_lemmas:
                        lemma = self_lemmas[lemma]
                    elif 'NUM' in tree.name and lemma in num_lemmas:
                        lemma = num_lemmas[lemma]
                    metas = [PTree('LEMMA',lemma)]
                    return PTree(tree.name,[ortho, PTree('META',metas)]), lemma_chars, lemma_association 
                elif text[:len(cur_text)] != cur_text:
                    cur_text = ''
                    cur_ass = []
                    j += 1
                    if j > 2:
                        print('Here is the content:' + tree.content)
                        raise ValueError('Too long without finding what you need')
    elif tree.content == '0' or tree.content[0] == '*':
        if tree.content == '0' and tree.name == 'NUM':
            return PTree(tree.name,[PTree('ORTHO','0'),PTree('META',[PTree('LEMMA','0')])]), lemma_chars, lemma_association
        else:
            return PTree(tree.name,[PTree('META',[PTree('ALT-ORTHO',tree.content),PTree('LEMMA','0')])]), lemma_chars, lemma_association
    else:
        new_content = []
        for child in tree.content:
                new_tree, lemma_chars, lemma_association = add_lemmas(child, lemma_chars, lemmas, lemma_association)
                new_content.append(new_tree)
        return PTree(tree.name, new_content), lemma_chars, lemma_association

if __name__ == '__main__':
    for f in sys.argv:
        if f[-3:] in ['ref','psd']:
            # Load relevant files
            trees = ParseFiles([f])
            corpus = f.split('/')[1].split('-')[0].rstrip('0123456789')
            text = f.split('/')[-1].split('.')[0]

            # Only recreate unprocessed files
            backup_name = 'corpora-final/'+corpus+'/'+text+'.bkp'
            if ospath.isfile(backup_name):
                raise SystemExit
            lemma_text = open('corpora-out/'+corpus+'/'+text+'.txt')

            # Associate original text characters with lemmas
            lemma_chars = ''
            lemma_association = []
            lemmas = []
            for line in lemma_text:
                s = line.rstrip().split('\t')
                lemma_chars += s[0]
                lemmas.append(s)
                lemma_association += [len(lemmas)-1]*len(s[0])

            lemma_chars = list(lemma_chars)

            new_trees = []

            for key in trees:
                for tree in trees[key]:
                    new_tree, lemma_chars, lemma_association = add_lemmas(tree, lemma_chars, lemmas, lemma_association)
                    new_trees.append(new_tree)

            outfile = open('corpora-final/'+corpus+'/'+text+'.psd','w')
            for tree in new_trees:
                outfile.write(str(tree))
