from ernie import SentenceClassifier, Models
import pandas as pd
import config
import numpy as np


df = pd.read_csv('dataset.csv')

mapper = {
    'negative': 0, 'neutral': 1, 'positive': 2
}
df.polarity = df.polarity.map(mapper)

df.text = df.text.str.replace(':', "")
df = df.sample(frac=1).reset_index(drop=True)

classifier = SentenceClassifier(model_name="roberta-base", max_length=64, labels_no=3)

classifier.load_dataset(df, validation_split=0.2)

classifier.fine_tune(epochs=10, learning_rate=5e-5)



text = "SELL bitcoin now!"

probabilities = classifier.predict_one(text)
probabilities

classes = config.classes
print(classes[np.argmax(probabilities)])
classifier.dump('./model')