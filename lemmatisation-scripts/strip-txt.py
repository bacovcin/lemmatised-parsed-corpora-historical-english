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
                i = 0
                while i < len(tree):
                    word = tree[i]
                    if len(word) > 1:
                        if '_' in word:
                            for x in word.split('_'):
                                outfile.write(x+'\n')
                        elif word[-1] == '@':
                            j = 1
                            newword = word[:-1]
                            while True:
                                if tree[i+j][-1] == '@':
                                    newword += tree[i+j][1:-1]
                                    j += 1
                                else:
                                    newword += tree[i+j][1:]
                                    i += j
                                    break
                            outfile.write(newword+'\n')
                        else:
                            outfile.write(word+'\n')
                    else:
                        outfile.write(word+'\n')
                    i += 1
