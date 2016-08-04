# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/security/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

SUBDIR= include

FILESDIR=	${LIBEXECDIR}/bsdconfig/130.security
FILES=		INDEX USAGE

SCRIPTSDIR=	${FILESDIR}
SCRIPTS=	kern_securelevel security

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
