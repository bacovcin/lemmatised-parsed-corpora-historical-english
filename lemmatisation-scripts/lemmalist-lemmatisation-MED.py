import progressbar
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

def extract_phones(x):
    outputs = []
    i = 0
    while i < len(x):
        if i < len(x) -1:
            if ((x[i] == '+') or (x[i] in ['t','d'] and x[i+1] == 'h')):
                nx = x[i] + x[i+1]
                outputs += [nx]
                i += 1
            else:
                outputs += x[i]
        else:
            outputs += x[i]
        i += 1
    return outputs

def levenshtein_distance(first, second):
    """Find the Levenshtein distance between two strings."""
    if len(first) > len(second):
        first, second = second, first
    if len(second) == 0:
        return len(first)
    first_length = len(first) + 1
    second_length = len(second) + 1
    distance_matrix = [[0] * second_length for x in range(first_length)]
    for i in range(first_length):
       distance_matrix[i][0] = i
    for j in range(second_length):
       distance_matrix[0][j]= j
    for i in range(1, first_length):
        for j in range(1, second_length):
            deletion = distance_matrix[i-1][j] + 1 
            insertion = distance_matrix[i][j-1] + 1 
            substitution = distance_matrix[i-1][j-1]
            if first[i-1] != second[j-1]:
                substitution += 1
            distance_matrix[i][j] = min(insertion, deletion, substitution)
    return distance_matrix[first_length-1][second_length-1]

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
            lemmas[s[2]][s[0]].append((s[1],s[3]))
        except KeyError:
            try:
                lemmas[s[2]][s[0]] = [(s[1],s[3])]
            except KeyError:
                lemmas[s[2]] = {}
                lemmas[s[2]][s[0]] = [(s[1],s[3])]
    except IndexError:
        continue

lkeys = {}
for key in lemmas:
    lkeys[key] = [x for x in set(lemmas[key].keys())]
ls = {}
for key in lemmas:
    ls[key] = [extract_phones(x.lower()) for x in lkeys[key]]
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
                mylkeys = lkeys[pos]
                myls = ls[pos]
                try:
                    medlemmas = [x[0] for x in mylemmas[word]]
                    oedlemmas = [x[1] for x in mylemmas[word]]
                except:
                    s2 = extract_phones(word.lower())
                    minlen = max(1,len(word))
                    maxlen = len(word)+1
                    medlemmas = []
                    oedlemmas = []
                    bestdist = 100000000
                    for i in range(len(myls)):
                        l = myls[i]
                        if len(l) >= minlen and len(l) <= maxlen:
                            ldist = levenshtein_distance(l,s2)
                            if ldist < bestdist:
                                medlemmas = [x[0] for x in mylemmas[mylkeys[i]]]
                                oedlemmas = [x[1] for x in mylemmas[mylkeys[i]]]
                                bestdist = ldist
                            elif ldist == bestdist:
                                medlemmas += [x[0] for x in mylemmas[mylkeys[i]]]
                                oedlemmas += [x[1] for x in mylemmas[mylkeys[i]]]
                medreals = set(medlemmas)
                oedreals = set(oedlemmas)
                outfile.write(word+'\t'+'-~'.join(medreals)+'\t'+'-~'.join(oedreals)+'\n')



