# Libraries
from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud, STOPWORDS

# directory path
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

# text data from file
text = open(path.join(d, 'text.txt')).read()

# load mask
alice_mask = np.array(Image.open(path.join(d, "mask.png")))

# Create wordcloud
wc = WordCloud(background_color="white", max_words=2000,
               mask=alice_mask).generate(text)

# Write to local file
wc.to_file(path.join(d, "out.png"))

# Show on matplotlib graph
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")
plt.figure()
plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis("off")
plt.show()
