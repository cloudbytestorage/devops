# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/docsinstall/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

SUBDIR= include

FILESDIR=	${LIBEXECDIR}/bsdconfig/020.docsinstall
FILES=		INDEX USAGE

SCRIPTSDIR=	${FILESDIR}
SCRIPTS=	docsinstall

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
