import os

class Constants:

    testsetloc  = os.getcwd()+os.path.sep+"TestSet.yml"
    dict={ }
    dict['sol_name'] = "NHC1.0_Automation"
    dict['testEnv'] = 'icoeqa'
    dict['testsetloc'] = testsetloc
    # dict['testtypes'] = ['Regression', 'backup']
    dict['testtype'] = 'Regression'

    #Pcf
    dict['pcfappdomain'] = 'pcf_app_domain: app.cfsmokeicoeqa.ppblue.lab.local'
    dict['pcfextlb'] = "pcf_ext_lb: 'no'"
    dict['pcfsysdomain'] = 'pcf_sys_domain: sys.cfsmokeicoeqa.ppblue.lab.local'
    dict['configFilePath'] = '/etc/nhc/config.yml'
    dict['ansiblebravoFilePath'] = '/opt/emc/nhc/logs/ansible_bravo.log'
    dict['pcfKeypairCreationTask'] = 'Create PCF Key pair'
    dict['ansiblebravoFailureValidation'] = 'failed=0'
    dict['mnrInstallerFilePath'] = '/opt/emc/nhc/logs/mnr_installer.log'
    dict['mnrInstallationValidation'] = 'Installation complete'
    dict['mnrConfiguration'] = 'mnr-configuration-end'
    dict['custommodulesFilePath'] = '/opt/emc/nhc/logs/custom_modules.log'
    dict['jmxConfiguration'] = 'jmx_configuration : INFO : Updated jmx-collector successfully'
    dict['custommodulesSuccessMsg'] = 'NHC : post_check : DEBUG : main:output Success'

    #List of files to check
    dict['precheck_AbsPath'] = '/opt/emc/nhc/pre_check.sh'
    dict['postinstall_AbsPath'] = '/opt/emc/nhc/post_install.sh'
    dict['mnrsh_abspath']='/opt/emc/nhc/mnr_run.sh'
    dict['kibanaTar_abspath']='/opt/emc/nhc/nhc-files/bin/kibana-4.1.1-linux-x64.tar.gz'
    dict['elasticSearchRpm_abspath']='/opt/emc/nhc/nhc-files/bin/elasticsearch-1.7.1.noarch.rpm'
    dict['logstashRPM_abspath']='/opt/emc/nhc/nhc-files/bin/logstash-1.5.3-1.noarch.rpm'
    dict['logstasthForwarder_abspath']='/opt/emc/nhc/nhc-files/bin/logstash-forwarder-0.4.0-1.x86_64.rpm'
    dict['viprSRM_abspath']='/opt/emc/nhc/nhc-files/bin/vipr*.rpm'
    dict['pcfPrivateKey_abspath']='/opt/emc/nhc/certs/PCF/pcf-private-key.pem'
    dict['neutrinokeyCert_abspath']='/opt/emc/nhc/certs/neutrino.pem'
    dict['kibanaURL'] = 'http://192.168.235.116:5601'
    dict['ss1_ip'] = '10.0.4.239'
    dict['ss2_ip'] = '10.0.4.240'
    dict['ss3_ip'] = '10.0.4.241'
    dict['sp1_ip'] = '10.0.4.237'
    dict['sp2_ip'] = '10.0.4.238'
    dict['mnr_ip'] = '192.168.235.116'
    dict['cacertpem_abspath'] = '/var/lib/ca-certificates/openssl/neutrino.smoke.local.pem'
    dict['cacertpem_abspath'] = '/var/lib/ca-certificates/openssl/192.168.235.4.pem'
    dict['cacertpem_abspath_name'] = '/var/lib/ca-certificates/openssl/neutrino.smoke.local.pem'
    scmpath = os.getcwd()  # this gives SCM path
    nhcpath = os.path.normpath(os.path.join(scmpath, '..'))  # this gives NHC path
    # fcmpath = nhcpath + "\\FCM"  # this gives FCM path
    fcmpath = nhcpath + os.path.sep+"FCM"  # this gives FCM path
    init_file = '/root/nhc_automation/SCM/init_config.yml'
    dict['mnr_User'] = 'root'
    dict['mnr_Password'] = 'password'
    nhc_outputfile = '/opt/emc/nhc/nhc-output.yml'
    nhc_fixedip = '/opt/emc/nhc/config/nhc-fixed-ip.yml'
    nhc_mnrdetails = '/opt/emc/nhc/config/nhc-mnr-vm-details.yml'
    dict['nhcpcf_config'] = '/opt/emc/nhc/config/nhcpcf-config.yml'
    # NHCQA-424
    nhc_backup_log = '/opt/emc/nhc/logs/nhc-backup.log'
    nhc_backup_success_msg = 'NHC : vm_backup : INFO : VM-backup VM snapshot Succeed'
    nhc_init_state = '/opt/emc/nhc/nhc-install.state'
    dict['mnr_User'] = 'root'
    dict['mnr_Password'] = 'password'
    nhc_outputfile = '/opt/emc/nhc/nhc-output.yml'
    nhc_state_file = '/opt/emc/nhc/nhc-install.state'

