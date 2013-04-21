import data_io
import author
import paper    
import pickle

class Parser:
    
    def __init__(self):
        self.authors = dict()
        self.papers = dict()

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
            curr_paper = self.papers[paper_id]
            curr_author = None
            if author_id in self.authors.keys():
                curr_author = self.authors[author_id]
                curr_author.update_paper(curr_paper)
            for coauthor_id in curr_paper.authors.keys():
                if coauthor_id in self.authors.keys():
                    coauthor = self.authors[coauthor_id]
                    coauthor.update_coauthors(author_id)
                    coauthor.num_coauthors += 1
                    if curr_author:
                        curr_author.update_coauthors(coauthor_id)
                        curr_author.num_coauthors += 1
            curr_paper.add_author(author_id)
        print "Done"
        
if __name__ == "__main__":
    p = Parser()
    p.parse()
    with open("parser.pkl") as output:
        pickle.dump(p, output)
        
