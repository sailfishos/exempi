Name:       exempi
Summary:    Library for easy parsing of XMP metadata
Version:    2.5.2
Release:    1
License:    BSD
URL:        https://libopenraw.freedesktop.org/exempi/
Source0:    %{name}-%{version}.tar.bz2
Source1:    tests.xml
Patch0:     nemo-tests-install.patch
Patch1:     arm-on-aarch64.patch
# Unable to build testadobesdk https://gitlab.freedesktop.org/libopenraw/exempi/-/issues/17
Patch2:     drop-testadobesdk.patch
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  boost-devel

%description
Exempi provides a library for easy parsing of XMP metadata. It is a port of 
Adobe XMP SDK to work on UNIX and to be build with GNU automake.
It includes XMPCore and XMPFiles.


%package devel
Summary:    Headers for developing programs that will use %{name}
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files needed for
developing with exempi


%package tests
Summary:    Tests and tests.xml for %{name}
Requires:   %{name} = %{version}-%{release}

%description tests
This package contains the tests and tests.xml for %{name}


%prep
%autosetup -p1 -n %{name}-%{version}/exempi

%build
# nemo-tests-install.patch changes some of the Makefile.am
# so a autoreconf is needed to generate the new Makefile.in
%reconfigure --disable-static --enable-unittest

%make_build

%install
%make_install

install -m 0644 -D %{SOURCE1} %{buildroot}/opt/tests/%{name}/tests.xml

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/exempi
%{_libdir}/libexempi.so.8*
%exclude %{_datadir}/man/man1/exempi.1.gz

%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README
%{_includedir}/exempi-2.0/
%{_libdir}/libexempi.so
%{_libdir}/pkgconfig/*.pc

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*
