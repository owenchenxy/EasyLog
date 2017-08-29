#_*_coding:utf-8_*_

from PathSearch import path_searcher
from LogPathVar import PathPrefix
import sys,os,json#,re
class log_filter(object):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'other')
   
    def filter_by_message(self):
        
        with open (self.path,'rb') as original_log:
                message=raw_input('input the message to search:     ')
                with open (PathPrefix+self.sr+os.sep+self.name+'.filter_by_message_%s'%message,'w') as log_filter_by_message:
                        for line in original_log.readlines():
                                if message in line:
                                        log_filter_by_message.write(line)
                print("filter result location:\n"+PathPrefix+self.sr+os.sep+self.name+'.filter_by_message_%s'%message)    
                view_now=raw_input("Do you want to view the result right now?(y/n):")
                if view_now=='y' or view_now=='Y':
                    with open(PathPrefix+self.sr+os.sep+self.name+'.filter_by_message_%s'%message,'r') as f:
                        for line in f.xreadlines():
                            print line.strip()
                else:
                    sys.exit("Thanks for using")

class cisco_log_filter(log_filter):
    
    def get_command_list(self,command_list_name):
        command_list_path='.'+os.sep+'lib'+os.sep+command_list_name
        if os.path.exists(command_list_path):
            pass
        else:
            print('Initializing...Please wait...')
            with open(self.path,'rb') as f:
                with open(command_list_path,'wb') as f1:
                    for line in f.readlines():
                        if(line[0]=='`'):
                            line=line.strip().strip('`')
                            f1.write(line+'\n')
            print('Initialization Completed!')
                         
    def command_finder(self):
            with open(self.command_list_file,'rb') as command_list:
                list_contents=command_list.readlines()
                while True:
                    command_part=raw_input('# ')
                    command_found_list=[]
                    
                    for line in list_contents:
                        if command_part in line:
                            command_found_list.append(line.strip('\n'))
                    if len(command_found_list)==0:
                        print('command not found')
                        continue
                    elif len(command_found_list)==1:
                        print('# '+command_found_list[0].strip())
                        return command_found_list[0].strip()
                    else:
                        input_error=0
                        for k,v in enumerate(command_found_list,1):
                            print k,v
                        try:
                            final_command_index=int(raw_input("which command do you want:"))
                            final_command=command_found_list[final_command_index-1].strip()
                            print('# '+final_command)
                            return final_command
                        except Exception:
                            input_error=1
                    if input_error==1:
                        print('invalid index')
                        continue    
    
    def search_segment(self,search_sub_seg,command_start_position,original_log,seg_searched):
        while search_sub_seg=='y' or search_sub_seg=='Y':                            
                            #������������е��ض�����
                            while True:
                                search_sub_seg=raw_input('\nDo you want to search sub segment in the output?(y/n)')
                                if(search_sub_seg=='y' or search_sub_seg=='Y'):
                                    if len(seg_searched)==0:
                                        seg_searched.append(1)    #ʹ����б�Ϊ��
                                    segment_keyword=raw_input('Keyword: ')
                                    original_log.seek(command_start_position)
                                    seg_found=0
                                    
                                    while seg_found==0:
                                        seg_content=original_log.readline()
                                        if seg_content[0]=='`':
                                            break
                                        if not (seg_content=='\n' or seg_content=='\r\n'):#������ǿ��У����жϹؼ����ڲ��ڸ���
                                            if segment_keyword in seg_content:  #����ؼ��ʳ��ֵ�һ���ǿ��У���ʼ���������
                                                seg_found=1
                                                print seg_content.strip()
                                                #loop
                                                end_of_seg=0
                                                while end_of_seg==0:
                                                    seg_content=original_log.readline()
                                                    if not (seg_content=='\n' or seg_content=='\r\n'):#��������Ĳ��ǿ���,���ӡ���������������¶�
                                                        print seg_content.strip()
                                                        continue
                                                    else:       #��������˿��У��Ͳ��ټ�����
                                                        end_of_seg=1
                                                        break
                                                continue    
                                                #loop
                                            else:#����ؼ��ֲ������ڵ�һ���ǿ���,��һֱ����ֱ��������һ������
                                                #LOOP
                                                while True:
                                                    seg_content=original_log.readline()
                                                    if (seg_content=='\n' or seg_content=='\r\n'):
                                                        break
                                                    else:
                                                        continue
                                                #LOOP 
                                                continue #������һ�����к󣬼���
                                                   
                                        else:  #����ǿ��У������ж���һ��
                                            continue                        
                                else:#������벻��yes���Ͳ����ж�����Ѱ
                                    break
        return  seg_searched                      
                        
    def filter_by_command(self):
        with open(self.path,'rb') as original_log:
            #loop
            while True:
                flag_found=0
                command_to_search=self.command_finder()   #��ȡ�Ϸ������һ�����Ի�ȡ��
                #LOOP
                while True:
                    line=original_log.readline().strip()
                    if '`%s`'%command_to_search ==line:
                        flag_found=1
                        
                        command_start_position=original_log.tell()
                        search_sub_seg='Y'
                        seg_searched=list()
                        seg_searched=self.search_segment(search_sub_seg,command_start_position,original_log,seg_searched)
                            #���û��ѡ����ж�����Ѱ������������������ݣ����ѡ����ж�����Ѱ���Ͳ��������������������
                        if (len(seg_searched)==0):    #������Ǹ����б���ʾû�н��й��������
                            while True:
                                content=original_log.readline()
                                
                                if content[0]=='`':
                                    break
                                else:
                                    print content.strip()
                                    continue
                        #LOOP
                    if flag_found==1:
                        break
                #LOOP    
                flag_continue=raw_input('Continue other command?(Y/N)')   #�˴�flag_foundһ������1����Ϊһ����������Ա��ҵ�
                if flag_continue=='N' or flag_continue=='n':
                    break
                else:
                    original_log.seek(0)
                    continue
