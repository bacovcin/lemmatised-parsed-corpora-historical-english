import os


def recombine(corpus):
    # Since PYCCLE and MorphAdorn have different chunking, for each text
    # associate every character of the original text with its
    # PYCCLE/MorphAdorner chunk. Then extract each MorphAdorner chunk and
    # combine any relevant PYCCLE POS tags associated with characters in that
    # chunk

    # Start by getting a list of original PYCCLE texts and lemmatised output
    texts = os.listdir('./' + corpus + '-texts')
    lemmatised_texts = os.listdir('./' + corpus + '-out')
    completenum = 0  # Track number of texts recombined
    fullnum = len(texts)  # Count complete number of texts

    # Go through every text
    for filename in lemmatised_texts:
        # Print current progress
        print('{0:.2f}% Complete'.format((float(completenum) /
                                          float(fullnum)) * 100))
        completenum += 1
        # Make sure file exists in both folders
        if filename in texts:
            # Load files (including output file)
            lemma_file = open('./' + corpus + '-out/'+filename)
            orig_file = open('./' + corpus + '-texts/'+filename)
            new_file = open('./' + corpus + '-final/'+filename, 'w')

            # Associate every original character with MorphAdorner chunk
            lemma_chars = ''
            lemmas = []
            lemma_states = []
            for line in lemma_file:
                s = line.rstrip().split('\t')
                lemma_chars += s[0]
                lemmas.append(s)
                lemma_states += [len(lemmas)-1] * len(s[0])

            # Associate every original character with PYCCLE chunk
            orig_chars = ''
            origs = []
            orig_states = []
            for line in orig_file:
                s = line.rstrip().split('\t')
                orig_chars += s[0]
                origs.append(s)
                orig_states += [len(origs)-1] * len(s[0])

            # Check that no alteration to original text has occurred
            if lemma_chars != orig_chars:
                raise ValueError('The two texts are different!!!')

            # Run through text outputting every MorphAdorner chunk
            cur_origs = []  # List of PYCCLE POS chunks encountered
            cur_lemma = 0  # Current MorphAdorner lemma
            cur_word = ''  # Current original text
            for i in range(len(lemma_chars)):
                if lemma_states[i] != cur_lemma:
                    # New MorphAdorner chunk: write out current data and reset
                    # variables for tracking next chunk
                    l = lemmas[cur_lemma]
                    orig_pos = '+'.join([origs[x][1] for x in cur_origs])
                    output = cur_word + '\t' + l[3] + '\t' + l[4] + '\t' + l[2] + '\t' + orig_pos + '\n'
                    new_file.write(output)
                    # Check if new token has been reached, if so add empty line
                    if l[-1] == '1':
                        new_file.write('\n')
                    cur_origs = []
                    cur_lemma = lemma_states[i]
                    cur_word = ''
                if orig_states[i] not in cur_origs:
                    # New PYCCLE chunk: add chunk to PYCCLE list
                    cur_origs.append(orig_states[i])
                # Add current character to current word
                cur_word += lemma_chars[i]
    return


if __name__ == "__main__":
    recombine('eebo')  # Recombine EEBO materials
    recombine('ecco')  # Recombine ECCO materials
