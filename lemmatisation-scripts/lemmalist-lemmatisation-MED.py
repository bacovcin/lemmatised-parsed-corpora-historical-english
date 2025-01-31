import progressbar
from copy import copy, deepcopy
import sys
from collections import Counter

equivsets = {'+a':['+a','a','e','i','o','u','y'],
              'a':['+a','a','e','i','o','u','y'],
              'e':['+a','a','e','i','o','u','y'],
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
              '=':['=']
}

def strip_endings(x,endings):
    for ending in endings:
        if len(ending) < len(x):
            if x[-len(ending):] == ending:
                if len(x[:-len(ending)]) > 2:
                    return(x[:-len(ending)])
    return(x)

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
    medlemmas = []
    oedlemmas = []
    for key in curdict.keys():
        if key == '#':
            curval = currow[-1]
            if curval < curbest:
                medlemmas = curdict['#'][0]
                oedlemmas = curdict['#'][1]
                curbest = curval
            elif curval == curbest:
                medlemmas += curdict['#'][0]
                oedlemmas += curdict['#'][1]
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
            if True in [y <= curbest for y in newrow]:
                keybest, keymed, keyoed = levsearch(x,curdict[key],
                                                    newrow,curbest)
                if keybest < curbest:
                    medlemmas = keymed
                    oedlemmas = keyoed
                    curbest = keybest
                elif keybest == curbest:
                    medlemmas += keymed
                    oedlemmas += keyoed
    return curbest, medlemmas, oedlemmas

def build_lemmas(x,lemma,curdict):
    if len(x) == 0:
        try:
            curdict['#'][0].append(lemma[0])
            curdict['#'][1].append(lemma[1])
        except KeyError:
            curdict['#'] = [[lemma[0]],[lemma[1]]]
    else:
        try:
            curdict[x[0]] = build_lemmas(x[1:],lemma,curdict[x[0]])
        except KeyError:
            curdict[x[0]] = build_lemmas(x[1:],lemma,{})
    return curdict

infile = open('lemma-lists/MED-endings.txt')
endings = sorted(infile.readline().rstrip().split(','),key=lambda x:-len(x))
endings = [extract_phones(x) for x in endings]

lemmas = {}
infile = open('lemma-lists/MED_lemmas.csv')
lines = infile.readlines()
infile.close()
names = lines[0].rstrip().split(',')
for line in lines[1:]:
    s = line.rstrip().split(',')
    try:
        # Don't try suffixes
        if s[2] not in ['adj','adv','conj','interj','v','n','p']:
            continue
        if s[3] == '':
            s[3] = s[1]
        try:
            pos_dict = lemmas[s[2]]
        except KeyError:
            pos_dict = {}
        newform = strip_endings(extract_phones(s[0].lower()),endings)
        pos_dict = build_lemmas(newform,(s[1],s[3]),pos_dict)
        lemmas[s[2]] = pos_dict
    except IndexError:
        continue

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
                    outfile.write(word+'\t\t\n')
                    continue
                mylemmas = lemmas[pos]
                newword = copy(word)
                newform = strip_endings(extract_phones(newword.lower()),
                                        endings)
                currow = [0]*(len(newform)+1)
                for i in range(len(newform)+1):
                    currow[i] = i
                medlemma = []
                oedlemma = []
                i = 0
                while medlemma == []:
                    score, medlemma, oedlemma = levsearch(newform,
                                                          mylemmas,
                                                          currow,
                                                          i)
                    i += 1
                    if i > max(min((len(newword)-2),3),1):
                        break
                if medlemma == []:
                    outfile.write(word+'\t\t\n')
                else:
                    outfile.write(word+'\t'+
                                  '-~'.join(set(medlemma))+'\t'+
                                  '-~'.join(set(oedlemma))+'\n')
