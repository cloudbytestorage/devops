import os.path
import sys
import yaml
import yamlordereddictloader
import string
import pexpect

from distutils.dir_util import copy_tree

#!/usr/bin/env python
_author_ = 'naveenkumar b'
_email_ = 'naveen.b@emc.com'

class FileUtilities:

    @staticmethod
    def copyfile(src, dest):
        filename1 = src
        open(filename1, "w").close()
        filename2 = filename1 + ".copy"
        print
        filename1, "=>", filename2
        os.system("copy %s %s" % (filename1, filename2))
        if os.path.isfile(filename2): print
        "Success"
        dirname1 = src.mktemp(".dir")
        os.mkdir(dirname1)
        dirname2 = dirname1 + ".copy"
        print
        dirname1, "=>", dirname2
        os.system("xcopy /s %s %s" % (dirname1, dirname2))
        if os.path.isdir(dirname2): print
        "Success"

    @staticmethod
    def verifyIfFolderExists(absoluteDirPath):
        return os.path.exists(os.path.dirname(absoluteDirPath))

    @staticmethod
    def copy_tree(src, dest):
        copy_tree(src, dest)

    @staticmethod
    def verifyIfFileExists(absoluteFilePath):
        return os.path.exists(absoluteFilePath)

    @staticmethod
    def mkdir(dir):
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("\nDir %s created" %dir)
        else:
            print("\nBE CAREFUL! Directory %s already exists." % dir)

    @staticmethod
    def createFile(absFilePath):
        open(absFilePath, 'w')
        print("%s File created" % absFilePath)

    @staticmethod
    def delFile(absFilePath):
        if os.path.exists(absFilePath):
            os.remove(absFilePath)
            print("%s file deleted" % absFilePath)
        else:
            print("Sorry, I can not remove %s file." % absFilePath)


    @staticmethod
    def delFolder(absFolderPath):
        if os.path.exists(absFolderPath):
            os.removedirs(absFolderPath)
            print ("Dir %s deleted" % absFolderPath)
        else:
            print("Dir %s not found" % absFolderPath)

    @staticmethod
    def renameFileorFolder(absPath, newAbsPath):
        os.rename(absPath, newAbsPath)
        print("File %s renamed to new path" % absPath)

    '''def testToExecuteList(testsetloc, testtypes):
        result = {}
        try:
            ts_dict = yaml.load(open(testsetloc), Loader=yamlordereddictloader.Loader)
            for testtype in testtypes:
                tests2execute = []
                testscommeted = []
                for key in ts_dict[testtype].keys():
                    if ts_dict[testtype][key]:
                        tests2execute.append(key)
                    else:
                        testscommeted.append(key)
                result[testtype]['yes_list'] = tests2execute
                result[testtype]['no_list'] = testscommeted
                result[testtype]['yes_count'] = len(tests2execute)
                result[testtype]['no_count'] = len(testscommeted)
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            return result
    '''

    def testToExecuteList(testsetloc, testtype):
        result = {}
        try:
            ts_dict = yaml.load(open(testsetloc), Loader=yamlordereddictloader.Loader)

            tests2execute = []
            testscommented = []

            for key in ts_dict[testtype].keys():
                if ts_dict[testtype][key]:
                    tests2execute.append(key)
                else:
                    testscommented.append(key)

                result['yes_list'] = tests2execute
                result['no_list'] = testscommented
                result['yes_count'] = len(tests2execute)
                result['no_count'] = len(testscommented)
        except IOError, (errno, strerror):
            print "I/O error(%s): %s" % (errno, strerror)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
        else:
            return result

    @staticmethod
    def scp_From(host_IP, host_User, host_Password, local_location, remote_Path):
        command = 'scp -o \"StrictHostKeyChecking no\" '+host_User+'@'+host_IP+':'+remote_Path+' '+local_location
        cp = pexpect.spawn(command)

        cp.expect('.*:')
        cp.sendline(host_Password)
        cp.expect('.*100%')
        print(cp.after)


    '''    @staticmethod
        def getpath(pathof):
            path = os.getcwd() # this gives utils path
            fcmpath = os.path.normpath(os.path.join(path, '..')) # this gives fcm path
            nhcpath = os.path.normpath(os.path.join(fcmpath, '..')) #this gives nhc path

            if pathof.lower == "fcm":
                return fcmpath
            elif path.lower == "scm":
                return nhcpath+"\\SCM"
            elif path.lower == "nhc":
                return nhcpath
    '''