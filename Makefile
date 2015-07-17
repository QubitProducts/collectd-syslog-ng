TARGET=deb
PACKAGE_NAME=collectd-syslog-ng-plugin
PACKAGE_VERSION=$(shell git describe)
PACKAGE_REVISION=1
PACKAGE_ARCH=all
PACKAGE_MAINTAINER=laurie@qubit.com
PACKAGE_FILE=$(PACKAGE_NAME)_$(PACKAGE_VERSION)-$(PACKAGE_REVISION)_$(PACKAGE_ARCH).$(TARGET)

$(PACKAGE_FILE):
	rm -rf build
	mkdir -p build/usr/lib/collectd/plugins/python
	cp syslog-ng.py build/usr/lib/collectd/plugins/python/syslog-ng.py
	cd build && \
	  fpm \
	  -t $(TARGET) \
	  -m $(PACKAGE_MAINTAINER) \
	  -n $(PACKAGE_NAME) \
	  -a $(PACKAGE_ARCH) \
	  -v $(PACKAGE_VERSION) \
	  --iteration $(PACKAGE_REVISION) \
	  -s dir \
	  -d collectd \
	  -p ../$(PACKAGE_FILE) \
	  .

package: $(PACKAGE_FILE)
