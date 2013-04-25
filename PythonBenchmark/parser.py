import data_io
import author
import paper    
import nlp
import pickle

class Parser:
    
    def __init__(self):
        self.authors = dict()
        self.papers = dict()
        self.affiliations = dict()
        self.surnames = dict()

    def update_paperauthor(self, curr_paper, curr_author, author_id, author_name, author_affiliation):
        if curr_author:
            curr_author.update_paper(curr_paper)
        if curr_paper:
            curr_paper.add_author(author_id)
            curr_paper.add_author_name(author_id, author_name)
            curr_paper.add_author_affiliation(author_id, author_affiliation)
            
    def parse_authors(self):
        # Create authors
        print "Parsing Authors..."
        f = open(data_io.get_paths()["author_processed_path"], "r")
        titles = f.readline()
        for l in f.readlines():
            res = l.strip().split(",")
            # Titles
            raw_title = res[1]
            (name, surname) = nlp.filter_title(raw_title)
            if surname in self.surnames.keys():
                self.surnames[surname] = self.surnames[surname] + 1
            else:
                self.surnames[surname] = 1

            #Affiliations
            raw_affiliation = res[2]
            affiliation = nlp.filter_affiliation(raw_affiliation)
            if affiliation in self.affiliations.keys():
                self.affiliations[affiliation] = self.affiliations[affiliation] + 1
            else:
                self.affiliations[affiliation] = 1
            self.authors[int(res[0])] = author.Author(int(res[0]), name, surname, affiliation)
        print "Done"
        f.close()


    def parse_papers(self):
        # Create Papers
        print "Parsing Papers..."
        f = open(data_io.get_paths()["paper_processed_path"], "r")
        titles = f.readline()
        for l in f.readlines():
            res = l.strip().split(",")
            paper_title = res[1]
            title_words = nlp.filter_paper_title(paper_title)
            paper_keyword = res[5]
            filtered_keyword = nlp.filter_paper_keyword(paper_keyword)
            self.papers[int(res[0])] = paper.Paper(int(res[0]), title_words, int(res[2]), int(res[3]), int(res[4]), filtered_keyword)
        print "Done"
        f.close()

        
    def parse_paperauthors(self):
        # Update all journal/conference/coauthor information
        print "Parsing PaperAuthors..."
        f = open(data_io.get_paths()["paperauthor_processed_path"], "r")
        titles = f.readline()
        count = 0
        for l in f.readlines():
            count += 1
            if count % 100000 == 0:
              print count
            res = l.strip().split(",")
            if not res[0].isdigit():
              continue
            paper_id = int(res[0])
            author_id = int(res[1])
            author_name = nlp.filter_title(res[2])[0]
            author_affiliation = nlp.filter_affiliation(res[3])
            curr_paper = self.papers.get(paper_id)
            curr_author = self.authors.get(author_id)
            self.update_paperauthor(curr_paper, curr_author, author_id, author_name, author_affiliation)
        print "Done"
        f.close()


    def parse_csv(self):
        self.parse_authors()
        self.parse_papers()
        self.parse_paperauthors()


    def parse_db(self):
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
    
        
if __name__ == "__main__":
    p = Parser()
    p.parse_csv()
    with open(data_io.get_paths()["parser_path"], "wb") as output:
        pickle.dump(p, output)
        
