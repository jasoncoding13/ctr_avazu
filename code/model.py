# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 22:38:44 2019

@author: Jason
@e-mail: jasoncoding13@gmail.com
"""

import sys
import xlearn as xl
from ctr_avazu.code.paramconfig import paramconfig
from ctr_avazu.code.utils import print_log

def train_ffm(
        train_libffm_path, test_libffm_path, model_path, pred_path, param):
    print_log(f'Training ffm from {train_libffm_path}')
    ffm = xl.create_ffm()
    ffm.setTrain(train_libffm_path)
    ffm.fit(param, model_path)

    ffm.setSigmoid()
    ffm.setTest(test_libffm_path)
    ffm.predict(model_path, pred_path)


def merge_id_proba(id_path, pred_path):
    with open(id_path, 'r') as f1, open(pred_path, 'r') as f2:
        ids, preds = f1.readlines(), f2.readlines()
        rows = [id_.rstrip() + ',' + pred for id_, pred in zip(ids, preds)]
        assert len(ids) == len(preds)
    return rows


def merge_prediction(
        pred_path_app, id_path_app, pred_path_site, id_path_site, submit_path):
    print_log('Merging predictions')
    rows = merge_id_proba(id_path_app, pred_path_app)
    rows += merge_id_proba(id_path_site, pred_path_site)
    with open(submit_path, 'w') as f:
        f.write('id,click\n')
        f.writelines(rows)


def main_model():
    train_ffm(paramconfig.training_libffm_path_app,
              paramconfig.test_libffm_path_app,
              paramconfig.model_path_app,
              paramconfig.prediction_path_app,
              paramconfig.ffm_param)
    train_ffm(paramconfig.training_libffm_path_site,
              paramconfig.test_libffm_path_site,
              paramconfig.model_path_site,
              paramconfig.prediction_path_site,
              paramconfig.ffm_param)
    merge_prediction(
            paramconfig.prediction_path_app,
            paramconfig.prediction_id_path_app,
            paramconfig.prediction_path_site,
            paramconfig.prediction_id_path_site,
            paramconfig.submission_path)


if __name__ == '__main__':
    main_model()
