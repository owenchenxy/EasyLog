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
                            #查找命令输出中的特定段落
                            while True:
                                search_sub_seg=raw_input('\nDo you want to search sub segment in the output?(y/n)')
                                if(search_sub_seg=='y' or search_sub_seg=='Y'):
                                    if len(seg_searched)==0:
                                        seg_searched.append(1)    #使这个列表不为空
                                    segment_keyword=raw_input('Keyword: ')
                                    original_log.seek(command_start_position)
                                    seg_found=0
                                    
                                    while seg_found==0:
                                        seg_content=original_log.readline()
                                        if seg_content[0]=='`':
                                            break
                                        if not (seg_content=='\n' or seg_content=='\r\n'):#如果不是空行，则判断关键字在不在该行
                                            if segment_keyword in seg_content:  #如果关键词出现第一个非空行，则开始读下面的行
                                                seg_found=1
                                                print seg_content.strip()
                                                #loop
                                                end_of_seg=0
                                                while end_of_seg==0:
                                                    seg_content=original_log.readline()
                                                    if not (seg_content=='\n' or seg_content=='\r\n'):#如果读到的不是空行,则打印出来，并继续往下读
                                                        print seg_content.strip()
                                                        continue
                                                    else:       #如果读到了空行，就不再继续读
                                                        end_of_seg=1
                                                        break
                                                continue    
                                                #loop
                                            else:#如果关键字不出现在第一个非空行,则一直读，直到读到下一个空行
                                                #LOOP
                                                while True:
                                                    seg_content=original_log.readline()
                                                    if (seg_content=='\n' or seg_content=='\r\n'):
                                                        break
                                                    else:
                                                        continue
                                                #LOOP 
                                                continue #读到下一个空行后，继续
                                                   
                                        else:  #如果是空行，继续判断下一行
                                            continue                        
                                else:#如果输入不是yes，就不进行段落搜寻
                                    break
        return  seg_searched                      
                        
    def filter_by_command(self):
        with open(self.path,'rb') as original_log:
            #loop
            while True:
                flag_found=0
                command_to_search=self.command_finder()   #获取合法的命令，一定可以获取到
                #LOOP
                while True:
                    line=original_log.readline().strip()
                    if '`%s`'%command_to_search ==line:
                        flag_found=1
                        
                        command_start_position=original_log.tell()
                        search_sub_seg='Y'
                        seg_searched=list()
                        seg_searched=self.search_segment(search_sub_seg,command_start_position,original_log,seg_searched)
                            #如果没有选择进行段落搜寻，则输出命令所有内容，如果选择进行段落搜寻，就不再输出该命令所有内容
                        if (len(seg_searched)==0):    #如果这是个空列表，表示没有进行过段落查找
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
                flag_continue=raw_input('Continue other command?(Y/N)')   #此处flag_found一定等于1，因为一定有命令可以被找到
                if flag_continue=='N' or flag_continue=='n':
                    break
                else:
                    original_log.seek(0)
                    continue
#command_list 是每个类的静态字段，可通过类名直接调用，也可通过对象调用 
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
                            #查找命令输出中的特定段落
                            while True:
                                search_sub_seg=raw_input('\nDo you want to search sub segment in the output?(y/n)')
                                if(search_sub_seg=='y' or search_sub_seg=='Y'):
                                    if len(seg_searched)==0:
                                        seg_searched.append(1)    #使这个列表不为空
                                    segment_keyword=raw_input('Keyword: ')
                                    original_log.seek(command_start_position)
                                    seg_found=0
                                    
                                    while seg_found==0:
                                        seg_content=original_log.readline()
                                        if seg_content.strip()[-8:]=='       :':
                                            break
                                        if not (seg_content=='\n' or seg_content=='\r\n'):#如果不是空行，则判断关键字在不在该行
                                            if segment_keyword in seg_content:  #如果关键词出现第一个非空行，则开始读下面的行
                                                seg_found=1
                                                print seg_content.strip()
                                                #loop
                                                end_of_seg=0
                                                while end_of_seg==0:
                                                    seg_content=original_log.readline()
                                                    if not (seg_content=='\n' or seg_content=='\r\n'):#如果读到的不是空行,则打印出来，并继续往下读
                                                        print seg_content.strip()
                                                        continue
                                                    else:       #如果读到了空行，就不再继续读
                                                        end_of_seg=1
                                                        break
                                                continue    
                                                #loop
                                            else:#如果关键字不出现在第一个非空行,则一直读，直到读到下一个空行
                                                #LOOP
                                                while True:
                                                    seg_content=original_log.readline()
                                                    if (seg_content=='\n' or seg_content=='\r\n'):
                                                        break
                                                    else:
                                                        continue
                                                #LOOP 
                                                continue #读到下一个空行后，继续
                                                   
                                        else:  #如果是空行，继续判断下一行
                                            continue                        
                                else:#如果输入不是yes，就不进行段落搜寻
                                    break
        return  seg_searched
    def filter_by_command(self):
        with open(self.path,'rb') as original_log:
            #loop
            while True:
                flag_found=0
                command_to_search=self.command_finder()   #获取合法的命令，一定可以获取到
                
                #LOOP
                while True:
                    line=original_log.readline()
                    
                    if re.match(r'%s(\s{6,9}):'%command_to_search,line):
                        flag_found=1
                        command_start_position=original_log.tell()
                        #search_sub_seg='Y'
                        #seg_searched=list()
                        #seg_searched=self.search_segment(search_sub_seg,command_start_position,original_log,seg_searched)
                            #如果没有选择进行段落搜寻，则输出命令所有内容，如果选择进行段落搜寻，就不再输出该命令所有内容
                        #if (len(seg_searched)==0):    #如果这是个空列表，表示没有进行过段落查找
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
                flag_continue=raw_input('Continue other command?(Y/N)')   #此处flag_found一定等于1，因为一定有命令可以被找到
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
        
        if (os.path.exists(self.command_dict_path) and os.path.exists(self.command_list_path)):#如果已经有command_list文件则不再次生成
            command_dict=json.load(open(self.command_dict_path,'rb'))
            command_list=json.load(open(self.command_list_path,'rb'))
            return command_dict,command_list
        
        else:   #如果还没有command_list就生成一个command_list文件(将command_dict序列化，包含命令及其输出内容)
            #loop 寻找commands文件夹
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
            #loop找到后
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
                    else:   #如果是有用的命令：
                        command_output_file=os.path.join(rootdir,f)    #具体的命令输出文件路径
                        command_str=f.strip('.txt')                     #命令字符串
                        command_list.append(command_str)                       #将命令字符串存入命令列表中
                        with open(command_output_file,'rb') as f1:      #打开命令输出文件，并读取内容，存到command_dict相应的键值中
                            command_dict[command_str]=f1.read()
                    #end loop 读完commands文件夹下所有文件
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
                          
                       