#_*_coding:utf-8_*_
import os.path
import platform
def set_pre_path():
        windows_pre_path=raw_input("Tell me the log folder path(e.g. X:\logs\ ):")
        #判断用户的输入最后有没有\符号
        if windows_pre_path[len(windows_pre_path)-1]=='\\':pass
        else:
            windows_pre_path+='\\'
        tmp=windows_pre_path.split('\\')
        pre_path='\\\\'.join(tmp)
        with open(r'C:\easylog\path.txt','wb') as f:
            f.write(pre_path)
        print("Current Log Folder is '%s'"%windows_pre_path)
        
        return pre_path
    
def init_tool():
        if os.path.exists(r'C:\easylog\path.txt'):
            with open(r'C:\easylog\path.txt','rb') as f:
                pre_path=f.readline()
                print("Current Log Folder is '%s'"%('\\'.join(pre_path.split('\\\\'))))
            choice=raw_input("do you want to change the log folder path?(y/n)")
            if choice=='y':
                return set_pre_path()
            else:
                print("Current Log Folder is '%s'"%('\\'.join(pre_path.split('\\\\'))))
                return pre_path
                
        else:
            pre_path=set_pre_path()
            return pre_path

sysstr=platform.system()
if sysstr=='Windows': 
    PathPrefix=init_tool()
       
elif sysstr=='Linux':
    PathPrefix='/home/logs/'
