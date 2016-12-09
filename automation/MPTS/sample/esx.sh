echo ""
echo "EC101 Reverting of Snapshot Begins"
vim-cmd vmsvc/snapshot.revert 48 2 supressPowerOff
vim-cmd vmsvc/power.on 48
echo "EC101 Reverting of Snapshot Done"
echo ""
sleep 5
echo "Ctl103 Reverting of Snapshot Begins"
vim-cmd vmsvc/snapshot.revert 45 3 supressPowerOff
vim-cmd vmsvc/power.on 45
echo "Ctl103 Reverting of Snapshot Done"
echo ""
