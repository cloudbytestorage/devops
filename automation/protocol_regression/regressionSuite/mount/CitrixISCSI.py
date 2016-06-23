xe sr-create host-uuid=<valid_UUID> content-type=user \
name-label="Example shared LVM over iSCSI SR" shared=true \
device-config:target=<valid_target_IP> device-config:targetIQN=<valid_target_IQN> \
device-config:SCSIid=<valid_SCSIID> \
type=lvmoiscsi
