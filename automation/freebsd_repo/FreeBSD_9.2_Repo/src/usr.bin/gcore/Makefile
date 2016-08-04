#	@(#)Makefile	8.1 (Berkeley) 6/6/93
# $FreeBSD: releng/9.2/usr.bin/gcore/Makefile 250872 2013-05-21 19:06:17Z trociny $

PROG=	gcore
SRCS=	elfcore.c gcore.c
DPADD=	${LIBSBUF} ${LIBUTIL}
LDADD=	-lsbuf -lutil

WARNS?=	1

.include <bsd.prog.mk>
