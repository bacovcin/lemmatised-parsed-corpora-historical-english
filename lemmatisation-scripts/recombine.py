import sys
from PTree import *

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False


def add_lemmas(tree, lemma_chars, lemmas, lemma_association):
    if tree.name in ['ID','CODE','METADATA']:
        return tree, lemma_chars, lemma_association
    if tree.height == 0 and tree.content != '0' and tree.content[0] != '*':
        text = tree.content
        match_found = 0
        cur_text = ''
        cur_ass = []
        while match_found != 1:
            cur_text += lemma_chars.pop(0)
            cur_ass += [lemma_association.pop(0)]
            if text == cur_text:
                ortho = PTree('ORTHO',text)
                metas = [PTree('STANDARD','+'.join([lemmas[x][3] for x in
                                                   set(cur_ass)])),
                         PTree('LEMMA','+'.join([lemmas[x][4] for x in
                                                set(cur_ass)])),
                         PTree('NUPOS','+'.join([lemmas[x][2] for x in
                                                set(cur_ass)]))
                        ]
                return PTree(tree.name,[ortho, PTree('META',metas)]), lemma_chars, lemma_association 
            elif text[:len(cur_text)] != cur_text:
                cur_text = ''
                cur_ass = []
    elif tree.content == '0' or (tree.content[0] == '*' and '-' not in
                                 tree.content):
        return PTree('META',[PTree('ALT-ORTHO',tree.content),PTree('LEMMA','0')]), lemma_chars, lemma_association
    elif tree.content[0] == '*':
        return PTree('META',[PTree('ALT-ORTHO',tree.content.split('-')[0]),PTree('INDEX',tree.content.split('-')[1])]), lemma_chars, lemma_association
    else:
        new_content = []
        for child in tree.content:
                new_tree, lemma_chars, lemma_association = add_lemmas(child, lemma_chars, lemmas, lemma_association)
                new_content.append(new_tree)
        if '-' in tree.name:
            if isInt(tree.name.split('-')[1]):
                new_content.insert(0,PTree('META',[PTree('INDEX',tree.name.split('-')[1])]))
                new_name = tree.name.split('-')[0]
            else:
                new_name = tree.name
        else:
            new_name = tree.name
        return PTree(new_name, new_content), lemma_chars, lemma_association

if __name__ == '__main__':
    for f in sys.argv:
        if f[-3:] in ['ref','psd']:
            # Load relevant files
            trees = ParseFiles([f])
            corpus = f.split('/')[1].split('-')[0].rstrip('0123456789')
            text = f.split('/')[-1].split('.')[0]
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
