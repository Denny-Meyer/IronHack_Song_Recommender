import numpy as np
import pandas as pd
import pickle
from sklearn import datasets # sklearn comes with some toy datasets to practise
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.metrics import silhouette_score
import os
import matplotlib.pyplot as plt


# take model with k 10
model_file = '../data/models/kmeans_34.pickle'

#model_file = '../data/models/kmeans_10.pickle'
scaler_file = '../data/models/scaler.pickle'
data_file = '../data/song_data.csv'

class ClusterNetwork:


    def __init__(self) -> None:
        self.raw_data = None
        self.cluster_data = None
        self.scaled_cluster_data = None
        self.scaled_cluster_df = None
        self.scaler = None
        self.kmeans = None
        self.labels = None

        if model_file != '':
            self.kmeans = self.load_pickle_model(model_name=model_file)
        if scaler_file != '':
            self.scaler = self.load_pickle_model(model_name=scaler_file)
        if data_file != '':
            self.raw_data = pd.read_csv(data_file)
            self.raw_data.drop(columns='Unnamed: 0', inplace=True)
            self.cluster_data = self.raw_data._get_numeric_data()

            self.set_scaler_on_cluster_data()
            self.create_scaled_data()
            self.set_labels()
        pass
    
    # old tradition, set_get methods for work data
    
    '''
    ToDo: running kmean cycle
    '''
    
    
    def set_scaler_on_cluster_data(self) -> None:
        self.scaler = StandardScaler()
        self.scaler.fit(self.cluster_data)
        

    def create_scaled_data(self):
        self.scaled_cluster_data = self.scaler.transform(self.cluster_data)
        self.scaled_cluster_df = pd.DataFrame(self.scaled_cluster_data)
        print(self.scaled_cluster_df)

    
    def create_and_train_cluster(self, n_cluster=20, random_state=42) -> None:
        self.kmeans = KMeans(n_clusters=n_cluster, random_state=random_state)
        self.kmeans.fit(self.scaled_cluster_df)
        pass

    
    
    def set_labels(self):
        self.labels = self.kmeans.predict(self.scaled_cluster_data)
        self.raw_data['cluster'] = self.labels
        print(self.labels)

    # todo set data

    def get_cluster_from_new_input(self, new_val):
        res_new = pd.DataFrame(new_val)
        res_num = res_new._get_numeric_data()
        res_num_scaled = self.scaler.transform(res_num)
        res_clust = self.kmeans.predict(res_num_scaled)
        result = self.raw_data[self.raw_data['cluster'] == res_clust[0]].sample()
        return result['id']


    def run_cluster_cycle(self) -> None:
        self.set_scaler_on_cluster_data()
        self.create_and_train_cluster()
    

    def get_cluster_from_data(self, request_data):
        req_scaled = self.scaler.transform(request_data)
        req_pred = self.kmeans.predict(req_scaled)
        return req_pred
    
    
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
    
    
    '''
    Helper functions to setup kmean, store and load models
    '''

    def load_pickle_model(self, model_name: str):
        if os.path.isfile(model_name):
            with open(model_name, 'rb') as f:
                return pickle.load(file=f)
        else:
            print('could not found model or path')
    


    def save_kmean_model(self, model_object: KMeans, model_name: str) -> None:
        if os.path.isdir('../data/models/'):
            with open(model_name+'.pickle', 'wb') as f:
                pickle.dump(model_object, file=f)
        else:
            print('could not found path data/models')