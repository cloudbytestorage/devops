> mail.txt
echo " ">> mail.txt

grep -i "fail\|pass" results/result.csv
if [ $? -eq 0 ]
then
    failed=`grep  "FAILED" results/result.csv | wc -l`
    passed=`grep -i "PASS" results/result.csv | wc -l`
    blocked=`grep -i "BLOCKED" results/result.csv | wc -l`
    total=`expr $failed + $passed + $blocked`
    status=PASSED
    echo "Summary of Automation Result"  >> mail.txt
    echo "Total number of Automated testcases are -- $total"  >> mail.txt
    echo "Total number of BLOCKED testcases are    -- $blocked" >> mail.txt
    echo "Total number of FAILED testcases are    -- $failed" >> mail.txt
    echo "Total number of PASSED testcases are    -- $passed" >> mail.txt
    echo "" >> mail.txt
    cat mail.txt.base >> mail.txt
    if [ $failed -ne 0 ]
    then
        echo "List of Failed TestCases are as below " >> mail.txt 
        grep  "FAILED" results/result.csv >> mail.txt
        status=FAILED
    fi
    #mail -s "Automation Report -- `sed -n 1p installed_version`" -a results/result.csv -r cbauto@cloudbyte.com cb-qa@cloudbyte.com < mail.txt
    #mail -s "Automation Report -- `sed -n 1p installed_version`" -a results/result.csv -r cbauto@cloudbyte.com ajesh.baby@cloudbyte.com < mail.txt
    #mail -s "Automation Report -- `sed -n 1p installed_version`" -a results/result.csv -r cbauto@cloudbyte.com ajesh.baby@cloudbyte.com -c hemanth@cloudbyte.co,rammohan.r@cloudbyte.com,anoop@cloudbyte.com,kiran.mova@cloudbyte.com,ajith.kumar@cloudbyte.com,umasankar.mukkara@cloudbyte.com,rameshbabu.kl@cloudbyte.com, vishnu.attur@cloudbyte.com,spurti@cloudbyteinc.com,shamrao@cloudbyteinc.com,giridhara.prasad@cloudbyte.com,karthik.s@cloudbyte.com,pavitra@cloudbyte.co,manohar.m@cloudbyte.com,yogesh.prasad@cloudbyte.com,apeksha.khakharia@cloudbyte.com,mardan.singh@cloudbyte.com,basavaraj.karande@cloudbyte.com,srinivasad@cloudbyte.co,snharinder@cloudbyte.com, < mail.txt
    #mail -s "Automation Report -- `sed -n 1p installed_version` -- $status" -a results/result.csv -r cbauto@cloudbyte.com cb-qa@cloudbyte.com -c ajith.kumar@cloudbyte.com,vishnu.attur@cloudbyte.com,giridhara.prasad@cloudbyte.com < mail.txt
    #mail -s "Automation Report -- `sed -n 1p installed_version` -- $status" -a results/result.csv -r cbauto@cloudbyte.com  -c senthilkumar.e@cloudbyte.com, cb-devman@cloudbyte.com, cb-qa@cloudbyte.com < mail.txt
    mail -s "Automation Report -- `sed -n 1p installed_version` -- $status" -a results/result.csv -r cbauto@cloudbyte.com -c mardan.singh@cloudbyte.com < mail.txt
    #mail -s "Automation Report -- `sed -n 1p installed_version` -- $status" -a results/result.csv -r cbauto@cloudbyte.com -c ajesh.baby@cloudbyte.com, mardan.singh@cloudbyte.com, senthilkumar.e@cloudbyte.com, manohar.m@cloudbyte.com, kaushik@cloudbyte.com < mail.txt
else
    #echo "No result file to attach, Hence mail not send to any one only sent to Automation Team" >> mail.txt
    #sed -i '1iNo result file to attach, Hence this mail is sent to Automation Team only.. Review it why it did not send' mail.txt
    echo "No result file to attach, Hence this mail is sent to Automation Team only.. Review it why it did not send" >> mail.txt
    cat mail.txt.base >> mail.txt
    mail -s "Automation Report -- `sed -n 1p installed_version` -- $status" -a results/result.csv -r cbauto@cloudbyte.com -c mardan.singh@cloudbyte.com  < mail.txt
fi
