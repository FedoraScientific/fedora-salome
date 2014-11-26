%global pre rc1

Name:          salome-kernel
Version:       7.5.0
Release:       0.3%{?pre:.%pre}%{dist}
Summary:       Salome core (Kernel) module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the KERNEL_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/kernel.git KERNEL_SRC_$version$pre
#  $ (cd KERNEL_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf KERNEL_SRC_$version$pre.tar.gz KERNEL_SRC_$version$pre
Source0:       KERNEL_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Fix missing destdir in various places
# find . -type f -not -path "*/deprecated/*" -print0 | xargs -0 sed -i 's|${CMAKE_INSTALL_PREFIX}|\\$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}|g'
Patch1:        0001-destdir.patch
# Install idl files to $prefix/share/idl, not $prefix/idl
Patch2:        0002-idl-dir.patch
# Fix lib -> lib64
# grep -r --exclude-dir=DEPRECATED --exclude-dir=deprecated --exclude="*.m4" --exclude=ChangeLog --exclude-dir=configuration_examples  '["/ ]lib["/]'
Patch3:        0003-libsuffix.patch
# Install salome_adm, adm_local files to share/salome/salome_adm
Patch4:        0004-adm-dir.patch
# Fix OCE detection
Patch5:        0005-detect-oce.patch
# Fix Paraview-VTK detection
Patch6:        0006-detect-paraview-vtk.patch

Source1:       macros.salome
%include %{SOURCE1}

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppunit-devel
BuildRequires: doxygen
BuildRequires: gcc-gfortran
BuildRequires: graphviz-devel
BuildRequires: hdf5-devel
BuildRequires: libbatch-devel
BuildRequires: libxml2-devel
BuildRequires: numpy
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: swig

Requires:      paraview
Requires:      python-omniORB
Requires:      omniORB-servers

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome core (Kernel) module.
The Salome kernel module defines the core functionalities of Salome.
See http://www.salome-platform.org/about/kernel


%package devel
Summary:       Development files for the Salome core (Kernel) module
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome core (Kernel) module.


%package doc
Summary:       Documentation for the Salome core (Kernel) module
BuildArch:     noarch

%description doc
Documentation for the Salome core (Kernel) module.


%prep
%autosetup -p1 -n KERNEL_SRC_%{version}%{?pre:%{pre}}
%salome_prep

# Fix file-not-utf8
iconv -f iso8859-1 -t utf-8 ChangeLog > ChangeLog.conv && mv -f ChangeLog.conv ChangeLog


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
%salome_install KERNEL

# Own folders which are used by modules to simplify things
mkdir -p %{buildroot}%{_datadir}/salome/plugins
mkdir -p %{buildroot}%{python_sitearch}/salome/shared_modules
mkdir -p %{buildroot}%{_defaultdocdir}/salome/{dev,tui,gui,examples}

# Scripts in %%{_bindir}
install -dm 0755 %{buildroot}%{_bindir}
ln -s %{_libexecdir}/salome/killSalome.py %{buildroot}%{_bindir}/killSalome
cat > %{buildroot}%{_bindir}/runSalome <<EOF
#!/bin/sh
for file in %{_datadir}/salome/env/*.env; do
  source \$file
done
export PATH=%{_libexecdir}/salome:\$PATH
export PYTHONPATH=%{python_sitelib}/salome:%{_libexecdir}/salome:\$PYTHONPATH
export LD_LIBRARY_PATH=%{_libdir}/paraview:\$LD_LIBRARY_PATH
%{_libexecdir}/salome/runSalome.py $*
EOF
chmod 755 %{buildroot}%{_bindir}/runSalome

# Copyright scripts for -doc packages
install -Dpm 0644 COPYING %{buildroot}%{_defaultdocdir}/salome/COPYING


%files
%doc ChangeLog COPYING
%{_bindir}/runSalome
%{_bindir}/killSalome
%dir %{_libexecdir}/salome/
%{_libexecdir}/salome/*
%dir %{_libdir}/salome/
%{_libdir}/salome/*
%dir %{python_sitelib}/salome/
%{python_sitelib}/salome/*
%dir %{python_sitearch}/salome/
%dir %{python_sitearch}/salome/salome/
%dir %{python_sitearch}/salome/shared_modules/
%{python_sitearch}/salome/*.*
%{python_sitearch}/salome/salome/*
%dir %{_datadir}/salome
%dir %{_datadir}/salome/plugins
%dir %{_datadir}/salome/resources/
%dir %{_datadir}/salome/env
%{_datadir}/salome/resources/kernel/
%{_datadir}/salome/env/%{name}.env

%files devel
%dir %{_includedir}/salome/
%{_includedir}/salome/*
%dir %{_datadir}/idl/salome/
%{_datadir}/idl/salome/*
%dir %{_datadir}/salome/adm/
%dir %{_datadir}/salome/adm/cmake_files
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/


%changelog
* Wed Nov 26 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.3.rc1
- Salome 7.5.0rc1
