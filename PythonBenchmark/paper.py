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
        self.author_affiliations = dict()

    def add_author(self, author_id):
        self.authors[author_id] = 1

    def add_author_name(self, author_id, author_name):
        self.author_names[author_id] = author_name

    def add_author_affiliation(self, author_id, aff):
        self.author_affiliations[author_id] = aff
