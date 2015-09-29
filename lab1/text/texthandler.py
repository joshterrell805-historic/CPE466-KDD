class Reader:
    sentenceTerminators = ['.', '!', '?']
    wordSeparators = [',', '-', ':', ';', '(', ')', '\'', '"', '...', ' ', '\n']
    wordSeparators.extend(sentenceTerminators)
    innerWordNonBreakingPunct = ['-', '\'']
    paragraphSeparators = ['\n\n']
    buffSize = 64

    def __init__(self, fileHandle):
        """Each reader should be initialized with a unique file handle"""
        self.fileHandle = fileHandle
        self.buff = ''
        self.eof = False
        self.iterType = None

    def __iter__(self):
        return self

    def __next__(self):
        raise Exception("__next__ is not implemented in Reader")

    def readMore(self):
        if not self.eof:
            buff = self.fileHandle.read(self.buffSize)
            if len(buff) == 0:
                self.eof = True
            self.buff += buff

class ParagraphReader(Reader):
    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        paragraph = None
        while paragraph is None:
            self.readMore()
            sep = None
            index = -1
            for s in self.paragraphSeparators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                paragraph = self.buff[:index]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                paragraph = self.buff
                self.buff = ''
        return paragraph

class SentenceReader(Reader):
    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        sentence = None
        while sentence is None:
            self.readMore()
            sep = None
            index = -1
            for s in self.sentenceTerminators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                sentence = self.buff[:endIndex]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                sentence = self.buff
                self.buff = ''
        return sentence.lstrip()

class WordReader(Reader):
    def __next__(self):
        if self.eof and len(self.buff) == 0:
            raise StopIteration()
        word = None
        while word is None:
            # TODO this should probably only be called if nothing is found
            # (in each of the reader classes)
            self.readMore()
            sep = None
            index = -1
            for s in self.wordSeparators:
                idx = self.buff.find(s)
                if idx != -1 and (index == -1 or idx < index):
                    if s in self.innerWordNonBreakingPunct:
                        # "sup chief-man"
                        #           ^
                        self.readMore()
                        if len(self.buff) > idx + 1:
                            if self.buff[idx+1] == ' ':
                                s += ' '
                            elif idx == 0:
                                self.buff = self.buff[1:]
                                return self.__next__()
                            else:
                                continue
                    index = idx
                    sep = s
            if index != -1:
                endIndex = index + len(sep)
                word = self.buff[:index]
                self.buff = self.buff[endIndex:]
            elif self.eof:
                word = self.buff
                self.buff = ''
        word = word.strip()
        return self.__next__() if word == '' else word

    def uniqWordsRead(self):
        pass

    def freqWordsMap(self):
        pass

    def countWords(self):
        pass

    def countUniqWords(self):
        pass

    def countSentences(self):
        pass

    def countParagraphs(self):
        pass

    def mostFreqWords(self):
        pass

    def wordsWithFreq(self, freq):
        pass

    def wordsWithGreaterFreq(self, freq):
        pass

    def wordFound(self, word):
        pass
