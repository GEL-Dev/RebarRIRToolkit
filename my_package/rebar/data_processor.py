# -*- coding: utf-8 -*-
import csv
import os
import codecs

def find_row_by_name(target_name, target_column = None ):
    name_column='Name'
    """CSVファイルから指定した名前の行を取得する"""
    current_dir = os.path.dirname(__file__)
    # 2層上のディレクトリ
    two_levels_up = os.path.abspath(os.path.join(current_dir, '..', '..'))
    # CSVファイルのパス
    csv_path = os.path.join(two_levels_up, 'data','rebarShape.csv')
    # CSVファイルを開く
    data = []
    with codecs.open(csv_path, 'r', 'utf-8') as file:
        reader = csv.DictReader(file)

    
        for row in reader:
            if row['Name'] == target_name:
                if target_column is not None:
                    data.append(row)
                else:
                    data.append(row)
            else:
                data
    
    return data


