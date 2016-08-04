#!/bin/sh
#
# $FreeBSD: releng/9.2/usr.bin/less/zless.sh 244342 2012-12-17 06:35:15Z delphij $
#

export LESSOPEN="||/usr/bin/lesspipe.sh %s"
exec /usr/bin/less "$@"
