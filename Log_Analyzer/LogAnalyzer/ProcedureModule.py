#_*_coding:utf-8_*_

from ClassLog import esxi_host_filter,n5k_showtech_filter,vmkernel_filter,sw_techsupportinfo_filter,sam_techsupportinfo_filter,log_filter,mds_showtech_filter

def esxi_command_analysis(sr_number):
        print('Welcome to ESXi command line Mode, Please enter the command!')
        esxi=esxi_host_filter(sr_number)
        esxi.filter_by_command()
        
def vmkernel_analysis(sr_number,log_name):
        print('this is a vmkernel log')
        print sr_number,log_name
        vmklog=vmkernel_filter('%s'%sr_number,'%s'%log_name)
        
        while True:
            print '''
    -------------------------------------------------------------------------
    How would you process?
    1. Filter by time period.
    2. Filter by Key word.
    -------------------------------------------------------------------------    
        '''
            choice=raw_input('Choose:')
            if choice=='1':
                vmklog.filter_by_time()
                go_on=raw_input('Do you want to continue?(Y/N)')
                if(go_on=='N' or go_on=='n'):
                    break
                else:
                    continue
            elif choice=='2':
                vmklog.filter_by_message()
                go_on=raw_input('Do you want to continue?(Y/N)')
                if(go_on=='N' or go_on=='n'):
                    break
                else:
                    continue
            else:
                print('Invalid choice,try again!')
                continue
def sw_techsupportinfo_analysis(sr_number,log_name):
        print('this is a sw_techsupportinfo')
        print sr_number,log_name
        fi_sw_log=sw_techsupportinfo_filter(sr_number,log_name)
        fi_sw_log.filter_by_command()    
        
def sam_techsupportinfo_analysis(sr_number,log_name):
        print('this is a sam_techsupportinfo')
        print sr_number,log_name
        fi_sam_log=sam_techsupportinfo_filter(sr_number,log_name)
        fi_sam_log.filter_by_command()

def mds_showtech_analysis(sr_number,log_name):
        print('this is a MDS show tech log')
        print sr_number,log_name
        mds_showtech_log=mds_showtech_filter(sr_number,log_name)
        mds_showtech_log.filter_by_command()
def n5k_showtech_analysis(sr_number,log_name):
        print('this is a N5K show tech log')
        print sr_number,log_name
        n5k_showtech_log=n5k_showtech_filter(sr_number,log_name)
        n5k_showtech_log.filter_by_command()
        
def other_analysis(sr_number,log_name):
    print sr_number,log_name
    other_log=log_filter(sr_number,log_name)
    other_log.filter_by_message()
    
def log_name_analysis(sr_number):   #����������ļ�����ѡ�����
        while True:
                log_name=raw_input('Please specify Log File Name:')  #���û������ļ�����
                if('vmkernel' in log_name):                         #�����к���vmkernel���ж�Ϊһ��vmkernel��־�ļ�
                    vmkernel_analysis(sr_number, log_name)          #ִ��vmkernel�ļ���������
                    break                                           #ִ�к��˳�
                elif('sw_techsupportinfo' in log_name):
                    sw_techsupportinfo_analysis(sr_number,log_name)
                    break
                elif('sam_techsupportinfo' in log_name):
                    sam_techsupportinfo_analysis(sr_number,log_name)
                    break
                else:
                    other_analysis(sr_number,log_name)
                    break
        