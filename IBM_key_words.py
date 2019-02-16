import json, collections, re
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, ConceptsOptions, KeywordsOptions

#Regexes for finding certain json strings
text_regex = re.compile(r"\"text\":.*")
value_regex = re.compile(r"\"relevance\":.*")

#Find floats
num_regex = re.compile(r"0\.\d*")


#API key constants
API_KEY = "K2vRDUoNLqNZx0cinHFMTUiOB4ja1kla6sE6mtnNH0xM"
URL = "https://gateway-wdc.watsonplatform.net/natural-language-understanding/api"


#Parse key values
def get_word_vals(text):
    start = False
    val_text = ""
    for i in range(len(text), 0, -1):
        if(text[i - 1] == "\""):
            if(start == False):
                start = True
            else:
                return val_text
        else:
            if(start):
                val_text = text[i - 1] + val_text 

#Get Key Words from IBM Cognitive
#Optional variables: The number of key words, sentiment and emotion
#Defaults are number of sentences // 2, false, and false respectively
def get_key_words(p_text, num_keys = -1, s = False, e = False):

    
    #If the number of keys is unspecified
    if(num_keys < 0):
        results = collections.Counter(p_text)
        num_keys = results["."] // 2

    #print("This will find {} keys".format(num_keys))

    #Connect to IBM Cloud
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2018-11-16',
        iam_apikey = API_KEY,
        url = URL
    )

    #Get response
    response = natural_language_understanding.analyze(
        text = p_text,
        features=Features(keywords=KeywordsOptions(sentiment=s,emotion=e,limit=num_keys))).get_result()

    #print(json.dumps(response, indent=2))

    #Get JSON info
    json_dump = json.dumps(response, indent=2)

    #Use Regex
    tmp_words = (text_regex.findall(json_dump))
    tmp_rel = (value_regex.findall(json_dump))

    #Parse the string returned from the regex
    kwrds = [get_word_vals(key_word) for key_word in tmp_words]
    keyrel = [float(num_regex.findall(relevance)[0]) for relevance in tmp_rel]

    return kwrds, keyrel

    
if __name__ == "__main__":
    #Text paragraph
    p = "The simplest among these amino acids is glycine. Glycine is the only non chiral amino acid and crystallizes in three distinct polymorphs at ambient pressures known as a-glycine, b-glycine and y-glycine. The most stable polymorph, y-glycine crystallizes in the non-centrosymmetric space group of P31 or P32, making it ideal for piezoelectricity, NLO, and photonics. While there has been extensive research done on inorganic materials such as barium titanate, polyvinylidene fluoride, softer materials such as amino acids show more promise in areas such as regenerative medicine and energy harvesting, owing to their flexibility and low polarization. In addition to having a moderate piezoelectric response, y-glycine also exhibits useful NLO properties as well, making it potentially useful in lasers, optical communications and data storage. In recent years, there have been many studies conducted on y-glycine, with the majority of the research being experimental. The explored properties include band-gap, potential for second harmonic generation, reaction under various temperatures, and different methods of crystal growth."

    words, rel = get_key_words(p)
    
