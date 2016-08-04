# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/timezone/share/Makefile 252995 2013-07-07 19:13:34Z dteske $

NO_OBJ=

FILESDIR=	${SHAREDIR}/bsdconfig/timezone
FILES=		continents.subr countries.subr iso3166.subr menus.subr \
		zones.subr

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}

.include <bsd.prog.mk>
