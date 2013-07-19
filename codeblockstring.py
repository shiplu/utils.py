class CodeBlockString:
    """CodeBlockString finds blocks of code in a codes. If you have code string

        if(len(x)>len(y)){
            return new GreaterResultType(new GreaterParameter(x), new LesserParameter(y));
        }

    You can extract following strings from it

    1. `new GreaterParameter(x), new LesserParameter(y)`
    2. `return new GreaterResultType(new GreaterParameter(x), new LesserParameter(y));`
    3. `len(x)>len(y)`

    This is specially helpfull when you parse scripts in website (javascript) or custom
    file format that uses specific starting and ending characters.

    This will not work if the starting and ending tokens are longer than one character.

    Usage:
        # Instanciate
        cbs = CodeBlockString("if(len(x)>len(y)){ ...")
        cbs.set_start(['('])
        cbs.set_end([')'])
        block = cbs.findfrom(2)
        # block contains 'len(x)>len(y)' now

    """

    input = ''
    start = ['[', '{', '(']
    end = [']', '}', ')']
    length = 1

    def __init__(self, value):
        self.set(value)

    def set_start(self, start):
        self.start = start

    def set_end(self, end):
        self.end = end

    def set(self, value):
        self.input = list(value)
        self.length = len(value)

    def findfrom(self, index, level=1):
        """Finds string from an index

        Args:
            index: character index where the search should be started from
            level: nested level of next character in the string. Default 1

        Returns:
            The extracted code block string.

        """
        
        output = ''
        for i in range(index+1, self.length):
            if self.input[i] in self.start:
                level += 1
                output += self.input[i]
            elif self.input[i] in self.end:
                level -= 1
                if level < 1:
                    break
                output += self.input[i]
            else:
                output += self.input[i]

        return output


if __name__ == '__main__':
    # setup instances
    sample = '[hello{world+(58/589(hdl))cruel}+1+4+16+[a+b+d]]'
    indexs = '012345678901234567890123456789012345678901234567'

    print '%s\n%s\n' % (sample, indexs)
    ss = CodeBlockString(sample)

    # prepare test data
    ex = [
        (0, 'hello{world+(58/589(hdl))cruel}+1+4+16+[a+b+d]'),
        (1, 'ello{world+(58/589(hdl))cruel}+1+4+16+[a+b+d]'),
        (6, 'world+(58/589(hdl))cruel'),
        (7, 'orld+(58/589(hdl))cruel'),
        (12, '(58/589(hdl))cruel'),
        (21, 'dl'),
        (22, 'l'),
        (40, 'a+b+d')
    ]

    # run test
    for index, expectation in ex:
        result = ss.findfrom(index)
        print "Index: %02d" % index
        print "Expect: '%s'" % expectation
        print "Actual: '%s'\n%s" % (result, '=' * 40)
