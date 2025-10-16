Sigmoid Perceptron from Scratch

This project builds a Sigmoid Perceptron (a simple single-layer neural network) completely from scratch using NumPy.
It shows how a neuron learns through forward and backward propagation without using any deep learning library.

Features

Built using only NumPy

Implements sigmoid activation

Supports manual training and weight updates

Includes accuracy evaluation

How It Works

Forward Propagation: Calculates weighted sum and applies sigmoid activation.

Backward Propagation: Computes error and updates weights and bias.

Evaluation: Checks model accuracy.

Mathematical Equations

Sigmoid Function:
σ(z) = 1 / (1 + e^(-z))

Prediction:
ŷ = σ(Wx + b)

Weight Update Rules:
W = W + η(y - ŷ)x
b = b + η(y - ŷ)

Example usage
```
# Example dataset (AND logic)
inputs = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])

targets = np.array([0, 0, 0, 1])

# Initialize model
model = SigmoidPerceptron(input_size=2)

# Train model
model.fit(inputs, targets, learning_rate=0.1, num_epochs=1000)

# Evaluate accuracy
accuracy = model.evaluate(inputs, targets)
print(f"Training Accuracy: {accuracy * 100:.2f}%")
```
Future Improvements

Add loss curve visualization

Implement batch training

Extend to multiple layers

Try other activation functions like ReLU or tanh

Author

Shirsha Nag 
Data Science and Quantum Computing Enthusiast
