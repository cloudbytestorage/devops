# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/startup/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

SUBDIR= include share

FILESDIR=	${LIBEXECDIR}/bsdconfig/140.startup
FILES=		INDEX USAGE

SCRIPTSDIR=	${FILESDIR}
SCRIPTS=	misc rcadd rcconf rcdelete rcedit rcvar startup

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
