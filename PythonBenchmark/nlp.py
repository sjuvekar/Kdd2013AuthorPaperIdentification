import re

stopwords = ["and", "of", "an", "in", "on", "de", "di", "li", "a", "for", "at", "the", "to", "as", "is", ""]

def filter_title(raw_title):
    name = re.split("[. ]+", raw_title.lower())
    surname = name[-1]
    return (" ".join(name), surname)

def filter_affiliation(raw_affiliation):
    camelcase_affiliation = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', raw_affiliation)
    aff_list = re.split("[|/;.\(\)\[\]$&*#+!'\" -]+|[0-9]+", camelcase_affiliation.lower())
    final_list = [x for x in aff_list if x not in stopwords]
    return " ".join(sorted(list(set(final_list))))

def filter_paper_title(raw_title):
    title_list = re.split("[|/;:.\(\)\[\]$&*#+!'\" -]+|[0-9]+", raw_title.lower())
    final_list = [x for x in title_list if x not in stopwords]
    return final_list
