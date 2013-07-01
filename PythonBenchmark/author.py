import paper

class Author:

    def __init__(self, _id, _name, _surname, _affiliation):
        self.id = _id
        self.name = _name
        self.surname = _surname
        self.affiliation = _affiliation
        
        #Features
        self.num_papers = 0
        self.num_conference_papers = 0
        self.num_journal_papers = 0

        self.paper_title_words = dict()
        self.all_keywords = dict()
        self.all_conferences = dict()
        self.all_journals = dict()
        self.all_years = dict()
        self.all_papers = dict()     

    def _update_dict(self, d, key, value):
        try:
            d[key] = d[key] + value
        except:
            d[key] = value
    
    def num_conferences(self):
        return len(self.all_conferences.keys())

    def num_journals(self):
        return len(self.all_journals.keys())

    def num_years(self):
        return len(self.all_years.keys())

    def update_conferences(self, conference_id):
        self._update_dict(self.all_conferences, conference_id, 1)

    def update_journals(self, journal_id):
        self._update_dict(self.all_journals, journal_id, 1)

    def update_years(self, year_id):
        self._update_dict(self.all_years, year_id, 1)

    def update_paper(self, pap):
        if not pap:
            return
        #if pap.id in self.all_papers.keys():
        #    return
        #self.all_papers[pap.id] = 1

        self.num_papers += 1
        self.update_years(pap.year)
        if pap.conference_id > 0:
            self.num_conference_papers += 1
            self.update_conferences(pap.conference_id)
        elif pap.journal_id > 0:
            self.num_journal_papers += 1
            self.update_journals(pap.journal_id)
        
        # Update paper titles and keywords
        for w in pap.title.split():
            try:
              self.paper_title_words[w] = self.paper_title_words[w] + 1
            except:
              self.paper_title_words[w] = 1

        for w in pap.keywords.split():
            try:
              self.all_keywords[w] = self.all_keywords[w] + 1
            except:
              self.all_keywords[w] = 1


    def key(self):
        return self.name + " " + self.affiliation
