#!/bin/bash

REPOS="$1"
TXN="$2"

SVNLOOK=/usr/bin/svnlook

LOG_MSG_LINE1=`${SVNLOOK} log -t "${TXN}" "${REPOS}" | head -n1`
echo $LOG_MSG_LINE1 >> $1/hooks/svn_commit.log

if (echo "${LOG_MSG_LINE1}" | egrep '^\[BUG-[0-9]*]\[RB-[0-9]*\].*$' > /dev/null;)
then
exit 0
exit 1
else
echo ""
echo "Your log message does not contain a Bug ID or a Review board ID (or bad format used)"
echo ""
echo "Proper format:  [BUG-XXXX][RB-XXXX] Commit message"
echo "Regex: '^\[BUG-[0-9]*]\[RB-[0-9]*\].*$'"
exit 1
fi

