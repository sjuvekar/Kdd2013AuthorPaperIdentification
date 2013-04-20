class Paper:
    
    def __init__(self, _id, title, year, conference_id, journal_id, keywords):
        self.id = _id
        #TODO
        #self.title = title
        #
        self.year = year
        self.conference_id = conference_id
        self.journal_id = journal_id
        #TODO
        self.keywords = keywords
        #
        self.authors = dict()

    def add_author(self, author_id):
        self.authors[author_id] = 1
