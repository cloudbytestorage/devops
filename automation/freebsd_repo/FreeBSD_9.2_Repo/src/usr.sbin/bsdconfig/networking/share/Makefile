# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/networking/share/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

FILESDIR=	${SHAREDIR}/bsdconfig/networking
FILES=		common.subr device.subr hostname.subr ipaddr.subr media.subr \
		netmask.subr resolv.subr routing.subr services.subr

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
