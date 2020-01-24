#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pickle


class Pickler:
    @staticmethod
    def read_pickle(filename):
        with open(filename, 'rb') as pick:
            data = pickle.Unpickler(pick).load()
        return data

    @staticmethod
    def save_pickle(filename, data):
        with open(filename, 'wb') as pick:
            pickle.Pickler(pick).dump(data)
        return data
