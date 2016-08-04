# $FreeBSD: releng/9.2/share/dtrace/Makefile 251697 2013-06-13 18:47:53Z gnn $
#
# Hand installing our scripts and optionally (based on MK_CDDL) installing
# the DTraceToolkit.
#

.include <bsd.own.mk>

SUBDIR= ${_toolkit}

.if ${MK_CDDL} != "no"
_toolkit=	toolkit
.endif

SCRIPTS=	nfsclienttime hotopen

SCRIPTSDIR= ${SHAREDIR}/dtrace

NO_OBJ=

.include <bsd.prog.mk>
