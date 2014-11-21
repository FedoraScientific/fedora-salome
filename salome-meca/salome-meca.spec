%global hash 758cf5156804

Name:          salome-meca
Version:       2014.1
Release:       1%{?pre:.%pre}%{dist}
Summary:       Salome core (Kernel) module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# wget --content-disposition https://bitbucket.org/code_aster/salome-codeaster/get/%%{version}.tar.gz
Source0:       code_aster-salome-codeaster-%{hash}.tar.gz

BuildRequires: salome-kernel-devel
BuildRequires: salome-gui-devel
BuildRequires: salome-med-devel
BuildRequires: salome-geom-devel
BuildRequires: salome-yacs-devel
BuildRequires: salome-smesh-devel
BuildRequires: salome-smesh-plugin-netgen

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
%autosetup -p1 -n code_aster-salome-codeaster-%{hash}

# Replace all occurences of bin/salome with libexec/salome, easier done here than with a patch
find . -type f -print0 | xargs -0 sed -i 's|bin/salome|libexec/salome|g'

# Fix python shebangs
find -name '*.py' | xargs sed -i '1s|^#!.*python|#!%{__python2}|'


%build
mkdir build
cd build
%cmake ..
make %{?_smp_mflags}


%install
# PYTHONPATH and LD_LIBRARY_PATH to have sphinx find the modules
export PYTHONPATH=%{buildroot}%{python_sitelib}/salome:%{buildroot}%{python_sitearch}/salome:%{buildroot}%{_libexecdir}/salome
export LD_LIBRARY_PATH=%{buildroot}%{_libdir}/salome
%make_install -C build

# Own folders which is used by modules to simplify things
mkdir -p %{buildroot}%{_datadir}/salome/plugins/
mkdir -p %{buildroot}%{python_sitearch}/salome/shared_modules/

# Don't install deprecated build scripts (paths there were not patched)
rm -rf %{buildroot}%{_datadir}/salome/adm/unix
rm -rf %{buildroot}%{_datadir}/salome/adm/cmake_files/deprecated

# Install docs through %%doc
mkdir doc_installed
mv %{buildroot}%{_datadir}/doc/salome/gui/KERNEL doc_installed/gui
mv %{buildroot}%{_datadir}/doc/salome/tui/KERNEL doc_installed/tui
rmdir %{buildroot}%{_datadir}/doc/salome/gui
rmdir %{buildroot}%{_datadir}/doc/salome/tui
rmdir %{buildroot}%{_datadir}/doc/salome

# Symlinks to %%{_bindir}
mkdir %{buildroot}%{_bindir}
ln -s %{_libexecdir}/salome/runSalome.py %{buildroot}%{_bindir}/runSalome
ln -s %{_libexecdir}/salome/killSalome.py %{buildroot}%{_bindir}/killSalome

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


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
%{_datadir}/salome/resources/kernel/

%files devel
%dir %{_includedir}/salome/
%{_includedir}/salome/*
%dir %{_datadir}/idl/salome/
%{_datadir}/idl/salome/*
%dir %{_datadir}/salome/adm/
%dir %{_datadir}/salome/adm/cmake_files
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc doc_installed/gui
%doc doc_installed/tui
%doc COPYING


%changelog
* Wed Jun 04 2014 Sandro Mani <manisandro@gmail.com> - 7.4.0-1
- Initial package
