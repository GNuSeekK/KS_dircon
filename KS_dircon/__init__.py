# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 10:56:56 2022
v0.0.1 - 모듈 배포
v0.0.4 - file_matching 추가
@author: 이기성

class
----------
dir_control : directory control obejct

function
----------
create_directory
"""
import os
import Keesung_logging
import zipfile

__version__ = 'v0.0.4'

def create_directory(directory: str, bool_file: bool=True):
    """_summary_

    Args:
        directory (str): 파일 or 폴더 경로
        bool_file (bool, optional): 파일이름이면 True, 경로면 Flase. Defaults to True.
    """    
    if bool_file == True:
        directory = os.path.dirname(directory)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")
        
class Dir_Controller(Keesung_logging.my_logger):
    """
    function
    ----------
    make_zip : zip 파일 생성.
    directory_search : 경로의 모든 file_list, folder_list 리턴.
    """
    
    def __init__(self):
        self.ori_path = os.path.dirname(os.path.abspath(__file__))
        self.dirname = ''
        super().__init__()
    
    def directory_search(self, dirname: str):
        """_summary_

        Args:
            dirname (str): 탐색 경로

        Returns:
            list: file_list, dir_list
        """
        if os.path.isdir(dirname):
            self.info(f'directory_search - {dirname} 탐색 시작')
            self.dirname = dirname
            file_list = []
            dir_list = []
            # 디렉토리의 파일 이름을 탐색한다
            filenames = os.listdir(dirname)
            for filename in filenames:
                full_filename = os.path.join(dirname, filename)
                if os.path.isdir(full_filename): 
                    # 해당 경로가 존재 할 경우 재귀 함수를 이용해 재탐색 하여 배열을 더해준다
                    dir_list.append(full_filename)
                    tmp_x, tmp_y = self.directory_search(full_filename)
                    file_list += tmp_x
                    dir_list += tmp_y
                else:
                    # 경로가 아닐 경우 해당 파일명을 리스트에 더해준다
                    file_list.append(full_filename)
            self.info(f'directory_search - {dirname} 탐색 종료')
            return file_list, dir_list
        else:
            self.error(f'{dirname} 경로가 존재하지 않습니다')
            return None, None
    
    def make_zip(self, zipname: str, file_path: str, file_list: list, save_path: str):
        """_summary_

        Args:
            zipname (str): 압축할 파일의 이름
            file_path (str): 압축 파일들의 최상위 경로
            file_list (list): 압축할 파일의 리스트
            save_path (str): 저장 위치
        """
        with zipfile.ZipFile(os.path.join(save_path, f'{zipname}.zip'), 'w') as zip_obj:
            self.info(f'{zipname} 압축 시작')
            for file in file_list:    
                zip_obj.write(file, 
                              file.replace(file_path + '\\', ''), 
                              compress_type=zipfile.ZIP_DEFLATED)
            self.info(f'{zipname} 압축 종료')
            
    def file_name_extract(self, text):
        text = os.path.splitext(os.path.split(text)[-1])[0]
        return text
    
    def img_json_matching(self, img_list: list, json_list: list):
        """_summary_

        Args:
            img_list (list): 비교할 image 리스트
            json_list (list): 비교할 json 리스트

        Returns:
            dictionary: {'파일명(확장자 제외)' : [이미지경로, json경로]}
        """        
        all_dict = {}
        for img_path in img_list:
            file_name = self.file_name_extract(img_path)
            all_dict[file_name] = [img_path]

        for json_path in json_list:
            file_name = self.file_name_extract(json_path)
            if file_name in all_dict:
                all_dict[file_name].append(json_path)
            else:
                self.error(f'{json_path}와 매칭되는 image파일이 없습니다')

        pop_list = []
        for key, value in all_dict.items():
            if len(value) != 2:
                pop_list.append(key)
                self.error(f'{value[0]}와 매칭되는 json파일이 없습니다')
        for tmp in pop_list:
            all_dict.pop(tmp, None)
        return all_dict
    
    def file_matching(self, list_of_file_list: list, naming_list: list):
        """_summary_

        Args:
            list_of_file_list (list): [List, List, ...]
            naming_list (list): [str, str, ...]

        Returns:
            dictionary : {
                'naming_list[0]' : list_of_file_list[0],
                'naming_list[1]' : list_of_file_list[1],
            }
        """        
        all_dict = {}
        
        for name, data in zip(naming_list, list_of_file_list):
            for file_path in data:
                file_name = self.file_name_extract(file_path)
                if file_name not in all_dict:
                    all_dict[file_name] = {}
                all_dict[file_name][name] = file_path
                
        pop_list = []
        for key, value in all_dict.items():
            if len(value.keys()) != len(naming_list):
                pop_list.append(key)
                self.error(f'{key} 파일과 매칭되는 파일이 {len(naming_list) - len(value.keys())}개 부족합니다.')
        for tmp in pop_list:
            all_dict.pop(tmp, None)
        return all_dict