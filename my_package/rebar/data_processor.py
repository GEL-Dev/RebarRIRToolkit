# -*- coding: utf-8 -*-
import csv
import os


def find_row_by_name(target_name, target_column = None ):
    current_dir = os.path.dirname(__file__)
    two_levels_up = os.path.abspath(os.path.join(current_dir, '..', '..'))
    csv_path = os.path.join(two_levels_up, 'data','rebarShape.csv')
    data = []
    with open(csv_path, mode='r') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            # 'Name'を含むキーを見つける
            for key in row.keys():
                if 'Name' in key:
                    name_key = key
                    break
            else:
                # 'Name'を含むキーがない場合は次の行へ
                continue

            if row[name_key] == target_name:
                if target_column:
                    # 特定の列のみを追加
                    data.append(row[target_column])
                else:
                    # 全ての列を追加
                    data.append(row)

    return data

print(find_row_by_name('00'))