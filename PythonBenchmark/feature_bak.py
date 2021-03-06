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
        ret = ret + [conf_frac, journal_frac, combined_frac]
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
        conf_or_journal = 0
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

          if pap.conference_id == 0:
            num_papers_in_conf_or_journal += (auth.all_journals.get(pap.journal_id) or 0)
            conf_or_journal = 1
            relevant_conf_or_journal = self.parser.journals.get(pap.journal_id) or ""
            for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.journal_freq.get(w) or 0)
                conf_or_journal_across_freq += (journal_dict.get(w) or 0)
          else:
            num_papers_in_conf_or_journal += (auth.all_conferences.get(pap.conference_id) or 0)
            conf_or_journal = 0
            relevant_conf_or_journal = self.parser.conferences.get(pap.conference_id) or ""
            for w in relevant_conf_or_journal.split():
                conf_or_journal_freq += (self.parser.conference_freq.get(w) or 0)
                conf_or_journal_across_freq += (conference_dict.get(w) or 0) 

          coauth_freq += (author_dict.get(auth_id) or 0)

        for title_word in pap.title.split():
            title_freq += title_dict[title_word]

        for keyword_word in pap.keywords.split():
            keyword_freq += keyword_dict[keyword_word]

        ret = [num_authors, num_papers, num_conference_papers, num_journal_papers, num_conferences, num_journals, num_papers_in_year, num_papers_in_conf_or_journal, conf_or_journal, conf_or_journal_keywords, conf_or_journal_freq, conf_or_journal_across_freq, coauth_freq, title_num, title_freq, keyword_num, keyword_freq]

        # Fractions
        conf_frac = float(num_conference_papers)/float(num_papers) if num_papers != 0 else 0
        journal_frac = float(num_journal_papers)/float(num_papers) if num_papers != 0 else 0
        combined_frac = float(num_conferences)/(float(num_conferences)+float(num_journals)) if (num_conferences+num_journals) != 0 else 0
        ret = ret + [conf_frac, journal_frac, combined_frac]
        return ret


    def create_author_paper_based_features(self, auth, pap):
        papers_in_relevant_conf_or_journal = 0
        papers_in_relevant_year = 0
        name_keywords = 0
        affiliation_keywords = 0
        common_surnames = 0
        common_affiliation = 0

        if pap.conference_id == 0:
            papers_in_relevant_conf_or_journal = (auth.all_journals.get(pap.journal_id) or 0)
        else:
            papers_in_relevant_conf_or_journal = (auth.all_conferences.get(pap.conference_id) or 0)
        papers_in_relevant_year = (auth.all_years.get(pap.year) or 0)

        all_names_in_paper = pap.author_names.get(auth.id) or [""]
        all_names_duplicate = pap.author_name_duplicate.get(auth.id) or 0

        name_keywords = 0
        for name_in_paper in all_names_in_paper:
            name_keywords += len(set(auth.name.split()) & set(name_in_paper.split()))
        name_keywords = float(name_keywords) / float(len(all_names_in_paper))
        #name_in_paper = max(all_names_in_paper, key=len)
        #name_keywords = len(set(auth.name.split()) & set(name_in_paper.split()))

        all_affiliations_in_paper = pap.author_affiliations.get(auth.id) or [""]
        all_affiliations_duplicate = pap.author_affiliation_duplicate.get(auth.id) or 0
        
        if len(all_affiliations_in_paper) == 1 and all_affiliations_in_paper[0] != "":
          all_names_in_paper *= 2
          name_keywords *= 2
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
        return [papers_in_relevant_conf_or_journal, papers_in_relevant_year, len(all_names_in_paper), all_names_duplicate, name_keywords, len(all_affiliations_in_paper), all_affiliations_duplicate, affiliation_keywords, common_surnames, common_affiliation]


    def common_papers(self, res):
        if len(res) < 3:
            return list()
        common_set = set(res[1].split()) & set(res[2].split())
        return map(lambda a:int(a), list(common_set))


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
            name_frac = float(author_paper_features[4])/float(author_features[6]) if author_features[6] != 0 else 0
            design_frac = float(author_paper_features[5])/float(author_features[7]) if author_features[7] != 0 else 0
            all_features = all_features + [name_frac, design_frac]
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
            name_frac = float(author_paper_features[4])/float(author_features[6]) if author_features[6] != 0 else 0
            design_frac = float(author_paper_features[5])/float(author_features[7]) if author_features[7] != 0 else 0
            all_features = all_features + [name_frac, design_frac]
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
