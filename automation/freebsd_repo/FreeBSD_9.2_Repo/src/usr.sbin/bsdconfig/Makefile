# $FreeBSD: releng/9.2/usr.sbin/bsdconfig/Makefile 252995 2013-07-07 19:13:34Z dteske $

SUBDIR=	console \
	diskmgmt \
	docsinstall \
	dot \
	examples \
	include \
	mouse \
	networking \
	packages \
	password \
	security \
	share \
	startup \
	timezone \
	ttys \
	usermgmt

FILESDIR=	${LIBEXECDIR}/bsdconfig
FILES=		USAGE

SCRIPTS= bsdconfig

MAN= bsdconfig.8

beforeinstall:
	mkdir -p ${DESTDIR}${FILESDIR}
	mkdir -p ${DESTDIR}${SCRIPTSDIR}
	mkdir -p ${DESTDIR}${MANDIR}8

.include <bsd.prog.mk>
