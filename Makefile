SUBDIRS = $(shell ls -d */)

all:
	for dir in $(SUBDIRS) ; do \
		make -C  $$dir ; \
	done
