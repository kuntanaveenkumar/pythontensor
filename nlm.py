from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn import metrics

# Sample data
texts = [
    "I love programming in Python",
    "Python is a great language",
    "I dislike bugs in the code",
    "Debugging is fun",
    "I enjoy learning new things",
    "Errors can be frustrating"
]
labels = ['positive', 'positive', 'negative', 'positive', 'positive', 'negative']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.2, random_state=42)

# Create a pipeline that combines a TF-IDF vectorizer with a Naive Bayes classifier
model = make_pipeline(TfidfVectorizer(), MultinomialNB())

# Train the model
model.fit(X_train, y_train)

# Predict the labels for the test set
predicted_labels = model.predict(X_test)

# Evaluate the model
accuracy = metrics.accuracy_score(y_test, predicted_labels)
print(f'Accuracy: {accuracy:.2f}')

# Print a classification report
print(metrics.classification_report(y_test, predicted_labels))