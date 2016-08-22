import Cython
import numpy as np
import pandas as pd
from scipy import linalg as LA
from nltk.corpus import stopwords
from sklearn import cluster, mixture
from sklearn.metrics import silhouette_samples, silhouette_score
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

stop = set(stopwords.words('english'))
stops = stop.union('symptoms')

# before beginning need to do:
# COPY (SELECT symptom, count(symptom) as cnt FROM psymptom group by symptom order by cnt desc)
# TO '/all_symptoms.csv' DELIMITER ',' CSV HEADER;

data = pd.read_csv('all_symptoms.csv')

data['symptom'] = data['symptom'].str.replace('[^\w\s]',' ')
data['symptom'] = data['symptom'].str.lower()
data['symptom'] = data['symptom'].str.replace('[0-9]',' ')

# building vocab model: Load Google's pre-trained Word2Vec model.
model = gensim.models.Word2Vec.load_word2vec_format('./GoogleNews-vectors-negative300.bin.gz', binary=True)

# assign each symptom a vector (sum of the word vectors)
n = data.shape[0] - 1
data = data.iloc[:n,:]
sym2vec = np.zeros((n,300))
sym2vecl2 = np.zeros((n,300))

isym = 0
for index, row in data.iterrows():
    print row['symptom']
    # split sentence into words
    w = row['symptom'].split()
    iword = 0
    words = filter(lambda x: x in model.vocab, w)
    for word in words:
        if word not in stop:
            print word
            if iword == 0:
                tot_vec = model[word]
            else:
                tot_vec += model[word]
            iword += 1

    tot_vec = tot_vec/LA.norm(tot_vec, ord=2)

    sym2vec[isym,:] = tot_vec
    isym += 1

print sym2vec

# if you want to try out different numbers of clusters

# check_clusters = False

# if check_clusters:
#     sil = np.zeros((101,2))
#     for no_clusters in range(70,130):
#         g = cluster.SpectralClustering(n_clusters=no_clusters, affinity='nearest_neighbors')

#         clusters = g.fit_predict(sym2vec)

#         silhouette_avg = silhouette_score(sym2vec, clusters)
#         print("For n_clusters =", no_clusters,"The average silhouette_score is :", silhouette_avg)
#         sil[no_clusters-30,0] = no_clusters
#         sil[no_clusters-30,1] = silhouette_avg

#     plt.plot([sil[:,0],sil[:,1]])
#     plt.show()

n_clusters = 300

g = cluster.SpectralClustering(n_clusters=n_clusters, affinity='nearest_neighbors')

clusters = g.fit_predict(sym2vec)

data['cluster'] = clusters

for name, group in data.groupby(['cluster']):
    print(name)
    print(group)

output = data.sort(['cluster'])

print output
output.to_csv('result.csv', index = False)