import json
import theano
import numpy as np
from numpy import random
from pandas import DataFrame
from theano import tensor as T
from collections import OrderedDict
from sklearn.preprocessing import LabelEncoder


shared_zeros_like = lambda var: theano.shared(np.zeros_like(var.get_value()).astype(np.float32))


# https://github.com/lisa-lab/pylearn2/pull/136
def get_nesterov_momentum_updates(loss_expr,
                                  dense_parameters, sparse_parameters,
                                  learning_rate, momentum):
    learning_rate = np.float32(learning_rate)
    momentum = np.float32(momentum)

    grads = T.grad(cost=loss_expr, wrt=dense_parameters + sparse_parameters)
    dense_grads = grads[:len(dense_parameters)]
    sparse_grads = grads[-len(sparse_parameters):]
    updates = []

    for p, g in zip(sparse_parameters, sparse_grads):
        updates.append((p, p - learning_rate * g))

    for p, g in zip(dense_parameters, dense_grads):
        v = shared_zeros_like(p)
        new_v = momentum * v - learning_rate * g
        new_p = p + momentum * new_v - learning_rate * g
        updates.append((v, new_v))
        updates.append((p, new_p))
    return updates


rng = random.RandomState(seed=42)


class Constant(object):
    def __init__(self, shape, val=0.0):
        self.shape = shape
        self.val = val

    def __call__(self):
        c = np.empty(self.shape, dtype=np.float32)
        c.fill(self.val)
        return c


class Orthogonal(object):
    def __init__(self, shape):
        self.shape = shape

    def __call__(self):
        a = rng.normal(0.0, 1.0, self.shape)
        u, _, v = np.linalg.svd(a, full_matrices=False)
        q = u if u.shape == self.shape else v
        q = q.reshape(self.shape).astype(np.float32)
        return q


class EmbeddingLayer(object):
    def __init__(self, embeding_init):
        self.W = theano.shared(embeding_init())

    def get_output_expr(self, input_expr):
        return self.W[input_expr]


class DenseLayer(object):
    def __init__(self, W_init, b_init):
        self.W = theano.shared(W_init())
        self.b = theano.shared(b_init())

    def get_output_expr(self, input_expr):
        return T.nnet.relu(T.dot(input_expr, self.W) + self.b)


class SoftmaxLayer(object):
    def __init__(self, W_init, b_init):
        self.W = theano.shared(W_init())
        self.b = theano.shared(b_init())

    def get_output_expr(self, input_expr):
        return T.nnet.softmax(T.dot(input_expr, self.W) + self.b)


class DropoutLayer(object):
    def __init__(self, dropout_prob):
        self.keep_prob = np.float32(1. - dropout_prob)

    def get_output_expr(self, input_expr):
        r_stream = T.shared_randomstreams.RandomStreams(1984)
        mask = r_stream.binomial(size=input_expr.shape, p=self.keep_prob, dtype='float32')
        return mask * input_expr


class ScaleLayer(object):
    def __init__(self, scale_factor):
        self.scale_factor = np.float32(scale_factor)

    def get_output_expr(self, input_expr):
        return self.scale_factor * input_expr


with open('data/train.json') as train_f, open('data/test.json') as test_f:
    train_data = json.load(train_f)
    test_data = json.load(test_f)


train_X = [' '.join(e['ingredients']) for e in train_data]
train_X = [e.split() for e in train_X]
train_Y = [e['cuisine'] for e in train_data]
test_X = [' '.join(e['ingredients']) for e in test_data]
test_X = [e.split() for e in test_X]
test_id = [e['id'] for e in test_data]

vocab = set([e for each in train_X for e in each]+['<ABS>'])
vocab_to_idx = dict((e[1], e[0]) for e in enumerate(vocab))
idx_to_vocab = list(vocab)

train_X = [[vocab_to_idx[e] for e in each] for each in train_X]
test_X = [[vocab_to_idx[(e if e in vocab else '<ABS>')] for e in each] for each in test_X]
ingredients_le = LabelEncoder()
cuisine_le = LabelEncoder()
train_Y = cuisine_le.fit_transform(train_Y)
num_classes = len(cuisine_le.classes_)


embd_layer = EmbeddingLayer(Orthogonal((len(vocab), 1024)))
drop1 = DropoutLayer(0.2)
sc1 = ScaleLayer(0.8)
dense_layer = DenseLayer(Orthogonal((1024, 512)), Constant((512, )))
drop2 = DropoutLayer(0.5)
sc2 = ScaleLayer(0.5)
softmax_layer = SoftmaxLayer(Orthogonal((512, num_classes)), Constant((num_classes, )))


ingredients = T.ivector()
cuisine = T.ivector()

# train model
output = embd_layer.get_output_expr(ingredients)
output = drop1.get_output_expr(output)
output = T.sum(output, axis=0)
output = dense_layer.get_output_expr(output)
output = drop2.get_output_expr(output)
predicted_y = softmax_layer.get_output_expr(output)

# valid model
output = embd_layer.get_output_expr(ingredients)
output = sc1.get_output_expr(output)
output = T.sum(output, axis=0)
output = dense_layer.get_output_expr(output)
output = sc2.get_output_expr(output)
predicted_y_val = softmax_layer.get_output_expr(output)


loss = T.sum(T.nnet.categorical_crossentropy(predicted_y, cuisine))
updates = get_nesterov_momentum_updates(loss, [dense_layer.W, dense_layer.b, softmax_layer.W, softmax_layer.b], [embd_layer.W], 0.0005, 0.9)
train_model = theano.function(inputs=[ingredients, cuisine], outputs=loss, updates=updates)

loss_val = T.sum(T.nnet.categorical_crossentropy(predicted_y_val, cuisine))
get_cost = theano.function(inputs=[ingredients, cuisine], outputs=loss_val)
predict = theano.function(inputs=[ingredients], outputs=predicted_y_val)

train_data = zip(train_X, train_Y)
rng.shuffle(train_data)
n = len(train_data)
val_data_val = train_data[:int(n * 0.1)]
train_data = train_data[int(n * 0.1):]


for i in xrange(18):
    print( 'epoch', i)
    losses = []
    rng.shuffle(train_data)
    for i, (ingredients, cuisine) in enumerate(train_data):
        loss = train_model(ingredients, [cuisine])
        losses.append(loss)
        if i != 0 and i % 10000 == 0:
            print ('train', np.mean(losses))
            losses = []
            for ingredients, cuisine in val_data_val:
                losses.append(get_cost(ingredients, [cuisine]))
            print ('val', np.mean(losses))
            losses = []


losses = []
acc = []
for ingredients, cuisine in val_data_val:
    losses.append(get_cost(ingredients, [cuisine]))
    prob_dist = predict(ingredients)
    idx = np.argmax(prob_dist)
    acc.append(idx == cuisine)
print( np.mean(losses), np.mean(acc))

test_Y = []
for each in test_X:
    prob_dist = predict(each)
    idx = np.argmax(prob_dist)
    test_Y.append(cuisine_le.inverse_transform(idx))

d = DataFrame(data=OrderedDict([('id', test_id), ('cuisine', test_Y)]))
d.to_csv('submission.csv', index=False)