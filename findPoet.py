landa = [0.002, 0.318, 0.68]
epsilon = 0.0001
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
    dictionary['<unk>'] = 0
    for i in sentences:
        for j in i.split(' '):
            if j in dictionary:
                dictionary[j] += 1
            else:
                dictionary[j] = 1
                dictionary['<unk>'] += 1
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

def backOffModel(twoWords: str , bigram: dict, unigram: dict):
    'Finds the probability of given string with landa and epsilon value'
    bigramValue = 0
    unigramValue = 0
    if twoWords in bigram:
        bigramValue = bigram[twoWords]
    if twoWords.split(' ')[0] in unigram:
        unigramValue = unigram[twoWords.split(' ')[0]]
    return ((landa[2] * bigramValue) + (landa[1] * unigramValue) + (landa[0] * epsilon))

def readTestFile():
    'Reads and filters test file'
    fo = open('./test_set/test_file.txt' , 'r' , encoding='utf-8')
    inputs = {}
    filteredInputs = {}
    for i in fo.readlines():
        line = i.split('\t')
        inputs['<s> ' + line[1].strip() + ' </s>'] = int(line[0])
    
    for i in inputs.keys():
        x = i
        x = x.replace(':' , '')
        x = x.replace('،' , '')
        x = x.replace('؟' , '')
        x = x.replace('!' , '')
        x = x.strip()
        filteredInputs[x] = inputs[i]
    
    return filteredInputs

def findAccuracy():
    #ferdowsi
    ferdowsi_sentences = readFromFile('./train_set/ferdowsi_train.txt')
    ferdowsi_sentences = removeSigns(ferdowsi_sentences)
    ferdowsi_dic , ferdowsi_counter = createDictionary(ferdowsi_sentences)
    ferdowsi_unigram = findUnigram(ferdowsi_dic , ferdowsi_counter)
    ferdowsi_bigram = findBigram(ferdowsi_sentences , ferdowsi_dic)
    print("Ferdowsi Training is completed")

    #hafez
    hafez_sentences = readFromFile('./train_set/hafez_train.txt')
    hafez_sentences = removeSigns(hafez_sentences)
    hafez_dic , hafez_counter = createDictionary(hafez_sentences)
    hafez_unigram = findUnigram(hafez_dic , hafez_counter)
    hafez_bigram = findBigram(hafez_sentences , hafez_dic)
    print("Hafez Training is completed")

    #molavi
    molavi_sentences = readFromFile('./train_set/molavi_train.txt')
    molavi_sentences = removeSigns(molavi_sentences)
    molavi_dic , molavi_counter = createDictionary(molavi_sentences)
    molavi_unigram = findUnigram(molavi_dic , molavi_counter)
    molavi_bigram = findBigram(molavi_sentences , molavi_dic)
    print("Molavi Training is completed")

    totalFerdowsi = 0
    totalHafez = 0
    totalMolavi = 0

    countedFerdowsi = 0
    countedHafez = 0
    countedMolavi = 0

    testSentences = readTestFile()

    for i in testSentences.keys():
        sentenceWord= i.split(' ')
        ferdowsi = 1.0
        molavi = 1.0
        hafez = 1.0
        for j in range(len(sentenceWord) - 1):
            twoWords = sentenceWord[j] + ' ' + sentenceWord[j + 1]
            ferdowsi *= backOffModel(twoWords , ferdowsi_bigram , ferdowsi_unigram)
            hafez *= backOffModel(twoWords , hafez_bigram , hafez_unigram)
            molavi *= backOffModel(twoWords , molavi_bigram , molavi_unigram)
        maximum = max(ferdowsi , molavi , hafez)
        if maximum == ferdowsi and testSentences[i] == 1:
            countedFerdowsi += 1
        elif maximum == hafez and testSentences[i] == 2:
            countedHafez += 1
        elif maximum == molavi and testSentences[i] == 3:
            countedMolavi += 1
        if maximum == ferdowsi:
            totalFerdowsi += 1
        if maximum == hafez:
            totalHafez += 1
        if maximum == molavi:
            totalMolavi += 1

    print("Ferdowsi Accuracy is: " , countedFerdowsi / totalFerdowsi * 100)
    print("Hafez Accuracy is: " , countedHafez / totalHafez * 100)
    print("Molavi Accuracy is: " , countedMolavi / totalMolavi * 100)



findAccuracy()