#command_list ��ÿ����ľ�̬�ֶΣ���ͨ������ֱ�ӵ��ã�Ҳ��ͨ��������� 
'''
class brocade_supportshow_filter(cisco_log_filter):   
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'brocade')
        self.get_command_list('brocade_supportshow_command_list')
        
        
    command_list_file='.'+os.sep+'lib'+os.sep+'brocade_supportshow_command_list'
    
    def get_command_list(self,command_list_name):
        command_list_path='.'+os.sep+'lib'+os.sep+command_list_name
        if os.path.exists(command_list_path):
            pass
        else:
            print('Initializing...Please wait...')
            with open(self.path,'rb') as f:
                with open(command_list_path,'wb') as f1:
                    for line in f.readlines():
                        line=line.strip()
                        if(line[-8:]=='       :'):
                            line=line.strip(':').strip()
                            f1.write(line+'\n')
            print('Initialization Completed!')
    def search_segment(self,search_sub_seg,command_start_position,original_log,seg_searched):
        while search_sub_seg=='y' or search_sub_seg=='Y':                            
                            #������������е��ض�����
                            while True:
                                search_sub_seg=raw_input('\nDo you want to search sub segment in the output?(y/n)')
                                if(search_sub_seg=='y' or search_sub_seg=='Y'):
                                    if len(seg_searched)==0:
                                        seg_searched.append(1)    #ʹ����б�Ϊ��
                                    segment_keyword=raw_input('Keyword: ')
                                    original_log.seek(command_start_position)
                                    seg_found=0
                                    
                                    while seg_found==0:
                                        seg_content=original_log.readline()
                                        if seg_content.strip()[-8:]=='       :':
                                            break
                                        if not (seg_content=='\n' or seg_content=='\r\n'):#������ǿ��У����жϹؼ����ڲ��ڸ���
                                            if segment_keyword in seg_content:  #����ؼ��ʳ��ֵ�һ���ǿ��У���ʼ���������
                                                seg_found=1
                                                print seg_content.strip()
                                                #loop
                                                end_of_seg=0
                                                while end_of_seg==0:
                                                    seg_content=original_log.readline()
                                                    if not (seg_content=='\n' or seg_content=='\r\n'):#��������Ĳ��ǿ���,���ӡ���������������¶�
                                                        print seg_content.strip()
                                                        continue
                                                    else:       #��������˿��У��Ͳ��ټ�����
                                                        end_of_seg=1
                                                        break
                                                continue    
                                                #loop
                                            else:#����ؼ��ֲ������ڵ�һ���ǿ���,��һֱ����ֱ��������һ������
                                                #LOOP
                                                while True:
                                                    seg_content=original_log.readline()
                                                    if (seg_content=='\n' or seg_content=='\r\n'):
                                                        break
                                                    else:
                                                        continue
                                                #LOOP 
                                                continue #������һ�����к󣬼���
                                                   
                                        else:  #����ǿ��У������ж���һ��
                                            continue                        
                                else:#������벻��yes���Ͳ����ж�����Ѱ
                                    break
        return  seg_searched
    def filter_by_command(self):
        with open(self.path,'rb') as original_log:
            #loop
            while True:
                flag_found=0
                command_to_search=self.command_finder()   #��ȡ�Ϸ������һ�����Ի�ȡ��
                
                #LOOP
                while True:
                    line=original_log.readline()
                    
                    if re.match(r'%s(\s{6,9}):'%command_to_search,line):
                        flag_found=1
                        command_start_position=original_log.tell()
                        #search_sub_seg='Y'
                        #seg_searched=list()
                        #seg_searched=self.search_segment(search_sub_seg,command_start_position,original_log,seg_searched)
                            #���û��ѡ����ж�����Ѱ������������������ݣ����ѡ����ж�����Ѱ���Ͳ��������������������
                        #if (len(seg_searched)==0):    #������Ǹ����б���ʾû�н��й��������
                        while True:
                            #print 'haha'
                            content=original_log.readline()
                            #print content
                            if (content.strip()[-8:]=='       :'):
                                break
                            else:
                                print content.strip()
                                continue
                        #LOOP
                    if flag_found==1:
                        break
                #LOOP    
                flag_continue=raw_input('Continue other command?(Y/N)')   #�˴�flag_foundһ������1����Ϊһ����������Ա��ҵ�
                if flag_continue=='N' or flag_continue=='n':
                    break
                else:
                    original_log.seek(0)
                    continue                     
'''
class sam_techsupportinfo_filter(cisco_log_filter):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'fi')
        self.get_command_list('sam_techsupportinfo_command_list')
    command_list_file='.'+os.sep+'lib'+os.sep+'sam_techsupportinfo_command_list' 
