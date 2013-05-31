class Paper:
    
    def __init__(self, _id, title, year, conference_id, journal_id, keywords):
        self.id = _id
        self.title = title
        self.year = year
        self.conference_id = conference_id
        self.journal_id = journal_id
        self.keywords = keywords
        
        self.authors = dict()
        self.author_names = dict()
        self.author_name_duplicate = dict()
        self.author_affiliations = dict()
        self.author_affiliation_duplicate = dict()

        if self.journal_id == 0 and self.conference_id == 0:
          self.both_zero = 1
        elif self.journal_id <= 0 and self.conference_id <= 0:
          self.both_zero = -1
        else:
          self.both_zero = 0

        if self.year <= 0:
          self.year_zero = 1
        else:
          self.year_zero = 0

        if self.title == "":
          self.title_zero = 1
        else:
          self.title_zero = 0


    def add_author(self, author_id):
        self.authors[author_id] = 1

    def add_author_name(self, author_id, author_name):
        if author_id not in self.author_name_duplicate.keys():
          self.author_name_duplicate[author_id] = 0
        if author_id in self.author_names.keys():
          if author_name in self.author_names[author_id]:
            self.author_name_duplicate[author_id] = self.author_name_duplicate[author_id] + 1
          else:
            self.author_names[author_id] = self.author_names[author_id] + [author_name]
        else:
          self.author_names[author_id] = [author_name]

    def add_author_affiliation(self, author_id, aff):
        if author_id not in self.author_affiliation_duplicate.keys():
          self.author_affiliation_duplicate[author_id] = 0
        if aff == "":
          return
        if author_id in self.author_affiliations.keys():
          if aff in self.author_affiliations[author_id]:
            self.author_affiliation_duplicate[author_id] = 1
          else:
            self.author_affiliations[author_id] = self.author_affiliations[author_id] + [aff]
        else:
          self.author_affiliations[author_id] = [aff]
