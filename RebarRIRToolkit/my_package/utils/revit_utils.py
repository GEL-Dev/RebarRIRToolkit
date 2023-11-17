# -*- coding: utf-8 -*-
import rhinoinside_utils

from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory
from Autodesk.Revit.DB import Transaction
from RhinoInside.Revit import Revit

def get_active_doc():
    """現在のRevitドキュメントを取得する"""
    return Revit.ActiveDBDocument

def start_transaction(doc, transaction_name):
    """トランザクションを開始する"""
    transaction = Transaction(doc, transaction_name)
    transaction.Start()
    return transaction

def commit_transaction(transaction):
    """トランザクションをコミットする"""
    transaction.Commit()