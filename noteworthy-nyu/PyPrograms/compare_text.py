import nltk, string, gensim
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

import re

#Remove unicode
unicode_regex = re.compile(r"\\u\w\w\w\w")

#Queue is needed for BFS, so not used
#from queue import *

#Constants for similarity
SIM_CONST = 0.77 #contrived through exhaustive search (very suspicious :P)
SIM_CONST_AVG = 0.5 #Also contrived

#dictionary to revert back to old sentences
o_stem = {}

#lemmatization
stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

#Helper method for preprocess
def lemmatize_stemming(text):
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos='v'))

#Tokenize and lemmatize (oops did this twice) a single sentence
def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
            
    return result

#get the stems of words
def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]

#Get rid of all punctuation
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

#Find the cosine similarity between two sentences using tfid
def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]

#Split list into 2 separate pieces (WAS FOR BFS METHOD, NOT USED)
def split_list(l):
    half = len(l) // 2
    return l[:half], l[half:]

#Combines a list into strings
#This is used for comparing the text with tfid
#I don't think this method is necessary because the lists
#can be compared directly, but I don't want to
#change my similarity constants, as it seems to be fine as of now
def combine_lists(l):
    #new list
    combined_list = []
    #add the words
    for i in l:
        combined_list += i

    #return string
    return " ".join(combined_list)

#vectorizer for comparing the sentences
#placing is weird, but it works (needs to be after normalize but before
#the main method)
vectorizer = TfidfVectorizer(tokenizer=normalize)

#Actual splitting method
def split_paragraphs(filename):

    #get text from the text files
    with open(filename) as f:
        
        data = f.read()
        data = unicode_regex.sub("", data)

        #print(data)

        #list of sentences
        sent_tokenize_list = sent_tokenize(data)

        #preprocessing for the sentences
        processed_sentences = []
        for sentence in sent_tokenize_list:
             tmp = preprocess(" ".join(normalize(sentence)))
             o_stem[" ".join(tmp)] = sentence
             if(len(tmp) != 0):
                 processed_sentences.append(tmp)
                 #print(tmp)

    #Output for error checking
        
    #print(o_stem)
    #print()
    #print("-" * 20)

    paragraphs = []

    #exhaustive comparison between each sentence. Find out the average "similarity"
    #in each paragraph and add to the paragraph accordingly
    #O(n^2)
    for sentence in processed_sentences:
        #Average similarity
        max_avg_sim = 0
        #Index to add the sentence to
        index = -1
        #loop through each paragraph
        for i, section in enumerate(paragraphs):
            avg = 0
            num = 0
            #loop through each sentence in the paragraph
            for s in section:
                
                #find cosine similarity
                c_sim = cosine_sim(combine_lists(sentence), combine_lists(s))

                #More error checking
                #print(c_sim)
                #print(sentence)
                #print(s)

                #if the similarity is high enough, add to the average
                if(c_sim > SIM_CONST):
                    avg += c_sim
                #incremment number of passes
                num += 1
            #Find the average
            avg /= (float(num))
            #Find the corresponding index
            if(avg > max_avg_sim and avg > 0.5):
                index = i
        #If the sentence doesn't fit a current paragraph
        if(index == -1):
            paragraphs.append([sentence])
        #add sentence to paragraph
        else:
            paragraphs[i].append(sentence)

    #print(paragraphs)

    #print("There were {} paragraphs found\n".format(len(paragraphs)))

    #Convert back to plain text
    plain_text_paragraph = []

    #loop through and do proper mapping
    for p in paragraphs:
        tmp = ""
        for i in p:
            tmp += o_stem[" ".join(i)] + " "

        plain_text_paragraph.append(tmp[:len(tmp) - 1])
        #print(tmp[:len(tmp) - 1] + "\n")        
                
    #BFS Method (Does not work as well, but is much faster - O(nlogn))

    """#BFS to get paragraphs

    paragraphs = []

    #TfidVectorizer for comparisons
    vectorizer = TfidfVectorizer(tokenizer=normalize)

    q = Queue(maxsize = 0)

    t1, t2 = split_list(processed_sentences)

    #print(cosine_sim(combine_lists(t1), combine_lists(t2)))

    if(cosine_sim(combine_lists(t1), combine_lists(t2)) < SIM_CONST ):
        q.put(t1)
        q.put(t2)

    while(not(q.empty())):
        lists_to_check = q.get()

        t1, t2 = split_list(lists_to_check)

        #print(cosine_sim(combine_lists(t1), combine_lists(t2)))

        if(cosine_sim(combine_lists(t1), combine_lists(t2)) < SIM_CONST and len(t1) > 1 and len(t2) > 1):
            q.put(t1)
            q.put(t2)
        else:
            for(int i = 0, i)
            paragraphs.append("{} {}".format(o_stem[combine_lists(t1)], o_stem[combine_lists(t2)]))

    print(paragraphs)"""

    #Return plaintext list
    return plain_text_paragraph

if __name__ == "__main__":
    ret = split_paragraphs("test.txt")
    #print(ret)
    

    
    

    
