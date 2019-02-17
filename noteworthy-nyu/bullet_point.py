#SpaCy
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = en_core_web_sm.load()

class bullet_point:
    f_rank = ""
    s_rank = []
    t_rank = {}
    def __init__(self, header):
        self.f_rank = header
    def add_s_rank(self, text):
        self.s_rank.append(text)
    def add_t_rank(self, text, index):
        if(str(index) in self.t_rank):
            t = self.t_rank[str(index)]
            t.append(text)
            self.t_rank[str(index)] = t
        else:
            self.t_rank[str(index)] = [text]

    def to_string(self):
        return_str = ""
        header_nlp = nlp(self.f_rank)
        labels = [x.label_ for x in header_nlp.ents]
        if(self.f_rank != "N/A" and "PERSON" not in labels):
            if(self.f_rank != ""):
                return_str += "\n~" + self.f_rank
            for index, val in enumerate(self.s_rank):
                person = False
                names = []
                if(not self.t_rank):
                    return_str += "\n`" + ("\t" + val)
                else:
                    val_list = val.split(" ")
                    for elm in val_list:
                        apply_nlp = nlp(elm)
                        labels = [x.label_ for x in apply_nlp.ents]
                        if("PERSON" in labels):
                            person = True
                            names.append(elm)
                    
                    #print 3rd rank
                    if(str(index) in self.t_rank):
                        sub_bullets = self.t_rank[str(index)]
                        
                        if(person == False or any(n in " ".join(sub_bullets) for n in names)):
                            return_str += "\n`" + ("\t" + val)
                            for b in sub_bullets:
                                return_str += ("\n@\t\t" + b)
        return return_str
    
    
    def check_person(self, person):
        pass

    def reset(self):
        self.s_rank = []
        self.t_rank = {}
