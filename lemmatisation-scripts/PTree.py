class PTree:
    def __init__(self, name, content):
        if type(name) is str and ' ' not in name:
            self.name = name
        else:
            print("Name is not a string")
        self.content = content
        self.height = 0
        if type(content) is list:
            for tree in content:
                if tree.height >= self.height:
                    self.height = tree.height + 1

    def __str__(self):
        if (type(self.content) is str):
            output = '\n(' + self.name + ' ' + self.content + ')'
        else:
            output = '\n(' + self.name
            for y in self.content:
                text = str(y).split('\n')
                output = output + '\n  '.join(text)
            output = output + '\n)'
        return output


def MatchParen(x):
    output = []
    outtext = ''
    i = 0
    while i < len(x):
        c = x[i]
        if c == '(':
            if outtext not in [' ', '', '\t']:
                output.append(outtext)
            outtext = ''
            y = MatchParen(x[i+1:])
            output.append(y[0])
            i = i+y[1]
        elif c == ')':
            if outtext not in [' ', '']:
                output.append(outtext)
            break
        else:
            outtext = outtext + c
            i = i + 1
    return (output, i+2)


def ParseTree(x):
    if len(x) > 1 or type(x[0]) is list:
        try:
            name = x[0].rstrip()
            start = 1
        except:
            name = ''
            start = 0
        content = []
        for y in x[start:]:
            if type(y) is list:
                content.append(ParseTree(y))
            else:
                content.append(y)
    else:
        y = x[0].split(' ')
        name = y[0]
        content = y[1]
    return PTree(name, content)


def ParseFiles(argvs):
    toklist = {}
    for i in range(len(argvs)):
        arg = argvs[i]
        if arg[-3:] in ['ref', 'psd']:
            print(arg)
            file = open(arg)
            tokens = []
            token = ''
            for line in file:
                if line == '\n' and 'ID' in token:
                    tokens.append(ParseTree(MatchParen(token.lstrip().rstrip())
                                            [0][0]))
                    token = ''
                elif line == '\n':
                    token = ''
                else:
                    token = token + line.rstrip().lstrip()
                toklist[arg[:-4]] = tokens
    return toklist
