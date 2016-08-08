> response
> temp2
echo "n" >> response
echo "n" >> response
for((i=150;i<=160;i++))
do
    cp response_temp temp2
    sed -i s/x/$i/ temp2
    cat temp2 >> response
done
rm temp2
echo -en File Named"\033[32m response \033[0m"has been created
echo ""
echo "Use the same with Configuration_Create.sh to create teh config file --  For Eg As below"
echo -en  "\033[32msh ConfigurationCreation.sh < response \033[0m"
echo ""
echo "n" >> response
