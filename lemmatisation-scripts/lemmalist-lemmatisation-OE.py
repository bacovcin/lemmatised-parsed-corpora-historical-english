import progressbar
import sys
from copy import copy, deepcopy
from collections import Counter

equivsets = {'+a':['+a','a','e','i','o','u','y'],
              'a':['+a','a','e','i','o','u','y'],
              'e':['+a','a','e','i','o','u','y'],
              '+e':['+a','a','e','i','o','u','y'],
              'i':['+a','a','e','i','o','u','y','+g','g'],
              'o':['+a','a','e','i','o','u','y'],
              'u':['+a','a','e','i','o','u','y','v'],
              'y':['+a','a','e','i','o','u','y','g','+g'],
              'b':['b'],
              'c':['k','q','c'],
              'd':['d'],
              'f':['f','v'],
              'g':['g','+g','y','i'],
              'h':['h'],
              'j':['j','g'],
              'k':['k','c','q'],
              'l':['l'],
              'm':['m'],
              'n':['n'],
              'p':['p'],
              'q':['q','c','k'],
              'r':['r'],
              's':['s','z'],
              't':['t'],
              'v':['+a','a','e','i','o','u','y','v'],
              'w':['w','v','u'],
              'x':['x'],
              'z':['z','s'],
              '+t':['+t','+d','th','dh'],
              '+d':['+t','+d','th','dh'],
              'th':['+t','+d','th','dh'],
              'dh':['+t','+d','th','dh'],
              '+g':['g','+g','y','i'],
              '&':['&'],
              ' ':[' '],
              '-':['-'],
              '=':['='],
              '$':['$']
}

def extract_phones(x):
    outputs = []
    i = 0
    while i < len(x):
        if i < len(x) -1:
            if ((x[i] == '+') or (x[i] in ['t','d'] and x[i+1] == 'h')):
                nx = x[i] + x[i+1]
                outputs += [nx]
                i += 1
            elif (x[i] == x[i+1]):
                outputs += x[i]
                i += 1
            elif x[i] == '-':
                pass
            else:
                outputs += x[i]
        else:
            outputs += x[i]
        i += 1
    return outputs

def levsearch(x,curdict,currow,curbest):
    bestlemmas = [curbest,[]]
    for key in curdict.keys():
        if key == '#':
            curval = currow[-1]
            if curval < bestlemmas[0]:
                bestlemmas = [curval,[curdict['#']]]
            elif curval == bestlemmas[0]:
                bestlemmas[1].append(curdict['#'])
        else:
            newrow = [currow[0]+1]
            for i in range(1,len(currow)):
                deletion = currow[i] + 1 
                insertion = newrow[-1] + 1 
                substitution = currow[i-1]
                if key != x[i-1]:
                    substitution += 1
                try:
                    if key not in equivsets[x[i-1]]:
                        substitution += 1
                except KeyError:
                    substitution += 1
                newrow.append(min(deletion,insertion,substitution))
            if True in [y <= bestlemmas[0] for y in newrow]:
                keybests = levsearch(x,curdict[key],newrow,bestlemmas[0])
                if keybests[0] < bestlemmas[0]:
                    bestlemmas = keybests
                elif keybests[0] == bestlemmas[0]:
                    bestlemmas[1] += keybests[1]
    return bestlemmas

infile = open('lemma-lists/OE-endings.txt')
endings = sorted(infile.readline().rstrip().split(','),key=lambda x:-len(x))
endings = [extract_phones(x) for x in endings]

def strip_endings(x,endings):
    for ending in endings:
        if len(ending) < len(x):
            if x[-len(ending):] == ending:
                if len(x[:-len(ending)]) > 2:
                    return(x[:-len(ending)])
    return(x)

def build_lemmas(x,lemma,curdict):
    if len(x) == 0:
        curdict['#'] = lemma
    else:
        try:
            curdict[x[0]] = build_lemmas(x[1:],lemma,curdict[x[0]])
        except KeyError:
            curdict[x[0]] = build_lemmas(x[1:],lemma,{})
    return curdict

lemmas = {}
infile = open('lemma-lists/OE_lemmas.txt')
lines = infile.readlines()
infile.close()
for line in lines[1:]:
    s = line.rstrip().split('\t')
    poses = []
    if 'Verb' in s[2]:
        poses.append('v')
    if 'Noun' in s[2]:
        poses.append('n')
    if 'Adjective' in s[2]:
        poses.append('adj')
    if 'Adverb' in s[2]:
        poses.append('adv')
    if 'Conjunction' in s[2]:
        poses.append('conj')
    if 'Interjection' in s[2]:
        poses.append('interj')
    if 'Preposition' in s[2]:
        poses.append('p')
    if poses == []:
        continue
    for pos in poses:
        try:
            pos_dict = lemmas[pos]
        except KeyError:
            pos_dict = {}
        for form in s[3].split(';'):
            newform = strip_endings(extract_phones(form.lower()),endings)
            pos_dict = build_lemmas(newform,s[1],pos_dict)
        lemmas[pos] = pos_dict

for arg in sys.argv:
    if arg[-3:] == 'txt':
        infile = open(arg)
        lines = infile.readlines()
        corpus = arg.split('/')[1].split('-')[0].rstrip('0123456789')
        text = arg.split('/')[-1]
        outfile = open('corpora-out/'+corpus+'/'+text,'w')
        with progressbar.ProgressBar(max_value=len(lines)) as bar:
            for i in range(len(lines)):
                line = lines[i]
                bar.update(i)
                pos, word = line.rstrip().split('~#')
                if pos == '':
                    outfile.write(word+'\t\n')
                    continue
                mylemmas = lemmas[pos]
                newword = copy(word)
                newform = strip_endings(extract_phones(newword.lower()),endings)
                currow = [0]*(len(newform)+1)
                for i in range(len(newform)+1):
                    currow[i] = i
                lemma = []
                i = 1
                while lemma == []:
                    score, lemma = levsearch(newform,mylemmas,currow,i)
                    i += 1
                    if i >= min(len(newform),5):
                        break
                if lemma == []:
                    outfile.write(word+'\t\n')
                else:
                    outfile.write(word+'\t'+'-~'.join(lemma)+'\n')
