import numpy as np
import pandas as pd
import pickle
from sklearn import datasets # sklearn comes with some toy datasets to practise
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.metrics import silhouette_score
import os


class ClusterNetwork:


    def __init__(self) -> None:
        self.__cluster_data = None
        self.__scaled_cluster_data = None
        self.__scaler = None
        self.__kmeans = None
        self.__labels = None
        pass
    
    # old tradition, set_get methods for work data
    # also __private to prevent access from outside this class
    
    def set_cluster_data(self, data_frame: pd.DataFrame) -> None:
        self.__cluster_data = data_frame
    

    def get_cluster_data(self) -> pd.DataFrame:
        return self.__cluster_data


    def set_scaled_cluster_data(self, scaled_cluster_data) -> None:
        self.__scaled_cluster_data = scaled_cluster_data


    def get_scaled_cluster_data(self) -> pd.DataFrame:
        return self.__scaled_cluster_data

    
    '''
    ToDo: running kmean cycle
    '''
    
    
    def set_scaler_on_cluster_data(self) -> None:
        self.__scaler = StandardScaler()
        self.__scaler.fit(self.get_cluster_data())
        self.set_scaled_cluster_data = self.__scaler.transform(self.get_cluster_data())


    def create_and_train_cluster(self, n_cluster=8, random_state=42) -> None:
        self.__kmeans = KMeans(n_clusters=n_cluster, random_state=random_state)
        self.__kmeans.fit(self.get_scaled_cluster_data())
        self.__labels = self.__kmeans.predict(self.get_scaled_cluster_data)
        print(self.__labels)
        pass
    

    def run_cluster_cycle(self) -> None:
        if self.get_cluster_data != None:
            self.set_scaler_on_cluster_data()
            self.create_and_train_cluster()
        else:
            print('not possible without cluster data')
        pass
    
    
    '''
    Helper functions to setup kmean, store and load models
    '''

    def load_kmean_model(self, model_name: str) -> KMeans:
        if os.path.isfile('../data/models/'+model_name+'.pickle'):
            with open('../data/models'+model_name+'.pickle', 'rb') as f:
                return pickle.load(file=f)
        else:
            print('could not found model or path')


    def save_kmean_model(self, model_object: KMeans, model_name: str) -> None:
        if os.path.isdir('../data/models/'):
            with open('../data/models'+model_name+'.pickle', 'wb') as f:
                pickle.dump(model_object, file=f)
        else:
            print('could not found path data/models')