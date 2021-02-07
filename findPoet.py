
def readFromFile(path: str):
    'Reads all lines of specified file'
    fo = open(path , 'r' , encoding='utf-8')
    inputs = []
    for i in fo.readlines():
        inputs.append('<s> ' + i.strip() + ' </s>')

    return inputs

def removeSigns(sentences: list):
    'Remove all . ، ? / ! signs from sentences'
    for i in range(len(sentences)):
        sentences[i] = sentences[i].replace(':' , '')
        sentences[i] = sentences[i].replace('،' , '')
        sentences[i] = sentences[i].replace('؟' , '')
        sentences[i] = sentences[i].replace('!' , '')
        sentences[i] = sentences[i].replace(':' , '')
        sentences[i] = sentences[i].strip()
        
    return sentences

def createDictionary(sentences: list):
    'Find and return dictionary of all words'
    dictionary = {}
    counter = 0
    for i in sentences:
        for j in i.split(' '):
            if j in dictionary:
                dictionary[j] += 1
            else:
                dictionary[j] = 1
            if j not in ['<s>' , '</s>']:
                counter += 1

    return (dictionary , counter)

def findUnigram(dictionary: dict, total: int):
    'Finds and returns the probability of each key of dictionary'
    unigram = {}
    for i in dictionary.keys():
        if i not in ['<s>' , '</s>']:
            unigram[i] = dictionary[i] / total
    
    return unigram

def findBigram(sentences: list , dictionary: dict):
    'Finds and returns the probability of any two consecutive words'
    bigramWords = {}
    bigram = {}
    for i in sentences:
        sentenceWords = i.split(' ')
        for j in range(len(sentenceWords) - 1):
            twoWords = sentenceWords[j] + ' ' + sentenceWords[j+1]
            if twoWords in bigramWords:
                bigramWords[twoWords] += 1
            else:
                bigramWords[twoWords] = 1

    for i in bigramWords:
        lastWord = i.split(' ')[1]
        bigram[i] = bigramWords[i] / dictionary[lastWord]

    return bigram
            
# def findBigram(dictionary: dict)
dictionary , total = createDictionary(removeSigns(readFromFile('./train_set/molavi_train.txt')))
print(findUnigram(dictionary , total))