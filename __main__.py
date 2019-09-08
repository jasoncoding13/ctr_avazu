# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 16:09:13 2019

@author: Jason
@e-mail: jasoncoding13@gmail.com
"""

import time
from ctr_avazu.code.paramconfig import paramconfig
from ctr_avazu.code.feature import main_feature
from ctr_avazu.code.model import main_model
from ctr_avazu.code.utils import make_dir


if __name__ == '__main__':
    start = time.time()
    make_dir([paramconfig.feature_path, paramconfig.model_path, paramconfig.prediction_path])
    main_feature()
    main_model()
    print('Total time: ', time.time()-start)