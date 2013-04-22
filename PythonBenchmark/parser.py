import data_io
import author
import paper    
import pickle

class Parser:
    
    def __init__(self):
        self.authors = dict()
        self.papers = dict()


    def update_paperauthor(self, curr_paper, curr_author, author_id):
        if curr_author:
            curr_author.update_paper(curr_paper)
        if curr_paper:
            """
            for coauthor_id in curr_paper.authors.keys():
                if coauthor_id in self.authors.keys():
                    coauthor = self.authors[coauthor_id]
                    coauthor.update_coauthors(author_id)
                    coauthor.num_coauthors += 1
                    if curr_author:
                        curr_author.update_coauthors(coauthor_id)
                        curr_author.num_coauthors += 1
            """
            curr_paper.add_author(author_id)
    
    def parse(self):
        conn = data_io.get_db_conn()
        cursor = conn.cursor()

        # Create authors
        print "Parsing Authors..."
        cursor.execute("SELECT * from Author;")
        for res in cursor:
            self.authors[res[0]] = author.Author(res[0], res[1], res[2])
        print "Done"

        # Create Papers
        print "Parsing Papers..."
        cursor.execute("SELECT * from Paper;")
        for res in cursor:
            self.papers[res[0]] = paper.Paper(res[0], res[1], res[2], res[3], res[4], res[5])
        print "Done"
                
        # First Update all journal/conference/coauthor information
        print "Parsing PaperAuthors..."
        cursor.execute("SELECT * from PaperAuthor;")
        for res in cursor:
            paper_id = res[0]
            author_id = res[1]
            curr_author = None
            curr_paper = None
            if paper_id in self.papers.keys():
                curr_paper = self.papers[paper_id]
            if author_id in self.authors.keys():
                curr_author = self.authors[author_id]
            self.update_paperauthor(curr_paper, curr_author, author_id)
        print "Done"
    

    def parse_csv(self):
        # Create authors
        print "Parsing Authors..."
        f = open("../data/Author_processed.csv", "r")
        titles = f.readline()
        while True:
            l = f.readline()
            if not l:
              break
            res = l.strip().split(",")
            self.authors[int(res[0])] = author.Author(int(res[0]), res[1], res[2])
        print "Done"
        f.close()

        # Create Papers
        print "Parsing Papers..."
        f = open("../data/Paper_processed.csv", "r")
        titles = f.readline()
        while True:
            l = f.readline()
            if not l:
              break
            res = l.strip().split(",")
            self.papers[int(res[0])] = paper.Paper(int(res[0]), res[1], int(res[2]), int(res[3]), int(res[4]), res[5])
        print "Done"
        f.close()

        # First Update all journal/conference/coauthor information
        print "Parsing PaperAuthors..."
        f = open("../data/PaperAuthor_processed.csv", "r")
        titles = f.readline()
        count = 0
        while True:
            l = f.readline()
            count += 1
            if count % 100000 == 0:
              print count
            if not l:
              break
            res = l.strip().split(",")
            if not res[0].isdigit():
              continue
            paper_id = int(res[0])
            author_id = int(res[1])
            curr_paper = self.papers.get(paper_id)
            curr_author = self.authors.get(author_id)
            self.update_paperauthor(curr_paper, curr_author, author_id)
        print "Done"
        f.close()


    def update_using_train(self):
        print "Updating parser using train csv..."
        f = open("../data/Train.csv")
        title = f.readline()
        for l in f.readlines():
            res = l.split(",")
            author_id = int(res[0])
            auth = self.authors.get(author_id)
            if not auth:
                return
            for pap_str in res[1].split():
                pap_id = int(pap_str)
                pap = self.papers.get(pap_id)
                auth.update_positive_paper(pap)
                if pap:
                    pap.positive_authors[author_id] = 1
                    for coauthor_id in pap.authors.keys():
                        coauthor = self.authors.get(coauthor_id)
                        # Update positive and all coauthors here
                        auth.num_coauthors += 1
                        auth.num_positive_coauthors += 1
                        auth.update_coauthors(coauthor_id)
                        auth.update_positive_coauthors(coauthor_id)
                    self.papers[pap_id] = pap
            
            for pap_str in res[2].split():
                pap_id = int(pap_str)
                pap = self.papers.get(pap_id)
                auth.update_negative_paper(pap)
                if pap:
                    pap.negative_authors[author_id] = 1
                    for coauthor_id in pap.authors.keys():
                        coauthor = self.authors.get(coauthor_id)
                        # Update negative and all coauthors here
                        auth.num_coauthors += 1
                        auth.num_negative_coauthors += 1
                        auth.update_coauthors(coauthor_id)
                        auth.update_negative_coauthors(coauthor_id)
                    self.papers[pap_id] = pap
            
            self.authors[author_id] = auth
        print "Done"


if __name__ == "__main__":
    p = Parser()
    p.parse_csv()
    with open(data_io.get_paths()["parser_path"], "wb") as output:
        pickle.dump(p, output)
        
