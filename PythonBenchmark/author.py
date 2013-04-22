import paper

class Author:

    def __init__(self, _id, _name, _affiliation):
        self.id = _id
        self.name = _name
        self.affiliation = _affiliation
        
        #Features
        self.num_papers = 0
        self.num_conference_papers = 0
        self.num_journal_papers = 0
        self.num_coauthors = 0
        self.num_years = 0
        
        self.num_positive_papers = 0
        self.num_positive_conference_papers = 0
        self.num_positive_journal_papers = 0
        self.num_positive_coauthors = 0
        self.num_positive_years = 0
        
        self.num_negative_papers = 0
        self.num_negative_conference_papers = 0
        self.num_negative_journal_papers = 0
        self.num_negative_coauthors = 0
        self.num_negative_years = 0
        
        self.all_keywords = dict()
        self.positive_keywords = dict()
        self.negative_keywords = dict()
        
        self.all_coauthors = dict()
        self.positive_coauthors = dict()
        self.negative_coauthors = dict()

        self.all_conferences = dict()
        self.positive_conferences = dict()
        self.negative_conferences = dict()
        
        self.all_journals = dict()
        self.positive_journals = dict()
        self.negative_journals = dict()

        self.all_years = dict()
        self.positive_years = dict()
        self.negative_years = dict()
        
    def _update_dict(self, d, key, value):
        if key in d.keys():
            d[key] = d[key] + value
        else:
            d[key] = value
            
    def update_conferences(self, conference_id):
        self._update_dict(self.all_conferences, conference_id, 1)

    def update_positive_conferences(self, conference_id):
        self._update_dict(self.positive_conferences, conference_id, 1)
        
    def update_negative_conferences(self, conference_id):
        self._update_dict(self.negative_conferences, conference_id, 1)
        
    def update_journals(self, journal_id):
        self._update_dict(self.all_journals, journal_id, 1)

    def update_positive_journals(self, journal_id):
        self._update_dict(self.positive_journals, journal_id, 1)
        
    def update_negative_journals(self, journal_id):
        self._update_dict(self.negative_journals, journal_id, 1)

    def update_coauthors(self, coauthor_id):
        self._update_dict(self.all_coauthors, coauthor_id, 1)

    def update_positive_coauthors(self, coauthor_id):
        self._update_dict(self.positive_coauthors, coauthor_id, 1)
        
    def update_negative_coauthors(self, coauthor_id):
        self._update_dict(self.negative_coauthors, coauthor_id, 1)
    
    def update_years(self, year_id):
        self._update_dict(self.all_years, year_id, 1)

    def update_positive_years(self, year_id):
        self._update_dict(self.positive_years, year_id, 1)
        
    def update_negative_years(self, year_id):
        self._update_dict(self.negative_years, year_id, 1)

    def update_paper(self, pap):
        self.num_papers += 1
        self.num_years += 1
        if not pap:
            return
        self.update_years(pap.year)
        if pap.conference_id != 0:
            self.num_conference_papers += 1
            self.update_conferences(pap.conference_id)
        if pap.journal_id != 0:
            self.num_journal_papers += 1
            self.update_journals(pap.journal_id)

    def update_positive_paper(self, pap):
        self.num_positive_papers += 1
        self.num_positive_years += 1
        if not pap:
            return
        self.update_positive_years(pap.year)
        if pap.conference_id != 0:
            self.num_positive_conference_papers += 1
            self.update_positive_conferences(pap.conference_id)
        if pap.journal_id != 0:
            self.num_positive_journal_papers += 1
            self.update_positive_journals(pap.journal_id)

    def update_negative_paper(self, pap):
        self.num_negative_papers += 1
        self.num_negative_years += 1
        if not pap:
            return
        self.update_negative_years(pap.year)
        if pap.conference_id != 0:
            self.num_negative_conference_papers += 1
            self.update_negative_conferences(pap.conference_id)
        if pap.journal_id != 0:
            self.num_negative_journal_papers += 1
            self.update_negative_journals(pap.journal_id)
