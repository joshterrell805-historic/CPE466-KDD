class Reader:
    sentenceTerminators = ['.', '!', '?']
    wordSeparators = [',', '-', ':', ';', '(', ')', '\'', '"', '...', ' ']
    innerWordChars = ['-', '\'']
    paragraphSeparators = ['\n\n']
    buffSize = 64

    def __init__(self, fileHandle):
        """Each reader should be initialized with a unique file handle"""
        self.fileHandle = fileHandle
        self.buff = ''
        self.eof = False
        self.iterType = None

    def __iter__(self):
        if self.iterType is None:
            raise Exception(
                    'Call paragraphReader, sentenceReader, or wordReader first')
        return self

    def __next__(self):
        fn = getattr(self, 'next' + self.iterType)
        return fn()

    def readMore(self):
        if not self.eof:
            buff = self.fileHandle.read(self.buffSize)
            if len(buff) == 0:
                self.eof = True
            self.buff += buff

    def paragraphReader(self):
        self.iterType = 'Paragraph'
        return self

    def sentenceReader(self):
        self.iterType = 'Sentence'
        return self

    def nextParagraph(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        paragraph = None
        while paragraph is None:
            self.readMore()
            sep = None
            index = -1
            for sep in self.paragraphSeparators:
                index = self.buff.find(sep)
                if index != -1:
                    break
            if index != -1:
                endIndex = index + len(sep)
                paragraph = self.buff[:index]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                paragraph = self.buff
                self.buff = ''
        return paragraph

    def nextSentence(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        sentence = None
        while sentence is None:
            self.readMore()
            sep = None
            index = -1
            for sep in self.sentenceTerminators:
                index = self.buff.find(sep)
                if index != -1:
                    break
            if index != -1:
                endIndex = index + len(sep)
                sentence = self.buff[:endIndex]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                sentence = self.buff
                self.buff = ''
        return sentence.lstrip()

