# $FreeBSD: releng/9.2/release/doc/share/xml/Makefile 251816 2013-06-16 18:59:07Z hrs $

RELN_ROOT?= ${.CURDIR}/../..

.include "${RELN_ROOT}/share/mk/doc.relnotes.mk"
.include "${DOC_PREFIX}/share/mk/doc.project.mk"

dev-auto.ent: ${MAN4PAGES} ${ARCHLIST} ${MAN2HWNOTES_CMD}
	${PERL} ${MAN2HWNOTES_CMD} ${MAN2HWNOTES_FLAGS} -a ${ARCHLIST} -o ${.TARGET} ${MAN4PAGES}

all: dev-auto.ent
