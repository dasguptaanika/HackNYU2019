#Get module stuff
from compare_text import *
from IBM_key_words import get_key_words, get_main_idea
from text_evaluate import evaluate_text
from bullet_point import bullet_point

from textToPdf import textToPdf

#Remove conjunctions from bullet points
conj = ['accordingly', 'furthermore', 'moreover', 'similarly', 'also', 'hence', 'namely', 'still', 'anyway', 'however', 'nevertheless', 'then', 'besides', 'incidentally', 'next', 'thereafter', 'certainly', 'indeed', 'nonetheless', 'therefore', 'consequently', 'instead', 'now', 'thus', 'finally', 'likewise', 'otherwise', 'undoubtedly', 'further', 'meanwhile', 'after', 'although', 'as', 'as if', 'as though', 'because', 'before', 'even if', 'even though', 'if', 'in case', 'once', 'only if', 'provided that', 'since', 'so that', 'than', 'that', 'though', 'till', 'unless', 'untill', 'when', 'whenever', 'where', 'wherever', 'while', 'for', 'and', 'nor', 'but', 'or', 'yet', 'so']

#Get rid of punctuation when checking for conjunctions
translator = str.maketrans('', '', string.punctuation)

#Don't repeat headers
all_keys = []
output_str = ""

#Print bullet given paragraph
def prt_bullet(p):
    global all_keys, output_str #global

    #Get the header from IBM
    idea = get_main_idea(p)

    #If new header
    if(idea.lower() not in " ".join(all_keys)):
        tmp_bullet = bullet_point(idea)
        #If IBM returns nothing
        if(idea.lower() != "n/a"):
            all_keys.append(idea.lower())
    else:
        tmp_bullet = bullet_point("")

    #Second column
    s_rank = []
    #If the paragraph is > 2 sentences long
    if(len(p) > 2):
        #Join the sentences
        full_text = " ".join(p)

        #Get key words from IBM. The relevance fro the words aren't needed yet
        key_words, _ = get_key_words(full_text)

        #print("Confidence: {}".format(_))

        #Reset the local variable (In case python's gc doesn't do the trick)
        tmp_bullet.reset()

        #Loop through key words
        for k in key_words:
            if(k in all_keys):
                #If the key word is repeated
                k = k + "cont."
            #Add to second column
            tmp_bullet.add_s_rank(k.capitalize())
            s_rank.append(k)
            all_keys.append(k.lower())

        #Get the most relevant key word for each header section
        for i in range(len(p) // 2):
            #Use cosine similarity
            max_cos_sim = 0
            index = -1

            #temp sentence
            tmp_sentence = p[i]

            #More preprocessing
            current_sentence = preprocess(" ".join(normalize(tmp_sentence)))
            #Get the most relevant key word
            for k in key_words:
                tmp_k = preprocess(" ".join(normalize(k)))
                c_sim = cosine_sim(combine_lists(current_sentence), combine_lists(tmp_k))
                if(c_sim > max_cos_sim):
                    max_cos_sim = c_sim
                    try:
                        index = s_rank.index(k)
                    except ValueError:
                        pass

            #Get rid of the conjunctions
            arr_tmp = tmp_sentence.split(" ")
            if(arr_tmp[0].translate(translator).lower() in conj):
                arr_tmp.pop(0)

            #Properly capitalize
            arr_tmp[0] = arr_tmp[0].capitalize()    
            
            tmp_bullet.add_t_rank(" ".join(arr_tmp), index)

        #Print out the "bulleted list"
        temp_out = tmp_bullet.to_string()
        if(temp_out != ""):
            output_str += temp_out + "\n"

    else:
        #If the paragraph is short, simply append the sentences w/ out a third column
        for sentence in p:

            #Get rid of conjunctions
            arr_tmp = sentence.split(" ")
            if(arr_tmp[0].translate(translator).lower() in conj):
                arr_tmp.pop(0)

            arr_tmp[0] = arr_tmp[0].capitalize()

            tmp_bullet.reset()

            tmp_bullet.add_s_rank(" ".join(arr_tmp))
        #Print out the bulleted list    
        temp_out = tmp_bullet.to_string()
        if(temp_out != ""):
            output_str += temp_out + "\n"

    #Reset at end
    tmp_bullet.reset()

    
#Main method, loops through the paragraphs and gets bulleted list for each
def main_nlp():
    global output_str
    sorted_paragraphs = evaluate_text()
    for i in range(len(sorted_paragraphs)):
        prt_bullet(sorted_paragraphs[i])

    #print(output_str.rstrip())
    print(output_str.rstrip())

    with open("inter.txt", "w") as f:
        f.write(output_str.rstrip())

    textToPdf("inter.txt")
    

if __name__ == "__main__":
    main_nlp()
        
