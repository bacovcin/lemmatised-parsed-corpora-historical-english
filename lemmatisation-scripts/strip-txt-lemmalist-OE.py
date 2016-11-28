import sys
from PTree import *

pos_equiv = {'ADJ':'adj',
             'ADJ^N':'adj',
             'ADJ^A':'adj',
             'ADJ^G':'adj',
             'ADJ^D':'adj',
             'ADJ^I':'adj',
             'ADJR':'adj',
             'ADJR^N':'adj',
             'ADJR^A':'adj',
             'ADJR^G':'adj',
             'ADJR^D':'adj',
             'ADJR^I':'adj',
             'ADJS':'adj',
             'ADJS^N':'adj',
             'ADJS^A':'adj',
             'ADJS^G':'adj',
             'ADJS^D':'adj',
             'ADJS^I':'adj',
             'ADV':'adv',
             'ADV^D':'adv',
             'ADV^T':'adv',
             'ADV^L':'adv',
             'ADVR':'adv',
             'ADVS':'adv',
             'CONJ':'conj',
             'INTJ':'interj',
             'MD':'v',
             'MD0':'v',
             'MD^D':'v',
             'MDD':'v',
             'MDDI':'v',
             'MDDS':'v',
             'MDI':'v',
             'MDP':'v',
             'MDPI':'v',
             'MDPS':'v',
             'N':'n',
             'N^N':'n',
             'N^A':'n',
             'N^G':'n',
             'N^D':'n',
             'N^I':'n',
             'N$':'n',
             'NS':'n',
             'NS$':'n',
             'P':'p',
             'Q':'adj',
             'Q^N':'adj',
             'Q^A':'adj',
             'Q^G':'adj',
             'Q^D':'adj',
             'Q^I':'adj',
             'Q$':'adj',
             'QR':'adj',
             'QR^N':'adj',
             'QR^A':'adj',
             'QR^G':'adj',
             'QR^D':'adj',
             'QR^I':'adj',
             'QS':'adj',
             'QS^N':'adj',
             'QS^A':'adj',
             'QS^G':'adj',
             'QS^D':'adj',
             'QS^I':'adj',
             'RP':'adv',
             'VAG':'v',
             'VAG^N':'v',
             'VAG^A':'v',
             'VAG^G':'v',
             'VAG^D':'v',
             'VAG^I':'v',
             'VAN':'v',
             'VB':'v',
             'VB^D':'v',
             'VBD':'v',
             'VBDI':'v',
             'VBDS':'v',
             'VBI':'v',
             'VBN':'v',
             'VBN^N':'v',
             'VBN^A':'v',
             'VBN^G':'v',
             'VBN^D':'v',
             'VBN^I':'v',
             'VBP':'v',
             'VBPH':'v',
             'VBPI':'v',
             'VBPS':'v',
        }

def get_text(tree):
    if tree.height == 0 and tree.content != '0' and tree.content[0] != '*' and tree.name not in ['ID','CODE','METADATA']:
        if tree.name in pos_equiv.keys():
            return [pos_equiv[tree.name]+'~#'+tree.content]
        else:
            return ['~#'+tree.content]
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
            text = '.'.join(f.split('/')[-1].split('.')[:-1])
            new_trees = []

            for key in trees:
                for tree in trees[key]:
                    new_tree = get_text(tree)
                    new_trees.append(new_tree)

            outfile = open('corpora-in/'+corpus+'/'+text+'.txt','w')
            for tree in new_trees:
                for word in tree:
                    outfile.write(word+'\n')
