# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 15:53:06 2019

@author: Jason
@e-mail: jasoncoding13@gmail.com
"""

import collections
import csv
import hashlib
import pickle
import sys
from ctr_avazu.code.paramconfig import paramconfig
from ctr_avazu.code.utils import get_device_id_csm, is_app, print_log

FIELDS_KEEPED = [
        'id', 'click', 'hour', 'banner_pos', 'device_id', 'device_ip',
        'device_model', 'device_conn_type', 'C14', 'C17', 'C20', 'C21',
        ]
FIELDS_KEEPED_FOR_SAMPLED = FIELDS_KEEPED + [
        'site_id', 'site_domain', 'site_category', 'app_id', 'app_domain',
        'app_category',
        ]
FIELDS_FEATURE = FIELDS_KEEPED + [
        'ad_id', 'ad_domain', 'ad_category', 'device_id_count',
        'device_ip_count', 'device_id_csm_count', 'device_id_csm_hour_count',
        ]
FIELDS_LIBFFM = [
        'hour', 'banner_pos', 'device_model', 'device_conn_type', 'C14', 'C17',
        'C20', 'C21', 'ad_id', 'ad_domain', 'ad_category', 'device_id_csm',
        'device_ip_csm', 'device_id_csm_hour'
        ]


def get_count_dict(train_path, test_path, dict_path):
    print_log('Getting count from ' + f'{train_path} {test_path}')
    device_id_cnt = collections.defaultdict(int)
    device_ip_cnt = collections.defaultdict(int)
    device_id_csm_cnt = collections.defaultdict(int)  # customize device_id
    device_id_csm_hour_cnt = collections.defaultdict(int)
    with open(paramconfig.training_data_path, 'r') as f1, \
            open(paramconfig.test_data_path, 'r') as f2:
        readers = [csv.DictReader(f1), csv.DictReader(f2)]
        for reader_name, reader in zip(['training', 'test'], readers):
            for i, row in enumerate(reader, 1):
                device_id_csm = get_device_id_csm(row)
                device_id_cnt[row['device_id']] += 1
                device_ip_cnt[row['device_ip']] += 1
                device_id_csm_cnt[device_id_csm] += 1
                device_id_csm_hour_cnt[device_id_csm+'_'+row['hour']] += 1
                if i % 1000000 == 0:
                    print_log(f'Counted {i} rows of {reader_name}')
    dct_cnt = {
            'device_id_cnt': device_id_cnt,
            'device_ip_cnt': device_ip_cnt,
            'device_id_csm_cnt': device_id_csm_cnt,
            'device_id_csm_hour_cnt': device_id_csm_hour_cnt,
            }
    with open(paramconfig.count_dict_path, 'wb') as f:
        pickle.dump(dct_cnt, f)
    print_log(f'pickle file is saved in {dict_path}')


def extract_feature(data_path, app_path, site_path, is_train):
    print_log(f'Extracting feature from {data_path} to {app_path}, {site_path}')
    with open(paramconfig.count_dict_path, 'rb') as f:
        dct_cnt = pickle.load(f)
    dct_history = collections.defaultdict(
            lambda: {'history': '', 'buffer': '', 'prev_hour': ''})

    with open(data_path, 'r') as f1, \
            open(app_path, 'w') as f2, \
            open(site_path, 'w') as f3:
        reader = csv.DictReader(f1)
        writer_app = csv.DictWriter(f2, fieldnames=FIELDS_FEATURE)
        writer_site = csv.DictWriter(f3, fieldnames=FIELDS_FEATURE)
        writer_app.writeheader()
        writer_site.writeheader()
        
        j, k = 0, 0
        for i, row in enumerate(reader, 1):
            if not is_train:
                row['click'] = 0.5
            _row = {field: row[field] for field in FIELDS_KEEPED}
            
            # Count Feature
            device_id_csm = get_device_id_csm(row)
            _row['device_id_count'] = dct_cnt['device_id_cnt'][row['device_id']]
            _row['device_ip_count'] = dct_cnt['device_ip_cnt'][row['device_ip']]
            _row['device_id_csm_count'] = dct_cnt['device_id_csm_cnt'][device_id_csm]
            _row['device_id_csm_hour_count'] = dct_cnt['device_id_csm_hour_cnt'][device_id_csm+'_'+row['hour']]

            if is_app(row):
                j += 1
                _row['ad_id'] = row['app_id']
                _row['ad_domain'] = row['app_domain']
                _row['ad_category'] = row['app_category']
                writer_app.writerow(_row)
            else:
                k += 1
                _row['ad_id'] = row['site_id']
                _row['ad_domain'] = row['site_domain']
                _row['ad_category'] = row['site_category']
                writer_site.writerow(_row)
            if i % 1000000 == 0:
                print_log(f'Wrote {j} rows for app {k} rows for site')


def hash_feature(feature):
    return str(int(hashlib.md5(feature.encode('utf8')).hexdigest(), 16)%(paramconfig.hash_feature_size))


def convert_feature(feature_path, libffm_path, id_path=None, is_train=True):
    print_log(f'Converting feature from {feature_path} to {libffm_path}')
    with open(feature_path, 'r') as f1, open(libffm_path, 'w') as f2:
        def write_helper(row, features):
            f2.write(row['click'] + ' ' + ' '.join(features) + '\n')
        if not is_train:
            f3 = open(id_path, 'w')

            def write_id(func):
                def wrapper(*args, **kwargs):
                    f3.write(row['id'] + '\n')
                    return func(*args, **kwargs)
                return wrapper

            @write_id
            def write_helper(row, features):
                f2.write(row['click'] + ' ' + ' '.join(features) + '\n')
        reader = csv.DictReader(f1)
        for i, row in enumerate(reader, 1):
            row['hour'] = row['hour'][-2:]
            if int(row['device_ip_count']) > 1000:
                row['device_ip_csm'] = row['device_ip']
            else:
                row['device_ip_csm'] = 'low'+row['device_ip_count']
            if int(row['device_id_count']) > 1000:
                row['device_id_csm'] = row['device_id']
            else:
                row['device_id_csm'] = 'low'+row['device_id_count']

            if int(row['device_id_csm_hour_count']) > 30:
                row['device_id_csm_hour'] = 'freq'
            else:
                row['device_id_csm_hour'] = row['device_id_csm_hour_count']

            features = [
                    '{0}:{1}:1'.format(
                            j, hash_feature(f'{field}:{row[field]}'))
                    for j, field in enumerate(FIELDS_LIBFFM)]

            write_helper(row=row, features=features)
            if i % 1000000 == 0:
                print_log(f'Wrote {i} rows')
    if not is_train:
        f3.close()
        print_log(f'Wrote id to {id_path}')


def main_feature():
    get_count_dict(
            paramconfig.training_data_path,
            paramconfig.test_data_path,
            paramconfig.count_dict_path)
    extract_feature(
            paramconfig.training_data_path,
            paramconfig.training_feature_path_app,
            paramconfig.training_feature_path_site,
            is_train=True)
    extract_feature(
            paramconfig.test_data_path,
            paramconfig.test_feature_path_app,
            paramconfig.test_feature_path_site,
            is_train=False)
    convert_feature(
            paramconfig.training_feature_path_app,
            paramconfig.training_libffm_path_app,
            is_train=True)
    convert_feature(
            paramconfig.training_feature_path_site,
            paramconfig.training_libffm_path_site,
            is_train=True)
    convert_feature(
            paramconfig.test_feature_path_app,
            paramconfig.test_libffm_path_app,
            is_train=False,
            id_path=paramconfig.prediction_id_path_app)
    convert_feature(
            paramconfig.test_feature_path_site,
            paramconfig.test_libffm_path_site,
            is_train=False,
            id_path=paramconfig.prediction_id_path_site)


if __name__ == '__main__':
    main_feature()
