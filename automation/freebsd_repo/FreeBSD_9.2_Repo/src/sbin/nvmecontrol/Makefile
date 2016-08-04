# $FreeBSD: releng/9.2/sbin/nvmecontrol/Makefile 253631 2013-07-24 22:48:29Z jimharris $

PROG=	nvmecontrol
SRCS=	nvmecontrol.c devlist.c firmware.c identify.c logpage.c	\
	perftest.c reset.c nvme_util.c
MAN=	nvmecontrol.8

.PATH:	${.CURDIR}/../../sys/dev/nvme

.include <bsd.prog.mk>