class sw_techsupportinfo_filter(cisco_log_filter):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'fi')
        self.get_command_list('sw_techsupportinfo_command_list')
    command_list_file='.'+os.sep+'lib'+os.sep+'sw_techsupportinfo_command_list'  
class mds_showtech_filter(cisco_log_filter):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'mds')
        self.get_command_list('mds_showtech_command_list')
    command_list_file='.'+os.sep+'lib'+os.sep+'mds_showtech_command_list'
class n5k_showtech_filter(cisco_log_filter):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'n5k')
        self.get_command_list('n5k_showtech_command_list')
    command_list_file='.'+os.sep+'lib'+os.sep+'n5k_showtech_command_list'  
     
class vmkernel_filter(log_filter):
    def __init__(self,sr_number,log_name):
        self.sr=sr_number
        self.name=log_name
        self.path=path_searcher.path_search(self.sr, self.name,'vmkernel')
    
    def filter_by_time(self):
        
        with open (self.path,'rb') as original_log:
                    starttime=int(raw_input('Start Time(YYMMDDhhmmss):'))
                    endtime=int(raw_input('End Time(format:YYYYMMDDhhmmss):'))
                    with open (PathPrefix+self.sr+os.sep+self.name+'.filter_by_time_%s-%s'%(starttime,endtime),'w') as log_filter_by_time:
                            for line in original_log.readlines():
                                    timestr=line[0:4]+line[5:7]+line[8:10]+line[11:13]+line[14:16]+line[17:19]
                                    if timestr.isdigit():
                                            timestamp=int(timestr)
                                            if starttime<=timestamp and endtime>=timestamp:
                                                    log_filter_by_time.write(line)
                    print("filter result location:\n"+PathPrefix+self.sr+os.sep+self.name+'.filter_by_time_%s-%s'%(starttime,endtime))           #loop
