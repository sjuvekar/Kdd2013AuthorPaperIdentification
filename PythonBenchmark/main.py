import data_io
import parser
import feature
import numpy
from sklearn.ensemble import RandomForestClassifier

def train(f, file_path):
  file_pt = open(file_path, "r")
  title = file_pt.readline()
  ret = None
  for l in file_pt.readlines():
    res = l.split(",")
    fet = f.create_features_from_res(res)
    if ret != None:
      ret = numpy.vstack((ret, fet))
    else:
      ret = fet
  
  classifier = RandomForestClassifier(n_estimators=50, 
                                      verbose=2,
                                      n_jobs=1,
                                      min_samples_split=10,
                                      random_state=1)
  classifier.fit(ret[:, 1:ret.shape[1]], ret[:, 0])

  numpy.savetxt(data_io.get_paths()["feature_path"], ret.astype(float), fmt='%f', delimiter=",")

  return classifier

def predict(f, classifier, file_path):
  file_pt = open(file_path, "r")
  title = file_pt.readline()
  output = open("submission.csv", "a")
  for l in file_pt.readlines():
    res = l.split(",")
    fet = f.create_features_from_res(res)
    pred = classifier.predict_proba(fet[:, 1:fet.shape[1]])
    sorted_pred = sorted(zip(res[1].split(), pred[:, 1]), key=lambda a:a[1], reverse=True)
    print sorted_pred
    output.write(res[0] + "," + " ".join(map(lambda a: a[0], sorted_pred)) + "\n")
  output.close()

if __name__ == "__main__":
  p = parser.Parser()
  p.parse_csv()
  p.update_using_train()
  f = feature.Feature(p)
  classifier = train(f, data_io.get_paths()["train_path"])
  predict(f, classifier, data_io.get_paths()["valid_path"])
