Name:       exempi
Summary:    Library for easy parsing of XMP metadata
Version:    2.4.3
Release:    1
Group:      System/Libraries
License:    BSD
URL:        http://libopenraw.freedesktop.org/wiki/Exempi
Source0:    http://libopenraw.freedesktop.org/download/%{name}-%{version}.tar.bz2
Source1:    tests.xml
Patch0:     nemo-tests-install.patch
Patch1:     arm-on-aarch64.patch
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
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
This package contains the libraries and header files needed for
developing with exempi


%package tests
Summary:    Tests and tests.xml for %{name}
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description tests
This package contains the tests and tests.xml for %{name}


%prep
%setup -q -n %{name}-%{version}/exempi

# nemo-tests-install.patch
%patch0 -p1
%patch1 -p1

%build
# nemo-tests-install.patch changes some of the Makefile.am
# so a autoreconf is needed to generate the new Makefile.in

%autogen --disable-static
%configure --disable-static \
    LDFLAGS="-L%{_libdir}" \
    CPPFLAGS="-I%{_includedir}" \
    --enable-unittest


# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf %{buildroot}

make DESTDIR=%{buildroot} install

rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.a
install -m 0644 $RPM_SOURCE_DIR/tests.xml $RPM_BUILD_ROOT/opt/tests/%{name}/tests.xml

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc COPYING
%{_bindir}/exempi
%{_libdir}/*.so.*
%exclude %{_datadir}/man/man1/exempi.1.gz

%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README
%defattr(-, root, root, -)
%{_includedir}/exempi-2.0/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files tests
%defattr(-,root,root,-)
/opt/tests/%{name}/*

