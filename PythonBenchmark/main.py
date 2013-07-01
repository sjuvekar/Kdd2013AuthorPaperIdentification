import data_io
import parser
import feature
import numpy
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cross_validation import train_test_split

def validate(f, valid_path, classifier):
  file_pt = open(valid_path, "r")
  ret = None
  for l in file_pt.readlines():
    res = l.split(",")
    fet = f.create_features_from_res(res)
    if ret == None:
      ret = fet
    elif fet != None:
      ret = numpy.vstack((ret, fet))
    print ret.shape
  #print "Valid Score->", classifier.score(ret[:, 3:], ret[:, 0])
  return ret


def train(f, file_path):
  file_pt = open(file_path, "r")
  title = file_pt.readline()
  ret = None
  for l in file_pt.readlines():
    res = l.split(",")
    fet = f.create_features_from_res(res)
    if ret == None:
      ret = fet
    elif fet != None:
      ret = numpy.vstack((ret, fet))
    print ret.shape

#  classifier = RandomForestClassifier(n_estimators=100, 
#                                      verbose=2,
#                                      n_jobs=1,
#                                      min_samples_split=10,
#                                      random_state=1)

  classifier = GradientBoostingClassifier(n_estimators=512, 
                                          verbose=3,
                                          max_depth=6,
                                          min_samples_split=10,
                                          subsample=0.8,
                                          random_state=1)

  valid_ret = validate(f,  data_io.get_paths()["valid_sol_path"], classifier)
  ret = numpy.vstack( (ret, valid_ret) )
  print "Final size: ", ret.shape

  trainX, testX, trainY, testY = train_test_split(ret[:, 3:], ret[:, 0], random_state=1)

  classifier.fit(trainX, trainY)

  numpy.savetxt(data_io.get_paths()["feature_path"], ret.astype(float), fmt='%f', delimiter=",")

  print classifier.score(testX, testY)
  #validate(f, data_io.get_paths()["valid_sol_path"], classifier)
  print classifier.score(valid_ret[:, 3:], valid_ret[:, 0])

  return classifier

def predict(f, classifier, file_path):
  file_pt = open(file_path, "r")
  title = file_pt.readline()
  output = open(data_io.get_paths()["submission_path"], "a")
  tot_fet = None
  for l in file_pt.readlines():
    res = l.split(",")
    fet = f.create_features_from_res(res)
    if tot_fet == None:
      tot_fet = fet
    else:
      tot_fet = numpy.vstack((tot_fet, fet))
    pred = classifier.predict_proba(fet[:, 3:])
    sorted_pred = sorted(zip(res[1].split(), pred[:, 1]), key=lambda a:a[1], reverse=True)
    #print sorted_pred
    output.write(res[0] + "," + " ".join(map(lambda a: a[0], sorted_pred)) + "\n")
  output.close()
  numpy.savetxt(data_io.get_paths()["test_feature_path"], tot_fet.astype(float), fmt='%f', delimiter=",")

if __name__ == "__main__":
  p = parser.Parser()
  p.parse_csv()
  f = feature.Feature(p)
  classifier = train(f, data_io.get_paths()["train_path"])
  predict(f, classifier, data_io.get_paths()["valid_path"])
