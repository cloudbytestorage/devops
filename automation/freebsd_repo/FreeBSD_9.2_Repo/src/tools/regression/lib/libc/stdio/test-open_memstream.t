#!/bin/sh
# $FreeBSD: releng/9.2/tools/regression/lib/libc/stdio/test-open_memstream.t 252343 2013-06-28 16:07:20Z jhb $

cd `dirname $0`

executable=`basename $0 .t`

make $executable 2>&1 > /dev/null

exec ./$executable
