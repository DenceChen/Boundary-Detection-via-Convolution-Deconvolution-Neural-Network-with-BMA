'''
Created on Mar 7, 2016

@author: Wuga
'''
import numpy
import theano
from theano import tensor as T
import backend as K

class ConvLayer(object):

    def __init__(self, rng, input, filter_shape, image_shape,padding='valid',activation=T.nnet.relu):

        assert image_shape[1] == filter_shape[1]
        self.input = input
        fan_in = numpy.prod(filter_shape[1:])
        fan_out = (filter_shape[0] * numpy.prod(filter_shape[2:]))
        # initialize weights with random weights
        W_bound = numpy.sqrt(6. / (fan_in + fan_out))
        self.W = theano.shared(
            numpy.asarray(
                rng.uniform(low=-W_bound, high=W_bound, size=filter_shape),
                dtype=theano.config.floatX
            ),
            borrow=True
        )

        b_values = numpy.zeros((filter_shape[0],), dtype=theano.config.floatX)
        self.b = theano.shared(value=b_values, borrow=True)

        conv_out = K.conv2d(
            x=input,
            kernel=self.W,
            filter_shape=filter_shape,
            image_shape=image_shape,
            border_mode=padding
        )

        self.output = activation(conv_out + self.b.dimshuffle('x', 0, 'x', 'x'))
        self.params = [self.W, self.b]
        self.input = input

