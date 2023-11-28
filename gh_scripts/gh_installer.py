"""Provides a scripting component.
    Inputs:
        _install: bool:
    Output:
        message: string: The a output variable"""

__author__ = "ykish"
__version__ = "2023.11.24"


ghenv.Component.Name = 'RebarToolkit Installer'
ghenv.Component.NickName = 'RTInstall'
ghenv.Component.Message = '0.0.1'
ghenv.Component.Category = 'RebarToolkit'
ghenv.Component.SubCategory = '1 :: Version'
ghenv.Component.AdditionalHelpFromDocStrings = '0'

import clr
clr.AddReference("System.Net")
import os
import io
import subprocess
import System.Net
import System.Windows.Forms
import shutil
from distutils import dir_util
import Rhino
from Rhino.RhinoApp import Version as RHINO_VERSION
from Grasshopper.Folders import UserObjectFolders, DefaultAssemblyFolder
from Grasshopper.Kernel import GH_RuntimeMessageLevel as Message
from System import Array
from System.Net import WebClient
from System.IO import Path, Directory
import zipfile
import json

def get_latest_release_zip_url(repo):
    """GitHubのAPIを使用して最新のリリースのZIPファイルのURLを取得する"""
    api_url = "https://api.github.com/repos/{}/releases/latest".format(repo)
    client = WebClient()
    client.Headers.Add("User-Agent", "request")
    release_info = client.DownloadString(api_url)
    release_data = json.loads(release_info)
    return release_data["zipball_url"]
    
def download_zip_from_url(url, save_dir):
    """指定されたURLからZIPファイルをダウンロードし、指定されたディレクトリに保存する"""
    client = WebClient()
    client.Headers.Add("User-Agent", "request")
    filename = os.path.join(save_dir, "latest_release.zip")
    client.DownloadFile(url, filename)
    return filename

def unzip_file(zip_filepath, dest_dir,folders_to_extract,specific_destinations):
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        for item in zip_ref.infolist():
            path_parts = item.filename.split('/')
            # 2番目のフォルダ名を取得（トップレベルフォルダが1つのみの場合）
            second_level_folder = path_parts[1] if len(path_parts) > 1 else None

            # 2番目のフォルダが特定のフォルダに属する場合、適切なディレクトリに解凍
            if second_level_folder in folders_to_extract:
                destination = specific_destinations.get(second_level_folder, dest_dir)

                # 完全な解凍先のパスを生成
                full_path = os.path.join(destination, *path_parts[1:])

                # ディレクトリの作成
                if item.filename.endswith('/') and not os.path.isdir(full_path):
                    print(full_path)
                    os.makedirs(full_path)
                # ファイルの解凍
                else:
                    # 元のフォルダ構造を無視して特定のパスにファイルを解凍
                    with zip_ref.open(item) as source, open(full_path, 'wb') as target:
                        shutil.copyfileobj(source, target)

    # ZIPファイルの削除（エラー処理を追加する場合はここで）
    os.remove(zip_filepath)
            
# リポジトリのユーザー名/名前
repo = "GEL-Dev/RebarRIRToolkit"

# 保存するディレクトリ
save_dir = os.path.join(os.environ["LOCALAPPDATA"], "GEL", "RebarToolkit")
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
    

# 最新のリリースZIPのURLを取得
latest_release_url = get_latest_release_zip_url(repo)
#print(latest_release_url)


folders_to_extract = {'my_package', 'gh_scripts', 'userObject'}
specific_destinations = {
    'my_package': save_dir,
    'gh_scripts': save_dir,
    'userObject': UserObjectFolders
}
# ZIPファイルをダウンロードして解凍
zip_path = download_zip_from_url(latest_release_url, save_dir)
#print(zip_path)
unzip_file(zip_path, save_dir,folders_to_extract,specific_destinations)

my_package_dir = os.path.join(save_dir,"my_package")
#print(my_package_dir)

    
_install = True
if _install:
    new_path = _new_path
    if new_path:
        current_paths = list(Rhino.Runtime.PythonScript.SearchPaths)
        if new_path not in current_paths:
            current_paths.append(new_path)
            Rhino.Runtime.PythonScript.SearchPaths = Array[str](current_paths)
        #print(Rhino.Runtime.PythonScript.SearchPaths)

