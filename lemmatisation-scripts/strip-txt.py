import sys
from PTree import *

def get_text(tree):
    if tree.height == 0 and tree.content != '0' and tree.content[0] != '*' and tree.name not in ['ID','CODE','METADATA']:
        return [tree.content]
    elif tree.height == 0 or tree.name in ['ID','CODE','METADATA']:
        return []
    else:
        text = []
        for child in tree.content:
                text += get_text(child)
        return text

if __name__ == '__main__':
    for f in sys.argv:
        if f[-3:] in ['ref','psd']:
            # Load relevant files
            trees = ParseFiles([f])
            corpus = f.split('/')[1].split('-')[0].rstrip('0123456789')
            text = f.split('/')[-1].split('.')[0]
            new_trees = []

            for key in trees:
                for tree in trees[key]:
                    new_tree = get_text(tree)
                    new_trees.append(new_tree)

            outfile = open('corpora-in/'+corpus+'/'+text+'.txt','w')
            for tree in new_trees:
                for word in tree:
                    outfile.write(word+'\n')
