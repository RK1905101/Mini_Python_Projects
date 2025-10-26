# Assessing Women's Safety in Indian Cities Through Twitter Data Analysis

## Overview

This project analyzes women's safety in Indian cities by performing sentiment analysis on Twitter data using machine learning techniques. The application provides a graphical user interface (GUI) to upload Twitter datasets, clean the data, perform sentiment analysis, and visualize the results in the form of graphs and charts.

## Project Structure

```
Assessing women's safety in Indian cities through Twitter Data Analysis/
├── CODE/
│   ├── MachineLearning.py
│   └── nltkdownload.py
└── Leveraging Machine learning for Assessing women's safety in Indian cities through Twitter Data Analysis/
    ├── MachineLearning.py
    ├── dataset_link.txt
    ├── download_nltk.bat
    ├── nltkdownload.py
    ├── requirements.txt
    └── run.bat
```

## Features

1. **Data Upload**: Load Twitter datasets in CSV format
2. **Data Cleaning**: Preprocess tweets by removing punctuation, stop words, and non-alphabetic characters
3. **Sentiment Analysis**: Perform natural language processing to classify tweets as positive, negative, or neutral
4. **Visualization**: Display sentiment analysis results in pie charts
5. **Detailed Results**: Show polarity scores for each tweet

## Requirements

- Python 3.x
- Required Python packages (found in [requirements.txt](Leveraging%20Machine%20learning%20for%20Assessing%20women's%20safety%20in%20Indian%20cities%20through%20Twitter%20Data%20Analysis/requirements.txt)):
  - textblob
  - tkinter
  - matplotlib
  - numpy
  - pandas
  - nltk

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```bash
   pip install -r "Leveraging Machine learning for Assessing women's safety in Indian cities through Twitter Data Analysis/requirements.txt"
   ```
3. Download NLTK data:
   ```bash
   cd "Leveraging Machine learning for Assessing women's safety in Indian cities through Twitter Data Analysis"
   python nltkdownload.py
   ```
   Or run the batch file:
   ```bash
   download_nltk.bat
   ```

## Dataset

The project uses Twitter data related to women's safety. The sample dataset can be found on Kaggle:
[MeToo Tweets Dataset](https://www.kaggle.com/mohamadalhasan/metoo-tweets-dataset)

The dataset should be in CSV format with a column named 'Text' containing the tweets.

## How to Run

1. Navigate to the project directory:
   ```bash
   cd "Leveraging Machine learning for Assessing women's safety in Indian cities through Twitter Data Analysis"
   ```
2. Run the main application:
   ```bash
   python MachineLearning.py
   ```
   Or use the batch file:
   ```bash
   run.bat
   ```

## Usage

1. **Upload Tweets Dataset**: Click the "Upload Tweets Dataset" button to select and load your CSV file containing tweets
2. **Read Tweets**: Click "Read Tweets" to display the raw tweets from the dataset
3. **Tweets Cleaning**: Click "Tweets Cleaning" to preprocess the tweets (remove punctuation, stop words, etc.)
4. **Natural Language Processing**: Click "natural language processing" to perform sentiment analysis on the cleaned tweets
5. **Women Safety Graph**: Click "Women Saftey Graph" to visualize the sentiment analysis results in a pie chart

## How It Works

1. **Data Preprocessing**:

   - Removes punctuation and special characters
   - Filters out stop words
   - Retains only alphabetic tokens with length greater than 1

2. **Sentiment Analysis**:

   - Uses TextBlob library for sentiment analysis
   - Classifies tweets based on polarity scores:
     - Negative: Polarity ≤ 0.2
     - Neutral: 0.2 < Polarity ≤ 0.5
     - Positive: Polarity > 0.5

3. **Visualization**:
   - Displays results in a pie chart showing the distribution of positive, negative, and neutral tweets
   - Provides detailed statistics including percentages

## GUI Components

- **Title Bar**: "Analysis of Women Safety in Indian Cities Using Machine Learning on Tweets"
- **Buttons**:
  - Upload Tweets Dataset
  - Read Tweets
  - Tweets Cleaning
  - Natural Language Processing
  - Women Safety Graph
- **Text Area**: Displays tweets and analysis results
- **Graph Window**: Shows pie chart visualization of sentiment analysis

## Output

The application provides:

- Cleaned tweet data
- Sentiment classification for each tweet
- Polarity scores
- Statistical summary of sentiments
- Pie chart visualization of sentiment distribution

## Applications

This project can be used for:

- Social research on women's safety issues
- Understanding public sentiment about women's safety in India
- Policy making based on social media analysis
- Academic research on gender safety topics

## Notes

- Ensure your dataset is in CSV format with a 'Text' column
- The application may take some time to process large datasets
- NLTK data must be downloaded before running the application
- The GUI is built using tkinter library

## Contributing

Feel free to fork this project and submit pull requests for improvements or bug fixes.

## License

This project is open source and available under the MIT License.
