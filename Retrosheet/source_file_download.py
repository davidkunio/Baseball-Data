# encoding: utf-8
# python3.6

import os
import sys
import zipfile
import requests
from datetime import date

dir_path = os.path.dirname(os.path.realpath(__file__))
top_path = '\\'.join(dir_path.split('\\')[:2])
sys.path.append(top_path+'Retrosheet')

class FileDownload:

    def __init__(self):

        os.chdir(top_path)
        print(top_path)

        self.start_year = 1980

        self.event_reg_filename = '{}eve.zip'
        self.event_reg_url = 'https://www.retrosheet.org/events/'
        self.event_reg_src_loc = top_path+'\\RetrosheetSource\\Events\\'
        self.event_post_filename = '{}post.zip'
        self.event_post_url = 'https://www.retrosheet.org/events/'
        self.event_post_src_loc = top_path+'\\RetrosheetSource\\Events\\'

        self.game_log_filename = 'gl{}.zip'
        self.game_log_url = 'https://www.retrosheet.org/gamelogs/'
        self.game_log_src_loc = top_path+'\\RetrosheetSource\\GameLog\\'
        self.game_log_post_list = ['wc','dv','lcs','ws']

        self.sched_filename = '{}SKED.ZIP'
        self.sched_url = 'http://www.retrosheet.org/schedule/'
        self.sched_src_loc = top_path+'\\RetrosheetSource\\Schedule\\'

        self.ref_data_loc = top_path+'\\RetrosheetSource\\Reference\\'
        self.id_url = 'https://www.retrosheet.org/retroID.htm'
        self.ballparks_url = 'https://www.retrosheet.org/parkcode.txt'
        self.rosters_url = 'https://www.retrosheet.org/Rosters.zip'

        self.src_type_lookup = {
            'event_reg':    (self.event_reg_url,    self.event_reg_src_loc, self.event_reg_filename),
            'event_post':   (self.event_post_url,   self.event_post_src_loc,self.event_post_filename),
            'game_log':     (self.game_log_url,     self.game_log_src_loc,  self.game_log_filename),
            'sched':        (self.sched_url,        self.sched_src_loc,     self.sched_filename),
            'ids':          (self.id_url,           self.ref_data_loc,      self.'retroID.txt'),
            'ballparks':    (self.ballparks_url,    self.ref_data_loc,      self.'parkcode.txt'),
            'rosters':      (self.rosters_url,      self.ref_data_loc,      self.'Rosters.zip'),
            }

    def request_page(self,target_url):
        r = requests.get(target_url, stream=True)
        return r

    def save_file(self,page_contents,target_loc):
        with open(target_loc, 'wb') as fd:
            for chunk in page_contents.iter_content(chunk_size=chunk_size):
                fd.write(chunk)
        return 1

    def download_files(self,type,modifier,chunk_size=128):

        if not os.path.exists(self.src_type_lookup[type][1]):
            os.makedirs(self.src_type_lookup[type][1])

        target_url = self.src_type_lookup[type][0]+self.src_type_lookup[type][2].format(modifier)
        target_loc = self.src_type_lookup[type][1]+self.src_type_lookup[type][2].format(modifier)

        page_contents = self.request_page(target_url)
        self.save_file(page_contents,target_loc)
        return self.src_type_lookup[type][2].format(modifier)

    def download_all(self,type,modifier_type=None):

        if type in ['ballparks','rosters']:
            self.download_files(type,None)
        elif: type == 'ids':
            pass
        else:
            year_range = (self.start_year,date.today().year)
            for y in range(*year_range):
                self.download_files(type,y)
            if type =='game_log':
                for m in self.game_log_post_list:
                    self.download_files(type,m)
