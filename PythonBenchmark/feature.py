import author
import paper
import numpy

class Feature:
    
    def __init__(self, parser):
        self.parser = parser
        
    def create_global_author_features(self, auth):
        ret = []
        #Numbers
        num_papers = auth.num_papers
        num_conference_papers = auth.num_conference_papers
        num_journal_papers = auth.num_journal_papers
        num_coauthors = auth.num_coauthors
        num_years = auth.num_years
       
        num_positive_papers = auth.num_positive_papers
        num_positive_conference_papers = auth.num_positive_conference_papers
        num_positive_journal_papers = auth.num_positive_journal_papers
        num_positive_coauthors = auth.num_positive_coauthors
        num_positive_years = auth.num_positive_years
        
        num_negative_papers = auth.num_negative_papers
        num_negative_conference_papers = auth.num_negative_conference_papers
        num_negative_journal_papers = auth.num_negative_journal_papers
        num_negative_coauthors = auth.num_negative_coauthors
        num_negative_years = auth.num_negative_years
      
        # Sanity check
        if num_papers == 0:
          num_papers = max(num_positive_papers + num_negative_papers, 1)
        if num_conference_papers == 0:
          num_conference_papers = max(num_positive_conference_papers + num_negative_conference_papers, 1)
        if num_journal_papers == 0:
          num_journal_papers = max(num_positive_journal_papers + num_negative_journal_papers, 1)
        if num_coauthors == 0:
          num_coauthors = max(num_positive_coauthors + num_negative_coauthors, 1)
        if num_years == 0:
          num_years = max(num_positive_years + num_negative_years, 1)

        ret = ret + [num_papers, num_conference_papers, num_journal_papers, num_coauthors, num_years]
        #ret = ret + [num_positive_papers, num_positive_conference_papers, num_positive_journal_papers, num_positive_coauthors, num_positive_years]
        #ret = ret + [num_negative_papers, num_negative_conference_papers, num_negative_journal_papers, num_negative_coauthors, num_negative_years]

        #Fractions
        frac_positive_papers = float(num_positive_papers) / float(num_papers)
        frac_positive_conference_papers = float(num_positive_conference_papers) / float(num_conference_papers)
        frac_positive_journal_papers = float(num_positive_journal_papers) / float(num_journal_papers)
        frac_positive_coauthors = float(num_positive_coauthors) / float(num_coauthors)
        frac_positive_years = float(num_positive_years) / float(num_years)
        #ret = ret + [frac_positive_papers, frac_positive_conference_papers, frac_positive_journal_papers, frac_positive_coauthors, frac_positive_years]
        
        frac_negative_papers = float(num_negative_papers) / float(num_papers)
        frac_negative_conference_papers = float(num_negative_conference_papers) / float(num_conference_papers)
        frac_negative_journal_papers = float(num_negative_journal_papers) / float(num_journal_papers)
        frac_negative_coauthors = float(num_negative_coauthors) / float(num_coauthors)
        frac_negative_years = float(num_negative_years) / float(num_years)
        #ret = ret + [frac_negative_papers, frac_negative_conference_papers, frac_negative_journal_papers, frac_negative_coauthors, frac_negative_years]
        
        return ret
        
    def create_conference_based_features(self, auth, conference_id):
        all_conferences = auth.all_conferences.get(conference_id) or 1
        positive_conferences = auth.positive_conferences.get(conference_id) or 1
        negative_conferences = auth.negative_conferences.get(conference_id) or 1
        frac_positive_conferences = float(positive_conferences) / float(all_conferences)
        frac_negative_conferences = float(negative_conferences) / float(all_conferences)
        return [all_conferences, positive_conferences, negative_conferences, frac_positive_conferences, frac_negative_conferences]
    
    def create_journal_based_features(self, auth, journal_id):
        all_journals = auth.all_journals.get(journal_id) or 1
        positive_journals = auth.positive_journals.get(journal_id) or 1
        negative_journals = auth.negative_journals.get(journal_id) or 1
        frac_positive_journals = float(positive_journals) / float(all_journals)
        frac_negative_journals = float(negative_journals) / float(all_journals)
        return [all_journals, positive_journals, negative_journals, frac_positive_journals, frac_negative_journals]
    
    def create_year_based_features(self, auth, year_id):
        all_years = auth.all_years.get(year_id) or 1
        positive_years = auth.positive_years.get(year_id) or 1
        negative_years = auth.negative_years.get(year_id) or 1
        frac_positive_years = float(positive_years) / float(all_years)
        frac_negative_years = float(negative_years) / float(all_years)
        return [all_years, positive_years, negative_years, frac_positive_years, frac_negative_years]
    
    def create_coauthor_based_features(self, curr_author_id, auth):
        sum_authors = auth.all_coauthors.get(curr_author_id) or 1
        sum_positive_authors = auth.positive_coauthors.get(curr_author_id) or 1
        sum_negative_authors = auth.negative_coauthors.get(curr_author_id) or 1
        frac_positive_authors = float(sum_positive_authors) / float(sum_authors)
        frac_negative_authors = float(sum_negative_authors) / float(sum_authors)
        return [sum_authors, sum_positive_authors, sum_negative_authors, frac_positive_authors, frac_negative_authors]
    
    
    def create_paper_based_features(self, global_features, curr_auth_id, pap):
        #TODO
        coauthor_based = [0., 0., 0., 1., 1.]
        conference_based = [0., 0., 0., 1., 1.]
        journal_based = [0., 0., 0., 1., 1.]
        year_based = [0., 0., 0., 1., 1.]
        for auth_id in pap.authors.keys():
            auth = self.parser.authors.get(auth_id)
            if not auth:
                continue
            new_coauth = self.create_coauthor_based_features(curr_auth_id, auth)
            new_conf = self.create_conference_based_features(auth, pap.conference_id)
            new_journal = self.create_journal_based_features(auth, pap.journal_id)
            new_year = self.create_year_based_features(auth, pap.year)
            coauthor_based = [coauthor_based[0]+new_coauth[0], coauthor_based[1]+new_coauth[1], coauthor_based[2]+new_coauth[2], coauthor_based[3]*new_coauth[3], coauthor_based[4]*new_coauth[4]]
            conference_based = [conference_based[0]+new_conf[0], conference_based[1]+new_conf[1], conference_based[2]+new_conf[2], conference_based[3]*new_conf[3], conference_based[4]*new_conf[4]]
            journal_based = [journal_based[0]+new_journal[0], journal_based[1]+new_journal[1], journal_based[2]+new_journal[2], journal_based[3]*new_journal[3], journal_based[4]*new_journal[4]]
            year_based = [year_based[0]+new_year[0], year_based[1]+new_year[1], year_based[2]+new_year[2], year_based[3]*new_year[3], year_based[4]*new_year[4]]
  
        tot_paper = max(len(pap.authors.keys()), 1)
        pos_paper = len(pap.positive_authors.keys())
        neg_paper = len(pap.negative_authors.keys())
        ret = [tot_paper, pos_paper, neg_paper, float(pos_paper) / float(tot_paper), float(neg_paper) / float(tot_paper) ]
        if pap.conference_id == 0:
            ret = ret + [0]
        else:
            ret = ret + [1]

        return (global_features + ret + coauthor_based + conference_based + journal_based + year_based)
        

    def create_features_from_res(self, res):
        author_id = int(res[0])
        auth = self.parser.authors.get(author_id)
        
        global_features = self.create_global_author_features(auth)
        
        ret = None
        # Create positive features
        for pap_str in res[1].split():
            pap_id = int(pap_str)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            all_features = self.create_paper_based_features(global_features, author_id, pap)
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
            all_features = self.create_paper_based_features(global_features, author_id, pap)
            ret = numpy.vstack((ret, [0] + all_features))
            print all_features
        return ret
