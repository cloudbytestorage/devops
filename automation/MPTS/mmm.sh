python ISCSIVolume.py expandVol.txt

## enabling the initiators
python setISCSIInitiatorGroup.py expandVol.txt

## execution.py file
python execution.py expandVol.txt all

## expand volume
python expandVol.py expandVol.txt iscsi 1

## execute after expand
python executeExpand.py expandVol.txt iscsi
