# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/include/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

FILESDIR=	${LIBEXECDIR}/bsdconfig/include
FILES=		bsdconfig.hlp media.hlp messages.subr network_device.hlp \
		options.hlp tcp.hlp usage.hlp

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
