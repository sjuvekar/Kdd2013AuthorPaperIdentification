import author
import paper

class Feature:
    
    def __init__(self, parser):
        self.parser = parser
        
    def create_global_author_features(self, author):
        ret = []
        #Numbers
        num_papers = auth.num_papers
        num_conference_papers = auth.num_conference_papers
        num_journal_papers = auth.num_journal_papers
        num_coauthors = auth.num_coauthors
        num_years = auth.num_years
        ret = ret + [num_papers, num_conference_papers, num_journal_papers, num_coauthors, num_years]
        
        num_positive_papers = auth.num_positive_papers
        num_positive_conference_papers = auth.num_positive_conference_papers
        num_positive_journal_papers = auth.num_positive_journal_papers
        num_positive_coauthors = auth.num_positive_coauthors
        num_positive_years = auth.num_positive_years
        ret = ret + [num_positive_papers, num_positive_conference_papers, num_positive_journal_papers, num_positive_coauthors, num_positive_years]
        
        num_negative_papers = auth.num_negative_papers
        num_negative_conference_papers = auth.num_negative_conference_papers
        num_negative_journal_papers = auth.num_negative_journal_papers
        num_negative_coauthors = auth.num_negative_coauthors
        num_negative_years = auth.num_negative_years
        ret = ret + [num_positive_coauthors, num_negative_conference_papers, num_negative_journal_papers, num_negative_coauthors, num_negative_years]
        
        #Fractions
        frac_positive_papers = float(num_positive_papers) / float(num_papers)
        frac_positive_conference_papers = float(num_positive_conference_papers) / float(num_conference_papers)
        frac_positive_journal_papers = float(num_positive_journal_papers) / float(num_journal_papers)
        frac_positive_coauthors = float(num_positive_coauthors) / float(num_coauthors)
        frac_positive_years = float(num_positive_years) / float(num_years)
        ret = ret + [frac_positive_papers, frac_positive_conference_papers, frac_positive_journal_papers, frac_positive_coauthors, frac_positive_years]
        
        frac_negative_papers = float(num_negative_papers) / float(num_papers)
        frac_negative_conference_papers = float(num_negative_conference_papers) / float(num_conference_papers)
        frac_negative_journal_papers = float(num_negative_journal_papers) / float(num_journal_papers)
        frac_negative_coauthors = float(num_negative_coauthors) / float(num_coauthors)
        frac_negative_years = float(num_negative_years) / float(num_years)
        ret = ret + [frac_negative_papers, frac_negative_conference_papers, frac_negative_journal_papers, frac_negative_coauthors, frac_negative_years]
        
        return ret
        
    def create_conference_based_features(self, auth, conference_id):
        all_conferences = auth.all_conferences.get(conference_id) or 1
        positive_conferences = auth.positive_conferences.get(conference_id) or 0
        negative_conferences = auth.negative_conferences.get(conference_id) or 0
        frac_positive_conferences = float(positive_conferences) / float(all_conferences)
        frac_negative_conferences = float(negative_conferences) / float(all_conferences)
        return [all_conferences, positive_conferences, negative_conferences, frac_positive_conferences, frac_negative_conferences]
    
    def create_journal_based_features(self, auth, journal_id):
        all_journals = auth.all_journals.get(journal_id) or 1
        positive_journals = auth.positive_journals.get(journal_id) or 0
        negative_journals = auth.negative_journals.get(journal_id) or 0
        frac_positive_journals = float(positive_journals) / float(all_journals)
        frac_negative_journals = float(negative_journals) / float(all_journals)
        return [all_journals, positive_journals, negative_journals, frac_positive_journals, frac_negative_journals]
    
    def create_year_based_features(self, auth, year_id):
        all_years = auth.all_years.get(year_id) or 1
        positive_years = auth.positive_years.get(year_id) or 0
        negative_years = auth.negative_years.get(year_id) or 0
        frac_positive_years = float(positive_years) / float(all_years)
        frac_negative_years = float(negative_years) / float(all_years)
        return [all_years, positive_years, negative_years, frac_positive_years, frac_negative_years]
    
    def create_coauthor_based_features(self, auth, pap):
        sum_authors = 0
        sum_positive_authors = 0
        sum_negative_authors = 0
        frac_authors = 1.
        frac_positive_authors = 1.
        frac_negative_authors = 1.
        total_coauthors = auth.num_coauthors
        if total_coauthors == 0:
            total_coauthors = 1
        
        for coauth in pap.authors.keys():
            curr_authors = auth.all_coauthors.get(coauth) or 1
            curr_positive_authors = auth.positive_coauthors.get(coauth) or 0
            curr_negative_authors = auth.negative_coauthors.get(coauth) or 0
            
            sum_authors += curr_authors
            sum_positive_authors += curr_positive_authors
            sum_negative_authors += curr_negative_authors
            frac_authors *= float(curr_authors) / float(total_coauthors)
            frac_positive_authors *= float(curr_positive_authors) / float(curr_authors)
            frac_negative_authors *= float(curr_negative_authors) / float(curr_authors)
        
        return [sum_authors, sum_positive_authors, sum_negative_authors, frac_authors, frac_positive_authors, frac_negative_authors]
    
    
    def create_paper_based_features(self, pap):
        #TODO
        return [len(pap.authors.keys())]
    
    def create_all_features(self, global_features, auth, pap):
        paper_based = self.create_paper_based_features(pap)
        coauthor_based = self.create_coauthor_based_features(auth, pap)

        conference_id = pap.conference_id
        conference_based = self.create_conference_based_features(auth, conference_id)
        
        journal_id = pap.journal_id
        journal_based = self.create_journal_based_features(auth, journal_id)
        
        year_id = pap.year
        year_based = self.create_year_based_features(auth, year_id)
        
        return (global_features + paper_based + coauthor_based + conference_based + journal_based + year_based)