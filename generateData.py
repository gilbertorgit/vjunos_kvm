"""
---------------------------------
 Author: gilbertorgit
 Date: 03/2023
---------------------------------
"""
import sys

sys.path.append('/')
import pandas as pd
import json
import numpy as np
import openpyxl


class GenerateData:

    def __init__(self):
        # lab1_device_info.xlsx TABs
        self._VMX = {}
        self._VROUTER = {}
        self._SRX = {}
        self._VEX = {}
        self._VEVO = {}
        self._APSTRA = {}
        self._LINUX = {}
        self._merged_data = {}

    def generate_data_info(self, excel_file: str, *args):

        """
        Read Excel file
        """

        for tab_name in args:

            try:
                df = pd.read_excel(excel_file, sheet_name=tab_name)
            except ValueError as e:
                print(f"Error reading the sheet '{tab_name}': {e}")
                continue

            df['name'] = df['name'].replace({0: np.nan}).fillna(method='ffill')
            df = df.replace({None: np.nan})
            df = df.dropna(thresh=2)
            df = df.fillna('None')

            results = {}
            for name, g in df.groupby(by='name'):
                g = g.drop('name', axis=1)
                data = json.loads(g.to_json(orient='table'))['data']
                for d in data:
                    __ = d.pop('index')
                results[name] = {
                    'data': data
                }

            attribute_map = {
                'VMX': '_VMX',
                'VROUTER': '_VROUTER',
                'SRX': '_SRX',
                'VEX': '_VEX',
                'VEVO': '_VEVO',
                'APSTRA': '_APSTRA',
                'LINUX': '_LINUX'
            }

            attribute_name = attribute_map.get(tab_name)
            if attribute_name:
                setattr(self, attribute_name, results)

    @property
    def get_vmx(self):
        return self._VMX

    @property
    def get_vrouter(self):
        return self._VROUTER

    @property
    def get_srx(self):
        return self._SRX

    @property
    def get_vex(self):
        return self._VEX

    @property
    def get_vevo(self):
        return self._VEVO

    @property
    def get_apstra(self):
        return self._APSTRA

    @property
    def get_linux(self):
        return self._LINUX

    @property
    def get_merged_data(self):
        """
        Creates a merged data list based on the TABS
        :return:
        """

        self._merged_data = self.get_vmx
        self._merged_data = self.get_vrouter
        self._merged_data.update(self.get_srx)
        self._merged_data.update(self.get_vex)
        self._merged_data.update(self.get_vevo)
        self._merged_data.update(self.get_apstra)
        self._merged_data.update(self.get_linux)
        return self._merged_data
