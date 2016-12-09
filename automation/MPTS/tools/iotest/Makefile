# $FreeBSD$

BINDIR= /usr/sbin/

PROG=  iotest

NO_MAN= true

WARNS?=	3

DPADD=	${LIBODIALOG} ${LIBNCURSES}
LDADD=	-lpthread -lrt 

.include <bsd.prog.mk>
