# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/ttys/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

SUBDIR= include

FILESDIR=	${LIBEXECDIR}/bsdconfig/150.ttys
FILES=		INDEX USAGE

SCRIPTSDIR=	${FILESDIR}
SCRIPTS=	ttys

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
