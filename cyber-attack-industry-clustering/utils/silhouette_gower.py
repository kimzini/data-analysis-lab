from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
def silhouette_gower(matrix, n_clusters):
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        metric='precomputed',
        linkage='average'
    )
    labels = clustering.fit_predict(matrix)

    score = silhouette_score(matrix, labels, metric='precomputed')

    return score