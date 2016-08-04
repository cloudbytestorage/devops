# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/share/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

SUBDIR=	media packages

FILESDIR=	${SHAREDIR}/bsdconfig
FILES=		common.subr device.subr dialog.subr mustberoot.subr \
		script.subr strings.subr struct.subr sysrc.subr variable.subr

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
