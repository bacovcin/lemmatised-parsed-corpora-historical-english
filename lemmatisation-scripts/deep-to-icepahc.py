import sys
from PTree import *

def isInt(x):
    try:
        int(x)
        return True
    except:
        return False

def to_icepahc(tree):
    if 'ORTHO' in [x.name for x in tree.content]:
        ortho = ''
        lemma = ''
        for x in tree.content:
            if x.name == 'ORTHO':
                ortho = x.content
            elif x.name == 'META':
                for y in x.content:
                    if y.name == 'LEMMA':
                        lemma = y.content
        return PTree(tree.name, ortho+'-~'+lemma)
    if 'META' in [x.name for x in tree.content]:
        ortho = ''
        lemma = ''
        for x in tree.content:
            if x.name== 'META':
                for y in x.content:
                    if y.name == 'ALT-ORTHO':
                        ortho = y.content
                    if y.name == 'LEMMA':
                        lemma = y.content
        return PTree(tree.name, ortho)
    elif tree.height == 0:
        return tree
    else:
        new_content = []
        for child in tree.content:
            if child.height > 0:
                new_content.append(to_icepahc(child))
            else:
                new_content.append(child)
        return PTree(tree.name,new_content)

if __name__ == '__main__':
    for f in sys.argv:
        if f[-3:] in ['ref','psd']:
            # Load relevant files
            trees = ParseFiles([f])
            print(trees)

            corpus = f.split('/')[1].split('-')[0].rstrip('0123456789')
            text = f.split('/')[-1].split('.')[0]

            new_trees = []

            i = 0
            for key in trees:
                for tree in trees[key]:
                    i += 1
                    print(i)
                    new_tree = to_icepahc(tree)
                    new_trees.append(new_tree)

            outfile = open('corpora-icepahc/'+corpus+'/'+text+'.psd','w')
            for tree in new_trees:
                outfile.write(str(tree))
