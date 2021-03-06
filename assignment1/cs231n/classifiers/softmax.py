import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_classes = W.shape[1]
  num_train = X.shape[0]
  for i in range(num_train):
    scores = X[i].dot(W)
    scores -= np.max(scores) # to prevent numeric instability
    exp_scores = np.exp(scores)
    exp_score_sum = 0.0
    for j in range(num_classes):
      exp_score_sum += exp_scores[j]
    correct_class_score = -np.log(exp_scores[y[i]] / exp_score_sum)
    loss += correct_class_score
    for j in range(num_classes):
      p = exp_scores[j] / exp_score_sum
      if j == y[i]:
        dW[:, y[i]] += (p-1) * X[i]
      else:
        dW[:, j] += p * X[i]
       
  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  scores = X.dot(W)
  scores -= np.max(scores)
  exp_scores = np.exp(scores)
  sum_class_scores = np.sum(exp_scores, axis = 1)
  p = exp_scores / sum_class_scores.reshape(-1, 1)
  y_i_p = -np.log(p[np.arange(p.shape[0]), y])
  loss = np.sum(y_i_p)
  
  # (p-1) * X == p*X - X
  dW += X.T.dot(p)
  y_i = np.zeros_like(p)
  y_i[np.arange(y_i.shape[0]), y] = 1
  dW -= X.T.dot(y_i)

  loss /= num_train
  dW /= num_train
  loss += reg * np.sum(W * W)
  dW += reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW

