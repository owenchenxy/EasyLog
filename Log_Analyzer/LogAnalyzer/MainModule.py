#_*_coding:utf-8_*_
from ProcedureModule import esxi_command_analysis,n5k_showtech_analysis,mds_showtech_analysis,vmkernel_analysis,sw_techsupportinfo_analysis,sam_techsupportinfo_analysis,log_name_analysis
import sys,os
from LogPathVar import PathPrefix

def main():
    print '''
    -------------------------------------------------------------------------
    Welcome to EasyLog version 1.1  
    Coder: owen.chen@vce.com
    -------------------------------------------------------------------------
    '''
    while True: 
        sr_number=raw_input('SR NUMBER:')
        if(os.path.exists(PathPrefix+sr_number)):
            break
        else:
            print('No SR record %s'%sr_number)
            continue
    # log_name=raw_input('LOG FILE NAME:')
    
    while True:
        print '''
    -------------------------------------------------------------------------
    Please Choose the Log Type or Tell the Log File name:
    1. VMware Log
    2. UCSM Hardware Inventory Log(sam_techsupportinfo)
    3. UCSM Fabric Interconnecter show tech Log(sw_techsupportinfo)
    4. MDS show tech log(mds_showtech)
    5. N5K show tech log(n5k_showtech)
    6. Manually specify the LOG NAME
    -------------------------------------------------------------------------
    

    '''
        choice_log_type=raw_input('Choose:')
        if(choice_log_type=='1'):
            while True:
                print '''
    -------------------------------------------------------------------------
    1. vmkernel log
    2. ESXi command mode
    -------------------------------------------------------------------------
                '''
                vmware_choice=raw_input('Choose:')
                if(vmware_choice=='1'):
                    is_vmkernel0=raw_input("Default is 'vmkernel.log'. If not,enter 'N'")
                    if is_vmkernel0=='N' or is_vmkernel0=='n':
                        log_name=raw_input('Log name should be:')    
                    else:
                        log_name='vmkernel.log'
                    vmkernel_analysis(sr_number, log_name)
                    break
                elif(vmware_choice=='2'):
                    esxi_command_analysis(sr_number)
                    break
                else:
                    print('invalid choice. Try again!')
        elif(choice_log_type=='2'):
            log_name='sam_techsupportinfo'
            sam_techsupportinfo_analysis(sr_number,log_name)
            break
        elif(choice_log_type=='3'):
            log_name='sw_techsupportinfo'
            sw_techsupportinfo_analysis(sr_number,log_name)
            break
        
        elif(choice_log_type=='4'):
            log_name='mds_showtech'
            mds_showtech_analysis(sr_number,log_name)
        elif(choice_log_type=='5'):
            log_name='n5k_showtech'
            n5k_showtech_analysis(sr_number,log_name)
        elif(choice_log_type=='6'):
            log_name_analysis(sr_number)
            break
        else:
            print('invalid choice. Try again!')
            continue
    
    
  
    raw_input('press any key to exit')
    sys.exit('Thanks for using')
    
main()

