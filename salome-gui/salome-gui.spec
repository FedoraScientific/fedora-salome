%global pre rc1

Name:          salome-gui
Version:       7.5.0
Release:       0.3%{?pre:.%pre}%{dist}
Summary:       Salome GUI module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the GUI_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/gui.git GUI_SRC_$version$pre
#  $ (cd GUI_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf GUI_SRC_$version$pre.tar.gz GUI_SRC_$version$pre
Source0:       GUI_SRC_%{version}%{?pre:%{pre}}.tar.gz
Source1:       salome.desktop
Source2:       salome.png
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch1:        0001-idl-dir.patch
# Qt fixes
Patch2:        0002-qt-fixes.patch
# Add missing destdir
Patch3:        0003-destdir.patch
# Fix lib -> lib64
Patch4:        0004-libsuffix.patch
# Fix -Werror=format-security issues
Patch5:        0005-format-security.patch
# Fix conflict between VERSION from kernel and VERSION from gui
Patch6:        0006-conflicts.patch
# Add missing QtNetwork library
Patch7:        0007-qt-lib.patch

Source3:       macros.salome
%include %{SOURCE3}

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppunit-devel
BuildRequires: desktop-file-utils
BuildRequires: doxygen
BuildRequires: graphviz-devel
BuildRequires: hdf5-devel
BuildRequires: jsoncpp-devel
BuildRequires: libxml2-devel
BuildRequires: libXmu-devel
BuildRequires: netcdf-cxx-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: paraview-devel
BuildRequires: protobuf-devel
BuildRequires: pugixml-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: qt-devel
BuildRequires: qtwebkit-devel
BuildRequires: PyQt4-devel
BuildRequires: qwt-devel
BuildRequires: salome-kernel-devel
BuildRequires: sip-devel
BuildRequires: swig

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      paraview
Requires:      hicolor-icon-theme

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome GUI module.
The Salome GUI module provides a common shell for all components.
See http://www.salome-platform.org/about/gui


%package devel
Summary:       Development files for the Salome GUI module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome GUI module.


%package doc
Summary:       Documentation for the Salome GUI module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome GUI module.


%prep
%autosetup -p1 -n GUI_SRC_%{version}%{?pre:%{pre}}
%salome_prep

# Fix some lib -> %%{_libdir}
sed -i 's|"lib", "paraview"|"%{_lib}", "paraview"|' bin/gui_setenv.py
sed -i 's|${ROOTDIR}/lib/|${ROOTDIR}/%{_lib}|g' bin/runLightSalome.sh


%build
mkdir build
cd build
%cmake \
  -DKERNEL_ROOT_DIR=%{_prefix} \
  -DPARAVIEW_ROOT_DIR=%{_datadir}/cmake/paraview \
  -DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files  ..
make %{?_smp_mflags}


%install
%salome_install GUI

# Desktop file and icon
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{SOURCE1}
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/salome.png


%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
# %%{_libdir}/paraview/ owned by paraview
%{_libdir}/paraview/*
%{python_sitelib}/salome/*
%{python_sitearch}/salome/*.*
%{python_sitearch}/salome/salome/*
%{_datadir}/applications/salome.desktop
%{_datadir}/icons/hicolor/64x64/apps/salome.png
%{_datadir}/salome/plugins/gui/
%{_datadir}/salome/resources/gui/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_datadir}/idl/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/gui/GUI/
%doc %{_defaultdocdir}/salome/tui/GUI/


%changelog
* Wed Nov 26 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.3.rc1
- Salome 7.5.0rc1
