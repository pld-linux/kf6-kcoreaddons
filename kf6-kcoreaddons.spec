#
# Conditional build:
%bcond_with	tests		# build with tests

# TODO:
# - runtime Requires if any
# - python3 buildings

%define		kdeframever	6.16
%define		qtver		5.15.2
%define		kfname		kcoreaddons
Summary:	Utilities for core application functionality and accessing the OS
Name:		kf6-%{kfname}
Version:	6.16.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	50ea12adb5f570a49837aa07fcce1600
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
%if %{with tests}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6Widgets-devel >= %{qtver}
%endif
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	ninja
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info >= 1.3
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt6Core >= %{qtver}
Requires:	kf6-dirs
#Obsoletes:	kf5-%{kfname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KCoreAddons provides classes built on top of QtCore to perform various
tasks such as manipulating mime types, autosaving files, creating
backup files, generating random sequences, performing text
manipulations such as macro replacement, accessing user information
and many more.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core >= %{qtver}
Requires:	cmake >= 3.16
#Obsoletes:	kf5-%{kfname}-devel < %{version}

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DBUILD_PYTHON_BINDINGS=OFF \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%{?with_tests:%ninja_build -C build test}


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/{ie,tok}

%find_lang %{kfname}5_qt --with-qm --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kfname}5_qt.lang
%defattr(644,root,root,755)
%doc README.md
%{_datadir}/mime/packages/kde6.xml
%attr(755,root,root) %{_libdir}/libKF6CoreAddons.so.*.*.*
%ghost %{_libdir}/libKF6CoreAddons.so.6
##%dir %{_libdir}/qt6/plugins/namespace
##%attr(755,root,root) %{_libdir}/qt6/plugins/namespace/jsonplugin_cmake_macro.so
##%attr(755,root,root) %{_libdir}/qt6/plugins/namespace/pluginwithoutmetadata.so
%{_datadir}/qlogging-categories6/kcoreaddons.categories
%{_datadir}/qlogging-categories6/kcoreaddons.renamecategories
%dir %{_libdir}/qt6/qml/org/kde/coreaddons
%{_libdir}/qt6/qml/org/kde/coreaddons/kcoreaddonsplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/coreaddons/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/coreaddons/libkcoreaddonsplugin.so
%{_libdir}/qt6/qml/org/kde/coreaddons/qmldir
%dir %{_datadir}/kf6/jsonschema
%{_datadir}/kf6/jsonschema/kpluginmetadata.schema.json

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KCoreAddons
%{_libdir}/cmake/KF6CoreAddons
%{_libdir}/libKF6CoreAddons.so
%{_pkgconfigdir}/KF6CoreAddons.pc
