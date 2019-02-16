import nltk, gensim
from compare_text import split_paragraphs
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()

# Pre-processing
def preprocess(sentence):
    #Short sentence removal
    if len(sentence) < 3:
        return None 
    
    arr = word_tokenize(sentence)
    arr1 = []
    for word in arr:
        if len(word) >= 3 and word not in gensim.parsing.preprocessing.STOPWORDS: #stopword + shortword removal
            arr1.append(ps.stem(word)) #stem
    return arr1

def evaluate_text():
    paragraphs = split_paragraphs("/tmp/text.txt") #Splits the text into topic based paragraphs
    processed_paragraphs = []

    for paragraph in paragraphs:
        sentences = sent_tokenize(paragraph)
        new_paragraph = []
        for sentence in sentences:
            new_paragraph.append(preprocess(sentence))
        processed_paragraphs.append(new_paragraph) #preprocesses each sentence in each paragraph

    finalps = [] #final paragraph sentences
    #frequencies for each word in each paragraph
    for i in range(0,len(processed_paragraphs)):
        paragraph = processed_paragraphs[i]
        wordfreq = {}
        for sentence in paragraph:
            for word in sentence:
                for s in paragraph:
                    wordfreq[word] = sum(x.count(word) for x in s) #counts frequency of word in paragraph
        wordfreq[word]
        word_max = max(wordfreq.keys(), key=(lambda k: wordfreq[k])) #word with highest frequency
        maximum = wordfreq[word_max] #maximum frequency
        wweight = {}
        for key in wordfreq:
            wweight[key] = wordfreq[key]/maximum #weights of each word
        sentence_weights = []
        for sentence in paragraph:
            sweight = 0 
            for word in sentence:
                sweight += wweight[word] #sentence weight is the sum of the weights of each word in the sentence
            sentence_weights.append(sweight)
        finalp = []
        sentences = sent_tokenize(paragraphs[i]) #takes sentences from original text (non processed)
        finalp = [x for _,x in sorted(zip(sentence_weights,sentences))] #sorts sentences in order of their weight (least to greatest)
        finalps.append(finalp)
    return finalps