import author
import paper
import parser
import numpy
import sys
import gzip
import cPickle

class Feature:
    
    def __init__(self, parser):
        self.parser = parser
    
    def create_generic_dict(self, res, key, com_pap):
        def get_iter(pap, key):
            if key == "author":
                return pap.authors.keys()
            elif key == "title":
                return pap.title.split()
            elif key == "keyword":
                return pap.keywords.split()
            elif key == "conference":
                return (self.parser.conferences.get(pap.conference_id) or "").split()
            elif key == "journal":
                return (self.parser.journals.get(pap.journal_id) or "").split()
            else:
                print "Wrong key " + key
                sys.exit()

        d = dict()
        observed_pap_id = dict()
        for pap_str in res[1].split():
            pap_id = int(pap_str)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            if pap_id in observed_pap_id.keys() or pap_id in com_pap:
                continue
            observed_pap_id[pap_id] = 1
            for mykey in get_iter(pap, key):
                if mykey in d.keys():
                    d[mykey] = d[mykey] + 1
                else:
                    d[mykey] = 1
        if len(res) < 3:
            return d
        for pap_str in res[2].split():
            pap_id = int(pap_str)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            if pap_id in observed_pap_id.keys() or pap_id in com_pap:
                continue
            observed_pap_id[pap_id] = 1
            for mykey in get_iter(pap, key):
                if mykey in d.keys():
                    d[mykey] = d[mykey] + 1
                else:
                    d[mykey] = 1
        return d 


    def create_author_dict(self, res, com_pap):
        return self.create_generic_dict(res, "author", com_pap)
                

    def create_title_dict(self, res, com_pap):
        return self.create_generic_dict(res, "title", com_pap)


    def create_keyword_dict(self, res, com_pap):
        return self.create_generic_dict(res, "keyword", com_pap)


    def create_conference_dict(self, res, com_pap):
        return self.create_generic_dict(res, "conference", com_pap)


    def create_journal_dict(self, res, com_pap):
        return self.create_generic_dict(res, "journal", com_pap)


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

        # Fractions
        conf_frac = float(num_conference_papers)/float(num_papers) if num_papers != 0 else 0
        journal_frac = float(num_journal_papers)/float(num_papers) if num_papers != 0 else 0
        combined_frac = float(num_conferences)/(float(num_conferences)+float(num_journals)) if (num_conferences+num_journals) != 0 else 0
        ret = ret + [conf_frac, journal_frac, combined_frac, ]

        #Avg and std
        conf_avg = numpy.mean(auth.all_conferences.values())
        if numpy.isnan(conf_avg):
          conf_avg = 0
        conf_std = numpy.std(auth.all_conferences.values())
        if numpy.isnan(conf_std):
          conf_std = 0
        journal_avg = numpy.mean(auth.all_journals.values())
        if numpy.isnan(journal_avg):
          journal_avg = 0
        journal_std = numpy.std(auth.all_journals.values())
        if numpy.isnan(journal_std):
          journal_std = 0
        year_avg = numpy.mean(auth.all_years.values())
        if numpy.isnan(year_avg):
          year_avg = 0
        year_std = numpy.std(auth.all_years.values())
        if numpy.isnan(year_std):
          year_std = 0
        title_word_avg = numpy.mean(auth.paper_title_words.values())
        if numpy.isnan(title_word_avg):
          title_word_avg = 0
        title_word_std = numpy.std(auth.paper_title_words.values())
        if numpy.isnan(title_word_std):
          title_word_std = 0
        keyword_avg = numpy.mean(auth.all_keywords.values())
        if numpy.isnan(keyword_avg):
          keyword_avg = 0
        keyword_std = numpy.std(auth.all_keywords.values())
        if numpy.isnan(keyword_std):
          keyword_std = 0

        # Max min
        try:
          max_conf = max(auth.all_conferences.values())
          min_conf = min(auth.all_conferences.values())
        except:
          max_conf = 0
          min_conf = 0

        try:
          max_journal = max(auth.all_journals.values())
          min_journal = min(auth.all_journals.values())
        except:
          max_journal = 0
          min_journal = 0

        try:
          max_years = max(auth.all_years.values())
          min_years = min(auth.all_years.values())
        except:
          max_years = 0
          min_years = 0

        try:
          max_title_words = max(auth.paper_title_words.values())
          min_title_words = min(auth.paper_title_words.values())
        except:
          max_title_words = 0
          min_title_words = 0

        try:
          max_keywords = max(auth.all_keywords.values())
          min_keywords = min(auth.all_keywords.values())
        except:
          max_keywords = 0
          min_keywords = 0

        ret = ret + [conf_avg, conf_std, journal_avg, journal_std, year_avg, year_std, title_word_avg, title_word_std, keyword_avg, keyword_std, max_conf, min_conf, max_journal, min_journal, max_years, min_years, max_title_words, min_title_words, max_keywords, min_keywords]

        return ret
       

    def create_paper_based_features(self, pap, d):
        num_authors = len(pap.authors.keys())
        num_papers = 0
        num_conference_papers = 0
        num_journal_papers = 0
        num_conferences = 0
        num_journals = 0
        num_papers_in_year = 0
        year = pap.year
        num_papers_in_conf_or_journal = 0
        conf_or_journal = -1
        conf_or_journal_keywords = 0
        conf_or_journal_freq = 0

        author_dict = d[0]
        title_dict = d[1]
        keyword_dict = d[2]
        conference_dict = d[3]
        journal_dict = d[4]

        coauth_freq = 0
        title_num = len(pap.title.split())
        title_freq = 0
        global_title_freq = 0
        keyword_num = len(pap.keywords.split())
        keyword_freq = 0
        conf_or_journal_across_freq = 0

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

          if pap.journal_id > 0:
            num_papers_in_conf_or_journal += (auth.all_journals.get(pap.journal_id) or 0)
            conf_or_journal = 1
            relevant_conf_or_journal = self.parser.journals.get(pap.journal_id) or ""
            conf_or_journal_keywords = len(relevant_conf_or_journal.split())
            for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.journal_freq.get(w) or 0)
                conf_or_journal_across_freq += (journal_dict.get(w) or 0)
          elif pap.conference_id > 0:
            num_papers_in_conf_or_journal += (auth.all_conferences.get(pap.conference_id) or 0)
            conf_or_journal = 0
            relevant_conf_or_journal = self.parser.conferences.get(pap.conference_id) or ""
            conf_or_journal_keywords = len(relevant_conf_or_journal.split())
            for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.conference_freq.get(w) or 0)
                conf_or_journal_across_freq += (conference_dict.get(w) or 0) 
          else:
            if len(conference_dict.keys()) == 0 and len(journal_dict.keys()) == 0:
              num_papers_in_conf_or_journal = 0
              conf_or_journal_freq = 0
              conf_or_journal_across_freq = 0
            elif len(conference_dict.keys()) > len(journal_dict.keys()):
              c_i = max(conference_dict, key=conference_dict.get)
              num_papers_in_conf_or_journal += (auth.all_conferences.get(c_i) or 0)
              relevant_conf_or_journal = self.parser.conferences.get(c_i) or ""
              conf_or_journal_keywords = len(relevant_conf_or_journal.split())
              for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.conference_freq.get(w) or 0)
                conf_or_journal_across_freq += (conference_dict.get(w) or 0) 
            else:
              j_i = max(journal_dict, key=journal_dict.get)
              num_papers_in_conf_or_journal += (auth.all_journals.get(j_i) or 0)
              relevant_conf_or_journal = self.parser.journals.get(pap.journal_id) or ""
              conf_or_journal_keywords = len(relevant_conf_or_journal.split())
              for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.journal_freq.get(w) or 0)
                conf_or_journal_across_freq += (journal_dict.get(w) or 0)


          coauth_freq += (author_dict.get(auth_id) or 0)

        for title_word in pap.title.split():
            title_freq += title_dict[title_word]
            global_title_freq += self.parser.paper_titles[title_word]

        for keyword_word in pap.keywords.split():
            keyword_freq += keyword_dict[keyword_word]

        ret = [pap.title_zero, pap.year_zero, pap.both_zero, num_authors, num_papers, num_conference_papers, num_journal_papers, num_conferences, num_journals, num_papers_in_year, num_papers_in_conf_or_journal, conf_or_journal, conf_or_journal_keywords, conf_or_journal_freq, conf_or_journal_across_freq, coauth_freq, title_num, title_freq, keyword_num, keyword_freq]

        # Fractions
        conf_frac = float(num_conference_papers)/float(num_papers) if num_papers != 0 else 0
        journal_frac = float(num_journal_papers)/float(num_papers) if num_papers != 0 else 0
        combined_frac = float(num_conferences)/(float(num_conferences)+float(num_journals)) if (num_conferences+num_journals) != 0 else 0
        ret = ret + [conf_frac, journal_frac, combined_frac]

        # Avg and Std
        author_dict_avg = numpy.mean(author_dict.values())
        if numpy.isnan(author_dict_avg):
          author_dict_avg = 0
        author_dict_std = numpy.std(author_dict.values())
        if numpy.isnan(author_dict_std):
          author_dict_std = 0
        title_dict_avg = numpy.mean(title_dict.values())
        if numpy.isnan(title_dict_avg):
          title_dict_avg = 0
        title_dict_std = numpy.std(title_dict.values())
        if numpy.isnan(title_dict_std):
          title_dict_std = 0
        keyword_dict_avg = numpy.mean(keyword_dict.values())
        if numpy.isnan(keyword_dict_avg):
          keyword_dict_avg = 0
        keyword_dict_std = numpy.std(keyword_dict.values())
        if numpy.isnan(keyword_dict_std):
          keyword_dict_std = 0
        conference_dict_avg = numpy.mean(conference_dict.values())
        if numpy.isnan(conference_dict_avg):
          conference_dict_avg = 0
        conference_dict_std = numpy.std(conference_dict.values())
        if numpy.isnan(conference_dict_std):
          conference_dict_std = 0
        journal_dict_avg = numpy.mean(journal_dict.values())
        if numpy.isnan(journal_dict_avg):
          journal_dict_avg = 0
        journal_dict_std = numpy.std(journal_dict.values())
        if numpy.isnan(journal_dict_std):
          journal_dict_std = 0

        ret = ret + [author_dict_avg, author_dict_std, title_dict_avg, title_dict_std, keyword_dict_avg, keyword_dict_std, conference_dict_avg, conference_dict_std, journal_dict_avg, journal_dict_std]
        
        return ret


    def create_author_paper_based_features(self, auth, pap):
        papers_in_relevant_conf_or_journal = 0
        papers_in_relevant_year = 0
        name_keywords = 0
        affiliation_keywords = 0
        common_surnames = 0
        common_affiliation = 0

        if pap.journal_id > 0:
            papers_in_relevant_conf_or_journal = (auth.all_journals.get(pap.journal_id) or 0)
        elif pap.conference_id > 0:
            papers_in_relevant_conf_or_journal = (auth.all_conferences.get(pap.conference_id) or 0)
        else:
            m_c = sum(auth.all_conferences.values())
            n_c = len(auth.all_conferences.values())
            m_j = sum(auth.all_journals.values())
            n_j = len(auth.all_conferences.values())
            try:
              papers_in_relevant_conf_or_journal = (m_c * n_c + m_j * n_j) / (n_c + n_j)
            except:
              papers_in_relevant_conf_or_journal = 0

        frac_papers_in_relevant_conf_or_journal = float(papers_in_relevant_conf_or_journal) / float(auth.num_papers) if auth.num_papers != 0 else 0

        if pap.year > 0:
          papers_in_relevant_year = (auth.all_years.get(pap.year) or 0)
        else:
          try:
            papers_in_relevant_year = max(auth.all_years.values())
          except:
            papers_in_relevant_year = 0
        frac_papers_in_relevant_year = float(papers_in_relevant_year) / float(auth.num_papers) if auth.num_papers != 0 else 0

        all_names_in_paper = pap.author_names.get(auth.id) or [""]
        all_names_duplicate = pap.author_name_duplicate.get(auth.id) or 0

        name_keywords = 0
        for name_in_paper in all_names_in_paper:
            name_keywords += len(set(auth.name.split()) & set(name_in_paper.split()))
        name_keywords_normalized = float(name_keywords) / float(len(all_names_in_paper))
        #name_in_paper = max(all_names_in_paper, key=len)
        #name_keywords = len(set(auth.name.split()) & set(name_in_paper.split()))

        all_affiliations_in_paper = pap.author_affiliations.get(auth.id) or [""]
        all_affiliations_duplicate = pap.author_affiliation_duplicate.get(auth.id) or 0
        
        if len(all_affiliations_in_paper) == 1 and all_affiliations_in_paper[0] != "":
          all_names_in_paper *= 1
          all_names_duplicate *= 1
          name_keywords *= 1
          name_keywords_normalized *= 1

        affiliation_keywords = 0
        for affiliations_in_paper in all_affiliations_in_paper:
            affiliation_keywords += len(set(auth.affiliation.split()) & set(affiliations_in_paper.split()))
        affiliation_keywords = float(affiliation_keywords) / float(len(all_affiliations_in_paper))
        #affiliations_in_paper = max(all_affiliations_in_paper, key=len)
        #affiliation_keywords = len(set(auth.affiliation.split()) & set(affiliations_in_paper.split()))

        for auth_id in pap.authors.keys():
            other_auth = self.parser.authors.get(auth_id)
            if not other_auth:
                continue
            if other_auth.surname == auth.surname:
                common_surnames += 1
            common_affiliation += len(set(other_auth.affiliation.split()) & set(auth.affiliation.split()))

        # Get paper title frequency
        global_paper_title_freq = 0 
        for w in pap.title.split():
            global_paper_title_freq += (auth.paper_title_words.get(w) or 0)
        #try:
        #    global_paper_title_freq = float(global_paper_title_freq) / float(sum(auth.paper_title_words.values()))
        #except:
        #    global_paper_title_freq = 0

        global_keyword_freq = 0
        for w in pap.keywords.split():
            global_keyword_freq += (auth.all_keywords.get(w) or 0)
        #try:
        #    global_keyword_freq = float(global_keyword_freq) / float(sum(auth.all_keywords.values()))
        #except:
        #    global_keyword_freq = 0

        return [papers_in_relevant_conf_or_journal, papers_in_relevant_year, frac_papers_in_relevant_year, len(all_names_in_paper), all_names_duplicate, name_keywords, name_keywords_normalized, len(all_affiliations_in_paper), all_affiliations_duplicate, affiliation_keywords, common_surnames, common_affiliation, global_paper_title_freq, global_keyword_freq]


    def common_papers(self, res):
        if len(res) < 3:
            return list()
        common_set = set(res[1].split()) & set(res[2].split())
        return map(lambda a:int(a), list(common_set))


    def create_frac_features(self, auth, pap, author_features, paper_features, author_paper_features):
        #name_frac = float(author_paper_features[4])/float(author_features[6]) if author_features[6] != 0 else 0
        orig_aff_frac = float(author_paper_features[5])/float(author_features[7]) if author_features[7] != 0 else 0
        name_frac = float(author_paper_features[5])/float(author_features[6]) if author_features[6] != 0 else 0
        aff_frac = float(author_paper_features[9])/float(author_features[7]) if author_features[7] != 0 else 0
        all_affiliations_in_paper = pap.author_affiliations.get(auth.id) or [""]
        if len(all_affiliations_in_paper) == 1 and all_affiliations_in_paper[0] != "":
          name_frac /= 1.0
          orig_aff_frac /= 1.0
        #pap_papers = float(author_features[0])/float(paper_features[3]) if paper_features[3] != 0 else 0
        #name_freq_frac = float(author_paper_features[2])/float(author_features[6]) if author_features[6] != 0 else 0
        #aff_freq_frac = float(author_paper_features[7])/float(author_features[7]) if author_features[7] != 0 else 0
        #common_name_frac = float(author_paper_features[8])/float(author_features[6]) if author_features[6] != 0 else 0 
        #common_aff_frac = float(author_paper_features[9])/float(author_features[7]) if author_features[7] != 0 else 0
        #bin_name_frac = float(author_paper_features[3])/float(author_features[6]) if author_features[6] != 0 else 0
        #bin_aff_frac = float(author_paper_features[6])/float(author_features[7]) if author_features[7] != 0 else 0
        return [name_frac, aff_frac, orig_aff_frac]#pap_papers, name_freq_frac, aff_freq_frac, common_name_frac, common_aff_frac, bin_name_frac, bin_aff_frac] 

    def create_features_from_res(self, res):
        ret = None
        author_id = int(res[0])
        auth = self.parser.authors.get(author_id) 
        author_features = self.create_author_based_features(auth)
        
         # Create a list of both accepted and deleted
        com_pap = self.common_papers(res)
 
        author_dict = self.create_author_dict(res, com_pap)
        paper_title_dict = self.create_title_dict(res, com_pap)
        paper_keyword_dict = self.create_keyword_dict(res, com_pap)
        conference_dict = self.create_conference_dict(res, com_pap)
        journal_dict = self.create_journal_dict(res, com_pap)
        
        d = [author_dict, paper_title_dict, paper_keyword_dict, conference_dict, journal_dict]

        # Create a list for duplicate papers
        dup_pap = list()

        # Create positive features
        for pap_str in res[1].split():
            pap_id = int(pap_str)
            if pap_id in com_pap:
                continue
            if len(res) >= 3 and pap_id in dup_pap:
                continue
            dup_pap.append(pap_id)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            paper_features = self.create_paper_based_features(pap, d)
            author_paper_features = self.create_author_paper_based_features(auth, pap)
            all_features = [author_id, pap_id] + author_features + paper_features + author_paper_features
            # Fractions
            #name_frac = float(author_paper_features[4])/float(author_features[6]) if author_features[6] != 0 else 0
            #design_frac = float(author_paper_features[5])/float(author_features[7]) if author_features[7] != 0 else 0
            frac_features = self.create_frac_features(auth, pap, author_features, paper_features, author_paper_features)
            all_features = all_features + frac_features
            if ret != None:
                ret = numpy.vstack((ret, [1] + all_features))
            else:
                ret = numpy.array([1] + all_features)

        if len(res) < 3:
            return ret

        #Create negative features
        for pap_str in res[2].split():
            pap_id = int(pap_str)
            if pap_id in com_pap:
                continue
            if len(res) >= 3 and pap_id in dup_pap:
                continue
            dup_pap.append(pap_id)
            pap = self.parser.papers.get(pap_id)
            if not pap:
                continue
            paper_features = self.create_paper_based_features(pap, d)
            author_paper_features = self.create_author_paper_based_features(auth, pap)
            all_features = [author_id, pap_id] + author_features + paper_features + author_paper_features
            # Fractions
            #name_frac = float(author_paper_features[4])/float(author_features[6]) if author_features[6] != 0 else 0
            #design_frac = float(author_paper_features[5])/float(author_features[7]) if author_features[7] != 0 else 0
            frac_features = self.create_frac_features(auth, pap, author_features, paper_features, author_paper_features)
            all_features = all_features + frac_features
            if ret != None:
                ret = numpy.vstack((ret, [0] + all_features))
            else:
                ret = numpy.array([0] + all_features)
        return ret


if __name__ == "__main__":
    p = parser.Parser()
    p.parse_csv()
    f = Feature(p)
    gzout = gzip.open("/export/home/local/sjuvekar/feature.pickle.gz", "wb")
    cPickle.dump(f, gzout)
