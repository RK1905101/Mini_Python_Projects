# Diascan.ai 🩺 - Diabetes Prediction System for Females using SVM

**Diascan.ai** is a machine learning project focused on predicting diabetes in female patients using data from the PIMA Indian Diabetes dataset. The model is built with a Support Vector Machine (SVM) classifier and optimized for medical relevance, using proper feature scaling and metric-based evaluation.

---

## 🔍 Problem Statement

Early detection of diabetes is crucial for improving health outcomes. This project targets **female-specific prediction** by leveraging features such as pregnancies, glucose levels, BMI, and more to predict the presence of diabetes (binary classification).

---

## 🧠 Technologies Used

- **Language**: Python  
- **Libraries**: `scikit-learn`, `pandas`, `matplotlib`, `seaborn`  
- **Model**: Support Vector Machine (SVM)  
- **Evaluation**: F1-score, Confusion Matrix, Accuracy, Recall  
- **Scaling**: StandardScaler  
- **Dataset**: PIMA Indian Diabetes dataset (UCI)

## 📊 Features Used

- Number of pregnancies  
- Glucose concentration  
- Blood pressure  
- Skin thickness  
- Insulin  
- BMI  
- Diabetes pedigree function  
- Age
## ⚙️ How It Works

1. Data Cleaning (handling zero values in BMI, glucose, etc.)
2. Data Scaling using `StandardScaler`
3. Train-Test Split (80/20)
4. SVM Model Training (`sklearn.svm.SVC`)
5. Evaluation using F1-score and Confusion Matrix
6. ## 🧪 Sample Code Snippet

```python
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# SVM model
model = SVC(kernel='rbf', C=1)
model.fit(X_train, y_train)

# Evaluation
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
