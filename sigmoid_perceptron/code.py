import numpy as np

class SigmoidPerceptron():
  def __init__(self,input_size):
    self.weights=np.random.randn(input_size)
    self.bias=np.random.randn(1)

  def sigmoid(self,z):
    return 1/(1+np.exp(-z))

  def predict(self,inputs):
    weighted_sum=np.dot(inputs,self.weights)+self.bias
    return self.sigmoid(weighted_sum)

  def fit(self,inputs,targets,learning_rate,num_epochs):
    num_examples=inputs.shape[0]
    for epochs in range(num_epochs):
      for i in range(num_examples):
        #Forward Propagation
        input_vectors=inputs[i]
        target=targets[i]
        prediction=self.predict(input_vectors)
        #Backward Propagation
        error=target-prediction
        self.weights+=learning_rate*error*input_vectors
        self.bias+=learning_rate*error



  def evaluate(self,inputs,targets):
    correct=0
    for input_vector,target in zip(inputs,targets):
      prediction=self.predict(input_vector)
      if prediction>0.5:
        predicted_class=1
      else:
        predicted_class=0
      if predicted_class==target:
        correct+=1
    accuracy=correct/len(inputs)
    return accuracy
