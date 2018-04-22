import tensorflow as tf



# https://arxiv.org/pdf/1512.03385.pdf


# residual block
def res_block(x, layer, filters, is_training):
    input_tensor = x

    with tf.variable_scope(layer):
        x = tf.layers.conv2d(x, filters, (3, 3), (1, 1), padding='same')
        x = tf.layers.batch_normalization(x, training=is_training)
        x = tf.nn.relu(x)

        x = tf.layers.conv2d(x, filters, (3, 3), (1, 1), padding='same')
        x = tf.layers.batch_normalization(x, training=is_training)

    res = input_tensor + x
    res = tf.layers.batch_normalization(res, training=is_training)
    res = tf.nn.relu(res)

    return res


# TODO: modify so any size dimesnions are possible
def resnet(X, y, is_training):
    out = tf.layers.conv2d(X, 50, (3, 3), (1, 1))
    out = tf.layers.batch_normalization(out, training=is_training)
    out = tf.nn.relu(out)

    for i in range(3):
        out = res_block(out, '1.' + str(i), 50)

    out = tf.layers.max_pooling2d(out, (2, 2), (1, 1))

    for i in range(3):
        out = res_block(out, '2.' + str(i), 50)

    out = tf.layers.max_pooling2d(out, (2, 2), (2, 2))

    out = tf.layers.dense(tf.reshape(out, (-1, 14 * 14 * 50)), 200)
    out = tf.layers.batch_normalization(out, training=is_training)
    out = tf.layers.dropout(out, rate=.4, training=is_training)
    out = tf.nn.relu(out)

    return tf.layers.dense(out, 10)