class esxi_host_filter(log_filter):
    def __init__(self,sr_number):
        self.sr=sr_number
        self.command_list_path=PathPrefix+self.sr+os.sep+'command_list'
        self.command_dict_path=PathPrefix+self.sr+os.sep+'command_dict'
        
    def get_esxi_command_dict_list(self):
        
        if (os.path.exists(self.command_dict_path) and os.path.exists(self.command_list_path)):#����Ѿ���command_list�ļ����ٴ�����
            command_dict=json.load(open(self.command_dict_path,'rb'))
            command_list=json.load(open(self.command_list_path,'rb'))
            return command_dict,command_list
        
        else:   #�����û��command_list������һ��command_list�ļ�(��command_dict���л�������������������)
            #loop Ѱ��commands�ļ���
            print('Initializing....May take a while...Please wait...')
            command_folder_found=0
            for rootdir,subdirs,filenames in os.walk(PathPrefix+self.sr):
                for s in subdirs:
                    if s.split(os.sep)[-1]=='commands':
                        command_folder_found=1
                        command_folder=os.path.join(rootdir,s)
                        break
                if command_folder_found==1:
                    break
            #loop
            if command_folder_found==0:
                a=raw_input('No command list found.Press any key to exit!')
                sys.exit()
            #loop�ҵ���
            for rootdir,subdirs,filenames in os.walk(command_folder):
                command_list=list()
                command_dict=dict()
                #loop
                for f in filenames:
                    if 'esxcfg-info' in f:
                        pass
                    elif 'vsi_traverse' in f:
                        pass
                    elif 'cim-diagnostic' in f:
                        pass
                    elif 'esxcfg-resgrp' in f:
                        pass
                    elif 'vmware-vimdump' in f:
                        pass
                    elif 'smbios.bin' in f:
                        pass
                    else:   #��������õ����
                        command_output_file=os.path.join(rootdir,f)    #�������������ļ�·��
                        command_str=f.strip('.txt')                     #�����ַ���
                        command_list.append(command_str)                       #�������ַ������������б���
                        with open(command_output_file,'rb') as f1:      #����������ļ�������ȡ���ݣ��浽command_dict��Ӧ�ļ�ֵ��
                            command_dict[command_str]=f1.read()
                    #end loop ����commands�ļ����������ļ�
                command_list.sort()
                json.dump(command_dict,open(self.command_dict_path,'wb'))
                json.dump(command_list,open(self.command_list_path,'wb'))
                print('Initialization completed!')
                return command_dict,command_list 
    def command_finder(self): 
        #command_dict=self.get_esxi_command_list()[0]
        command_list=self.get_esxi_command_dict_list()[1]
        while True:
                    command_part=raw_input('$ ')
                    command_found_list=[]
                    
                    for item in command_list:
                        if command_part in item:
                            command_found_list.append(item.strip('\n'))
                    if len(command_found_list)==0:
                        print('command not found')
                        continue
                    elif len(command_found_list)==1:
                        print('$ '+command_found_list[0].strip())
                        return command_found_list[0].strip()
                    else:
                        input_error=0
                        for k,v in enumerate(command_found_list,1):
                            print k,v
                        try:
                            final_command_index=int(raw_input("which command do you want:"))
                            final_command=command_found_list[final_command_index-1].strip()
                            print('$ '+final_command)
                            return final_command
                        except Exception:
                            input_error=1
                    if input_error==1:
                        print('invalid index')
                        continue
    def filter_by_command(self):
        command_dict=self.get_esxi_command_dict_list()[0]
        while True: 
            key=self.command_finder()
            print command_dict[key]
            flag_continue=raw_input('Continue?(Y/N)')
            if (flag_continue=='n' or flag_continue=='N'):
                raw_input('press any key to exit')
                break
            else:
                continue
                          
                       