import author
import paper
import numpy

class Feature:
    
    def __init__(self, parser):
        self.parser = parser
        
    def create_author_based_features(self, auth):
        ret = []
        #Number of papers
        num_papers = auth.num_papers
        num_conference_papers = auth.num_conference_papers
        num_journal_papers = auth.num_journal_papers
        ret = ret + [num_papers, num_conference_papers, num_journal_papers]
        
        # Number of conferences/journals
        num_conferences = auth.num_conferences()
        num_journals = auth.num_journals()
        num_years = auth.num_years()
        ret = ret + [num_conferences, num_journals, num_years]

        # Title based
        num_people_with_surname = self.parser.surnames.get(auth.surname) or 0
        ret = ret + [num_people_with_surname]

        # Affiliation based
        num_people_with_affiliation = self.parser.affiliations.get(auth.affiliation) or 0
        ret = ret + [num_people_with_affiliation]

        return ret
        
    def create_paper_based_features(self, pap):
        num_authors = len(pap.authors.keys())
        num_papers = 0
        num_conference_papers = 0
        num_journal_papers = 0
        num_conferences = 0
        num_journals = 0
        num_papers_in_year = 0
        year = pap.year
        num_papers_in_conf_or_journal = 0
        conf_or_journal = 0

        for auth_id in pap.authors.keys():
          auth = self.parser.authors.get(auth_id)
          if not auth:
            continue
          num_papers += auth.num_papers
          num_conference_papers += auth.num_conference_papers
          num_journal_papers += auth.num_journal_papers
          num_conferences += auth.num_conferences()
          num_journals += auth.num_journals()
          num_papers_in_year += (auth.all_years.get(year) or 0)
          if pap.conference_id == 0:
            num_papers_in_conf_or_journal += (auth.all_journals.get(pap.journal_id) or 0)
            conf_or_journal = 1
          else:
            num_papers_in_conf_or_journal += (auth.all_conferences.get(pap.conference_id) or 0)
            conf_or_journal = 0
            
        return [num_authors, num_papers, num_conference_papers, num_journal_papers, num_conferences, num_journals, num_papers_in_year, num_papers_in_conf_or_journal, conf_or_journal]


    def create_author_paper_based_features(self, auth, pap):
        papers_in_relevant_conf_or_journal = 0
        papers_in_relevant_year = 0
        common_surnames = 0
        common_affiliation = 0
        if pap.conference_id == 0:
            papers_in_relevant_conf_or_journal = (auth.all_journals.get(pap.journal_id) or 0)
        else:
            papers_in_relevant_conf_or_journal = (auth.all_conferences.get(pap.conference_id) or 0)
        papers_in_relevant_year = (auth.all_years.get(pap.year) or 0)
        for auth_id in pap.authors.keys():
            other_auth = self.parser.authors.get(auth_id)
            if not other_auth:
                continue
            if other_auth.surname == auth.surname:
                common_surnames += 1
            common_affiliation += len(set(other_auth.affiliation.split()) & set(auth.affiliation.split()))
        return [papers_in_relevant_conf_or_journal, papers_in_relevant_year, common_surnames, common_affiliation]


    def create_features_from_res(self, res):
        ret = None
        author_id = int(res[0])
        auth = self.parser.authors.get(author_id)
        
        author_features = self.create_author_based_features(auth)
        
        # Create positive features
        for pap_str in res[1].split():
            pap_id = int(pap_str)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            paper_features = self.create_paper_based_features(pap)
            author_paper_features = self.create_author_paper_based_features(auth, pap)
            all_features = author_features + paper_features + author_paper_features
            if ret != None:
                ret = numpy.vstack((ret, [1] + all_features))
            else:
                ret = numpy.array([1] + all_features)
            print all_features

        if len(res) < 3:
            return ret

        #Create negative features
        for pap_str in res[2].split():
            pap_id = int(pap_str)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            paper_features = self.create_paper_based_features(pap)
            author_paper_features = self.create_author_paper_based_features(auth, pap)
            all_features = author_features + paper_features + author_paper_features
            ret = numpy.vstack((ret, [0] + all_features))
            print all_features
        return ret
