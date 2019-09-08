# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:34:59 2019

@author: Jason
@e-mail: jasoncoding13@gmail.com
"""

import os
import sys


def get_device_id_csm(row):
    # There are too many samples with `device_id = 'a99f214a'`.
    # So that we use `device_model` to idendity different samples here.
    if row['device_id'] == 'a99f214a':
        device_id_csm = 'device_ip:' + row['device_ip'] + '_device_model:' + \
                row['device_model']
    else:
        device_id_csm = 'device_id:' + row['device_id']
    return device_id_csm


def is_app(row):
    # Samples with `site_id = '85f751fd'` have too many different `app_id`.
    return True if row['site_id'] == '85f751fd' else False


def is_device_id_equal_device_id_csm(row):
    return False if row['device_id'] == 'a99f214a' else True


def print_log(string):
    sys.stdout.write(string+'\n')
    sys.stdout.flush()


def make_dir(paths):
    for path in paths:
        if not os.path.exists(path):
            os.mkdir(path)