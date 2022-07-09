import logging
from exception import AppException
import sys
from sklearn.cluster import KMeans
from kneed import KneeLocator
from File_operations import FileOperations

class Clustering:
    def __init__(self):
        self.fileop = FileOperations()
        logging.basicConfig(filename="logs/training/data_clustering/clustering_logs",
                            filemode='a',
                            level=logging.INFO,
                            format='%(asctime)s: %(levelname)s:: %(message)s)')


    def elbowPlot(self, data):

        """
        Finding actual value to create by using Elbow Plot method
        :param data:
        :return:
        """

        logging.info("Finding actual number of cluster by using elbow plot")
        try:
            wcss = []

            for i in range(1, 20):
                kmeans = KMeans(n_clusters=i, init="k-means++", random_state=20)
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)

            kn = KneeLocator(range(1, 20), wcss, curve='convex', direction='decreasing')

            logging.info("Proper value for cluster is :"+ str(kn.knee))

            return kn.knee


        except Exception as e:
            raise  AppException(e, sys)


    def createClusters(self, data):

        """
        Creating clusters of dataset to follow the Customized ML approach
        :param data:
        :return:
        """

        knee = self.elbowPlot(data)

        try:
            logging.info("data clustering")

            kmeans = KMeans(n_clusters=knee, init="k-means++", random_state=20)
            y_kmeans = kmeans.fit_predict(data)
            self.fileop.saveModel('Kmeans', kmeans)
            logging.info("Completed data clustering")

            return y_kmeans

        except Exception as e:
            raise AppException(e, sys)
