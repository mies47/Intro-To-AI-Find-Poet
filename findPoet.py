
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
            if j not in ['<s>' , '</s>'] and j in dictionary:
                dictionary[j] += 1
                counter += 1
            elif  j not in ['<s>' , '</s>']:
                dictionary[j] = 1
                counter += 1

    return (dictionary , counter)

def findUnigram(dictionary: dict, total: int):
    unigram = {}
    for i in dictionary.keys():
        unigram[i] = dictionary[i] / total
    
    return unigram
            
def findBigram(dictionary: dict)
dictionary , total = createDictionary(removeSigns(readFromFile('./train_set/molavi_train.txt')))
print(findUnigram(dictionary , total))