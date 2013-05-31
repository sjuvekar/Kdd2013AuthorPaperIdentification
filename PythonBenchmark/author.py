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

        self.all_keywords = dict()
        self.all_conferences = dict()
        self.all_journals = dict()
        self.all_years = dict()
        
    def _update_dict(self, d, key, value):
        if key in d.keys():
            d[key] = d[key] + value
        else:
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
        self.num_papers += 1
        self.update_years(pap.year)
        if pap.conference_id > 0:
            self.num_conference_papers += 1
            self.update_conferences(pap.conference_id)
        if pap.journal_id > 0:
            self.num_journal_papers += 1
            self.update_journals(pap.journal_id)
