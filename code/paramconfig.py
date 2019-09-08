# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 14:29:54 2019

@author: Jason
@e-mail: jasoncoding13@gmail.com
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train_path', type=str)
parser.add_argument('--test_path', type=str)
args = parser.parse_args()

class ParamConfig():
    def __init__(self):
        self.data_path = './ctr_avazu/data'
        if args.train_path:
            self.training_data_path = args.train_path
        else:
            self.training_data_path = self.data_path + '/train_sample.csv'
        if args.test_path:
            self.test_data_path = args.test_path
        else:
            self.test_data_path = self.data_path + '/test_sample.csv'
        self.feature_path = './ctr_avazu/feature'
        self.count_dict_path = self.feature_path + '/count_dict.pickle'
        self.training_feature_path_app = self.feature_path + '/training_app.csv'
        self.training_feature_path_site = self.feature_path + '/training_site.csv'
        self.test_feature_path_app = self.feature_path + '/test_app.csv'
        self.test_feature_path_site = self.feature_path + '/test_site.csv'
        self.hash_feature_size = 1000000
        self.training_libffm_path_app = self.feature_path + '/training_app.txt'
        self.training_libffm_path_site = self.feature_path + '/training_site.txt'
        self.test_libffm_path_app = self.feature_path + '/test_app.txt'
        self.test_libffm_path_site = self.feature_path + '/text_site.txt'
        self.model_path = './ctr_avazu/model'
        self.model_path_app = self.model_path + '/model_app.out'
        self.model_path_site = self.model_path + '/model_site.out'
        self.prediction_path = './ctr_avazu/prediction'
        self.prediction_path_app = self.prediction_path + '/output_app.txt'
        self.prediction_path_site = self.prediction_path + '/output_site.txt'
        self.prediction_id_path_app = self.prediction_path + '/id_app.txt'
        self.prediction_id_path_site = self.prediction_path + '/id_site.txt'
        self.submission_path = './ctr_avazu/submission.csv'
        self.ffm_param = {'task': 'binary', 'lr': 0.03, 'lambda': 0.00002, 'epoch': 15}

paramconfig = ParamConfig()
