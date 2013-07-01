import gzip
import cPickle
import operator

def common_papers(res):
  common_set = set(res[1].split()) & set(res[2].split())
  common_list = map(lambda a: int(a), common_set)
  return common_list

def paper_results(res):
  result_dict = dict()
  for paper in res[1].split():
    result_dict[int(paper)] = 1
  for paper in res[2].split():
    result_dict[int(paper)] = 0
  return result_dict

def accuracy(f, res, classifier):
  common_list = common_papers(res)
  result_dict = paper_results(res)
  predicted_dict = dict()
  fet = f.create_features_from_res(res)
  if fet == None:
    return
  if len(fet.shape) == 1:
    fet.resize(1, fet.shape[0])
  print "\n", fet
  count = 0
  for pos_paper in res[1].split():
    if int(pos_paper) in common_list:
      continue
    predicted_dict[int(pos_paper)] = classifier.predict_proba(fet[count, 1:])[0][1]
    count += 1
  for neg_paper in res[2].split():
    if int(neg_paper) in common_list:
      continue
    predicted_dict[int(neg_paper)] = classifier.predict_proba(fet[count, 1:])[0][1]
    count += 1
  print predicted_dict
  
  score = 0.
  pos_count = 0
  total_count = 0
  sorted_predicted_dict = sorted(predicted_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
  for x in sorted_predicted_dict:
    total_count += 1
    k = x[0]
    if result_dict[k] == 1:
      pos_count += 1
      score += float(pos_count) / float(total_count)
  if pos_count == 0:
      score = 1.000000
  else:
      score /= float(pos_count)
  with open("scores.txt", "a") as output:
    output.write("%d %s %f\n" % (int(res[0]), f.parser.authors[int(res[0])].name, score))


if __name__ == "__main__":
  print "Reading Features..."
  f = cPickle.load(gzip.open("/export/home/local/sjuvekar/feature.pickle.gz", "r"))
  print "Reading classifier..."
  classifier = cPickle.load(gzip.open("/export/home/local/sjuvekar/classifier.pickle.gz", "r"))
  train_file = open("../data/Train.csv", "r")
  title = train_file.readline()
  for l in train_file.readlines():
    res = l.strip().split(",")
    accuracy(f, res, classifier)
