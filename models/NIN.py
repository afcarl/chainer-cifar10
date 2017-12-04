import chainer
import chainer.functions as F
import chainer.links as L


class NIN(chainer.Chain):

    def __init__(self, n_class=10):
        w = chainer.initializers.HeNormal()
        super(NIN, self).__init__()
        with self.init_scope():
            self.mlpconv1 = L.MLPConvolution2D(
                3, (192, 160, 96), 5, pad=2, initialW=w)
            self.mlpconv2 = L.MLPConvolution2D(
                96, (192, 192, 192), 5, pad=2, initialW=w)
            self.mlpconv3 = L.MLPConvolution2D(
                192, (192, 192, n_class), 3, pad=1, initialW=w)

    def __call__(self, x, t):
        h = F.relu(self.mlpconv1(x))
        h = F.max_pooling_2d(h, 3, stride=2)
        h = F.dropout(h, ratio=0.5)

        h = F.relu(self.mlpconv2(h))
        h = F.average_pooling_2d(h, 3, stride=2)
        h = F.dropout(h, ratio=0.5)

        h = self.mlpconv3(h)
        h = F.average_pooling_2d(h, h.data.shape[2])
        y = F.reshape(h, (x.data.shape[0], 10))
        return y
