import subprocess
import yaml
import FCM.utils.ResultUtils as rutils
import re
import os
import time
import pexpect
import datetime
from FCM.utils.FileUtils import FileUtilities as fUtil
from FCM.utils.ResultUtils import ResultUtilities as rUtils
from SCM_Charlie.constants import Constants as const

# !/usr/bin/env python
_author_ = 'naveenkumar b'
_email_ = 'naveen.b@emc.com'


class Common:
    @staticmethod
    def execute(cmd):
        """
            Purpose  : To execute a command and return exit status
            Argument : cmd - command to execute
            Return   : exit_code
        """
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (result, error) = process.communicate()
        rc = process.wait()
        if rc != 0:
            print "Error: failed to execute command:", cmd
            return error
        return result

    @staticmethod
    def run_shell(cmd):
        # p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # return iter(p.stdout.readline, b'')
        """given shell command, returns communication tuple of stdout and stderr"""
        # instantiate a startupinfo obj:
        startupinfo = subprocess.STARTUPINFO()
        # set the use show window flag, might make conditional on being in Windows:
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        # pass as the startupinfo keyword argument:
        return subprocess.Popen(cmd,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE,
                                startupinfo=startupinfo).communicate()

    @staticmethod
    def replace_value_in_yaml(mylist, filename, **attribute):
        """
        This function takes key value pairs as input to replace any values in the yml file.
        :param mylist: For logging and reporting
        :param filename: path of yml file
        :param attribute: yml file values needed to be replaced e.g. IP = 10.125.8.130
        :return: mylist
        The call can be like replace_value_in_yaml(mylist, '/opt/emc/nhc/playbooks/config/result.yml', Z = 111122)
        """
        fh = open(filename,'rb+')
        new = []
        config_load = yaml.load(fh)
        for val in config_load.keys():
            new.append(val)
            input = config_load[val]
            for k in attribute.keys():
                if str(val) == str(k):
                    config_load[val] = attribute[k]

            def iteration(attribute, input):
                if isinstance(input, dict):
                    for k in attribute.keys():
                        for key in input.keys():
                            new.append(key)
                            if str(key) == str(k):
                                input[key] = attribute[k]
                            iteration(attribute, input[key])
            iteration(attribute, input)
        fh.close()
        for k in attribute.keys():
            if k not in new:
                rutils.logger(mylist,"The Attribute "+k+" not present in this yml file", "","","exception")

        with open(filename, 'w') as yaml_file:
            yaml_file.write(yaml.dump(config_load, default_flow_style=False))
        yaml_file.close()
        return mylist

    @staticmethod
    def verify_Service_Stat(service_name):
        # This method is design to verify the status of a given service
        # The method will return True or False along with status of that service
        """e.g
               if the service running and active
                  stat='True_Active'
                  return stat"""
        cmd = 'service --status-all | grep -i ' + service_name
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = process.communicate()[0]
        # print (out)
        regex = re.compile(r"service\s+\w+\s(\w+)\s(\w+)\s")
        match = regex.findall(out)
        # print match
        if (match[0][0] == 'active'):
            stat = match[0][0] + '&' + match[0][1]

        else:
            stat = match[0][0] + '_' + match[0][1]

        # print stat
        return stat

    @staticmethod
    def verify_Logs(path,string):
        #This method is designed to verify the log files
        cmd = 'grep '+"'"+string+"'"+' '+"'"+path+"'"+' '+'|'+' '+'tail -1'
        process = subprocess.Popen(cmd, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)

        out = process.communicate()[0]
        print out
        if not out.strip():
            stat = 'FAIL'
        else:
            stat = 'PASS'


        print stat
        return stat

    @staticmethod
    def search_Logs(path, string):
        # This method is designed to search for a string in the log files
        # This method will return True if string is found in the log
        # or false if string not found in the log
        cmd = 'grep ' + "'" + string + "'" + ' ' + "'" + path + "'" + ' ' + '|' + ' ' + 'tail -1'
        print cmd
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        out = process.communicate()[0]
        print out
        if not out.strip():
            stat = 'FAIL'
        else:
            stat = 'PASS' + ',' + out
        print stat
        return stat

    @staticmethod
    def check_Ping(ip):
        ps = subprocess.Popen(['ping', ip, '-c', '1'], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)
        out = ps.communicate()[0]
        regex = re.compile('ttl' + r'=(\d+)')
        match = regex.findall(out)
        try:
            if (match[0] != 0):
                return True
        except IndexError as e:
            return False

    @staticmethod
    def is_init_successfully_done():
        print 'DEBUG: inside is_init_successfully_done'
        cfg_file_path = const.nhc_config
        nhc_init_log = const.dict['nhcinitLogPath']
        nhc_init_succ_msg = const.nhc_init_success_msg
        print "config file %s : nhc init log %s : succ msg %s" %(cfg_file_path, nhc_init_log, nhc_init_succ_msg)
        if (fUtil.verifyIfFileExists(cfg_file_path)):
            print "Config file cfg_file_path exists. Init may have done successfully"
            print "Checking init.log to verify"
            stringm = subprocess.Popen(['grep', nhc_init_succ_msg, nhc_init_log], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stringo, _ = stringm.communicate()
            print "grep output %s" %(stringo)
            if not stringo.strip():
                print "Init log verification failed. We may have to rerun the init task"
                ret_val = 0
            else:
                print "Init log verified successfully"
                ret_val = 1
        else:
            print "Config file cfg_file_path does not exists"
            print "pre_Requisite was not successfully done"
            ret_val = 0
        return ret_val

    @staticmethod
    def read_value_in_yaml(filename, yparameter):
        '''
        This function read the values of the parameter
        :param filename: path of yaml file
        :param yparameter: parameter or keys in yaml
        :return: value(s) of the parameter
        '''
        try:
            fh = open(filename, 'r')
        except IOError as es:
            print "Exception while reading yaml file"
            print format(es)
            return False
        else:
            yaml_out = yaml.load(fh)
            val = yaml_out[yparameter]
            print val
        finally:
            fh.close()
        return val

    @staticmethod
    def run_schedule_backup(mylist, script, time_min=2):
        '''
        This method will run the schedule backup script to run backup after 2 minutes
        :param script: The script used for backup schedule, eg: schedule-mnr-bkup
        :time_min: time in minutes, telling schedule x minutes after
        :return: True if pass
        '''
        # Get current time (hours and minutes) and future time for 2 minutes later
        now = datetime.datetime.now()
        now_plus_2m = now + datetime.timedelta(minutes=int(time_min))
        print "%s - %s" % (now, now_plus_2m)
        future_date, future_time = str(now_plus_2m).split()
        print "%s - %s" % (future_date, future_time)
        future_hrs, future_mins, _ = str(future_time).split(':')
        print "%s - %s" % (future_hrs, future_mins)
        schedule_command = script + ' --interval "' + future_mins + ' ' + future_hrs + ' * * *"'
        print "command %s" % schedule_command
        out = os.system(schedule_command)
        if not out:
            rUtils.logger(mylist, "Running schedule mnr backup script", "success", "success", "pass")
        else:
            rUtils.logger(mylist, "Running schedule mnr backup script", "success", out, "fail")
            print "output from schedule backup %s" % (out)
            return None
        # Run crontab -l to verify the crontab
        run_script = subprocess.Popen(['crontab', '-l'], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = run_script.communicate()[0]
        print "output from crontab -l %s" % (out)
        if out:
            rUtils.logger(mylist, "crontab -l output after schedule script run", "-", out, "info")
        return True

    @staticmethod
    def check_backup_log(mylist, logpath, logmessage):
        '''
        This method will check for a message in a log file
        :param mylist: this is the result utils list
        :param logpath: path to the log file
        :param logmessage: message to be find in the log file
        :return: True
        '''
        today = datetime.date.today()
        run_script = subprocess.Popen(['grep', str(today), logpath], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = run_script.communicate()[0]
        print "output from log grep %s" % (out)
        pattern = re.compile(logmessage)
        found = 0
        if out:
            out_lines = out.splitlines()
            olength = len(out_lines)
            while olength > 0:
                line = out_lines[olength - 1]
                olength -= 1
                if pattern.search(line):
                    found = 1
                    break
        if found == 1:
            print "found message in log"
            out = line
        else:
            print "did not find message in log"
            return (False, out)
        return (True, out)

    @staticmethod
    def restore_backup_crontab(mylist, script, schedule):
        '''
        This method will run the schedule backup script to restore schedule as per config
        :param script: The script used for backup schedule, eg: schedule-mnr-bkup
        :return: True if pass
        '''
        # --interval "0 */12 * * *"
        if int(schedule) == 24:
            schedule_str = r'59 23'
        else:
            schedule_str = r'0 */' + schedule
        schedule_command = script + ' --interval "' + schedule_str + ' * * *"'
        print "command %s" % schedule_command
        out = os.system(schedule_command)
        if not out:
            rUtils.logger(mylist, "Running schedule mnr backup script", "success", "success", "pass")
        else:
            rUtils.logger(mylist, "Running schedule mnr backup script", "success", out, "fail")
            print "output from schedule backup %s" % (out)
            return None
        # Run crontab -l to verify the crontab
        run_script = subprocess.Popen(['crontab', '-l'], stdin=subprocess.PIPE,
                                      stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out = run_script.communicate()[0]
        print "output from crontab -l %s" % (out)
        if out:
            rUtils.logger(mylist, "crontab -l output after schedule script run", "-", out, "info")
        return True

    @staticmethod
    def get_vmname_from_config(config_file, keystring):
        '''
        This method will give you vm name from config file
        :param config_file: config file where vm name exists
        :param keystring: key string for the vm name
        :return: vm name
        '''
        vm_name = ''
        # config should exists
        if os.path.exists(config_file):
            grep_out = subprocess.Popen(['grep', keystring, '\:', config_file], shell=False,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            actual_output, _ = grep_out.communicate()
            regex_pattern = '\\s' + keystring + ':' + '\s+(.*)\s+'
            pattern01 = re.compile(regex_pattern)
            if (pattern01.search(actual_output)):
                match01 = pattern01.search(actual_output)
                vm_name = match01.groups()[0]
                print "got vm name from config file: %s" % vm_name
            else:
                print "failed to get detail from config file"
        return vm_name