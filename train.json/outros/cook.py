import json
from pandas import DataFrame
from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer


with open('train.json') as train_f, open('test.json') as test_f:
    train_data = json.load(train_f)
    test_data = json.load(test_f)

train_X = [' '.join(e['ingredients']) for e in train_data]
train_Y = [e['cuisine'] for e in train_data]
test_X = [' '.join(e['ingredients']) for e in test_data]
test_id = [e['id'] for e in test_data]

le = LabelEncoder()
ngram_vectorizer = CountVectorizer()
train_Y = le.fit_transform(train_Y)
print (train_Y)

train_X = ngram_vectorizer.fit_transform(train_X).toarray()
test_X = ngram_vectorizer.transform(test_X).toarray()

rf_classifier = RandomForestClassifier()
rf_classifier.fit(train_X, train_Y)

test_Y = rf_classifier.predict(test_X)
test_Y = le.inverse_transform(test_Y)

d = DataFrame(data=OrderedDict([('id', test_id), ('cuisine', test_Y)]))
d.to_csv('submission.csv', index=False)