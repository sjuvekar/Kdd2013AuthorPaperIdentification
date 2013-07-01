import numpy
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cross_validation import KFold 
from sklearn.preprocessing import StandardScaler

df = numpy.loadtxt("../data/features.csv", delimiter=",", skiprows=0)

classifier1 = GradientBoostingClassifier(n_estimators=1024, max_depth=6, min_samples_split=10, subsample=0.8, random_state=1, verbose=3)
classifier2 = RandomForestClassifier(random_state=1, verbose=3, n_estimators=100)
classifier3 = SVC(verbose=3, C=0.00001, probability=True)
sc = StandardScaler()

kf =KFold(len(df), n_folds=3)

count = 0
for train_index, test_index in kf:
  if count == 0:
    trainX, testX = df[train_index, 3:], df[test_index, 3:]
    trainY, testY = df[train_index, 0], df[test_index, 0]
    print "training GBF"
    classifier1.fit(trainX, trainY)
    print "Score for GBF = ", classifier1.score(testX, testY)
    count += 1
    continue

  elif count == 1:
    trainX, testX = df[train_index, 3:], df[test_index, 3:]
    trainY, testY = df[train_index, 0], df[test_index, 0]
    print "training RF"
    classifier2.fit(trainX, trainY)
    print "Score for RF = ", classifier2.score(testX, testY)
    count += 1
    continue
  else:
    trainX, testX = df[train_index, 3:], df[test_index, 3:]
    trainY, testY = df[train_index, 0], df[test_index, 0]
    print "training SVC"
    sc.fit(trainX)
    newTrainX = sc.transform(trainX)
    classifier3.fit(newTrainX, trainY)
    print "Score = ", classifier3.score(testX, testY)
    break

testdf = numpy.loadtxt("../data/test_features.csv", delimiter=",", skiprows=0)
myfp = open("sud.csv", "a")
curr_auth_id = -1
pred=list()
for i in range(len(testdf)):
    auth_id = int(testdf[i, 1])
    if auth_id != curr_auth_id:
        sorted_pred = sorted(pred, key=lambda a:a[1], reverse=True) 
        myfp.write(str(curr_auth_id) + "," + " ".join(map(lambda a: a[0], sorted_pred)) + "\n")
        curr_auth_id = auth_id
        pred = list()
    pred1 = classifier1.predict_proba(testdf[i, 3:])[0][1]
    pred2 = classifier2.predict_proba(testdf[i, 3:])[0][1]
    pred3 = classifier3.predict_proba(sc.transform(testdf[i, 3:]))[0][1]
    pred.append( (str(int(testdf[i, 2])), (pred1+pred2+pred3)/3.) )
sorted_pred = sorted(pred, key=lambda a:a[1], reverse=True)
myfp.write(str(curr_auth_id) + "," + " ".join(map(lambda a: a[0], sorted_pred)) + "\n")
myfp.close()
