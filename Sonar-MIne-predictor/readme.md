
# 🪨 Sonar Rock vs Mine Prediction using Logistic Regression

This project uses **Machine Learning (Logistic Regression)** to classify whether an object detected by sonar is a **Rock (R)** or a **Mine (M)** based on its frequency response.

---

## 📘 Project Overview

Sonar is used to detect and classify underwater objects based on the sound waves reflected from them.
In this project, we train a **Logistic Regression model** on the **Sonar dataset** to predict whether the detected object is a **mine (metal)** or a **rock (non-metal)**.

---

## 🧠 Dataset

* Dataset Name: **Sonar Data Set (from UCI Machine Learning Repository)**
* Each record consists of **60 numeric features** representing sonar signal strength at various frequencies.
* The **61st column** contains the label:

  * `R` → Rock
  * `M` → Mine

---

## 🧩 Technologies Used

* **Python**
* **NumPy**
* **Pandas**
* **Scikit-learn**

---

## ⚙️ Workflow

1. **Import Libraries**
   Load necessary Python libraries for data handling and model building.

2. **Load Dataset**

   ```python
   sonar_data = pd.read_csv('Copy of sonar data.csv', header=None)
   ```

3. **Data Preprocessing**

   * Display dataset info using `.head()`, `.shape()`, `.describe()`
   * Separate features (`X`) and labels (`y`)

4. **Train-Test Split**

   ```python
   X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, stratify=y, random_state=1)
   ```

5. **Model Training**

   ```python
   model = LogisticRegression()
   model.fit(X_train, y_train)
   ```

6. **Model Evaluation**

   * Accuracy on training and test data using `accuracy_score()`

7. **Prediction**
   Test the model with a sample sonar reading to classify it as Rock or Mine.

---

## 📊 Results

| Dataset  | Accuracy |
| -------- | -------- |
| Training | ~83–87%  |
| Testing  | ~76–80%  |

*(Exact scores may vary slightly on each run due to random initialization.)*

---

## 🧪 Example Prediction

```python
input_data = (
 0.0094,0.0333,0.0306,0.0376,0.1296,0.1795,0.1909,0.1692,0.1870,0.1725,
 0.2228,0.3106,0.4144,0.5157,0.5369,0.5107,0.6441,0.7326,0.8164,0.8856,
 0.9891,1.0000,0.8750,0.8631,0.9074,0.8674,0.7750,0.6600,0.5615,0.4016,
 0.2331,0.1164,0.1095,0.0431,0.0619,0.1956,0.2120,0.3242,0.4102,0.2939,
 0.1911,0.1702,0.1010,0.1512,0.1427,0.1097,0.1173,0.0972,0.0703,0.0281,
 0.0216,0.0153,0.0112,0.0241,0.0164,0.0055,0.0078,0.0055,0.0091,0.0067
)
```

**Output:**

```
['R']
The Object is Rock
```

---

## 🧾 How to Run

1. Clone this repository

   ```bash
   git clone https://github.com/<your-username>/sonar-rock-vs-mine.git
   cd sonar-rock-vs-mine
   ```

2. Install dependencies

   ```bash
   pip install numpy pandas scikit-learn
   ```

3. Run the script

   ```bash
   python sonar_prediction.py
   ```

---

## 🚀 Future Enhancements

* Experiment with other algorithms (SVM, Random Forest, Neural Networks)
* Build a web app using **Flask** or **Streamlit**
* Visualize sonar data patterns using **Matplotlib/Seaborn**

---

## 💡 Author

👤 **Shirsha Nag**



---


