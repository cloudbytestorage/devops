#	@(#)Makefile	8.2 (Berkeley) 4/19/94
# $FreeBSD: releng/9.2/games/fortune/datfiles/Makefile 251319 2013-06-03 17:33:12Z jhb $

DB=	fortunes freebsd-tips murphy startrek zippy

# TO AVOID INSTALLING THE POTENTIALLY OFFENSIVE FORTUNES, COMMENT OUT THE
# NEXT LINE.
DB+=	limerick murphy-o gerrold.limerick

BLDS=	${DB:S/$/.dat/}
FILES=	${DB} ${BLDS}
CLEANFILES+=${BLDS}

FILESDIR=	${SHAREDIR}/games/fortune

.for f in ${DB}
$f.dat: $f
	PATH=$$PATH:/usr/games:${.OBJDIR}/../strfile \
	    strfile -Cs ${.ALLSRC} ${.TARGET}
.endfor

.include <bsd.prog.mk>
