import re

stopwords = ["and", "of", "an", "in", "on", "de", "di", "li", "a", "for", "at", "the", "to", "as", "is", "by", ""]
regexp_string = "[|/:;.\(\)\[\]$&*#+!'\" ?\xe2\x80\x93-]+|[0-9]+"
regex_replace = "\xcc|\x81"
camelcase_string = '(.)([A-Z][a-z]+)'
surnames = ["parthasarathy", "ng"]


def filter_title(raw_title):
    #raw_title_lower = re.sub(regex_replace, "", raw_title.lower())
    name = re.split("[. ]+", raw_title.lower())
    name = map(lambda a: a.strip(), name)
    surname = name[-1]
    for s in surnames:
      if s in name:
        surname = s
    return (" ".join(name), surname)

def filter_generic(raw_string, camelcase_filter=False):
    if camelcase_filter:
      camelcase_output = re.sub(camelcase_string, r'\1 \2', raw_string)
    else:
      camelcase_output = raw_string
    int_list = re.split(regexp_string, camelcase_output.lower())
    final_list = [x for x in int_list if x not in stopwords]
    return " ".join(sorted(list(set(final_list))))

def filter_affiliation(raw_affiliation):
    return filter_generic(raw_affiliation, True)

def filter_paper_title(raw_title):
    return filter_generic(raw_title)

def filter_paper_keyword(raw_keyword):
    return filter_generic(raw_keyword)
