%global pre b1

Name:          salome-yacs
Version:       7.5.0
Release:       0.2%{?pre:.%pre}%{dist}
Summary:       Salome YACS module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the YACS_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/yacs.git YACS_SRC_$version$pre
#  $ (cd YACS_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf YACS_SRC_$version$pre.tar.gz YACS_SRC_$version$pre
Source0:       YACS_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch0:        0001-idl-dir.patch
# Fix adm dir
Patch1:        0002-adm-dir.patch
# Fix incorrect cmake add_dependencies usage
Patch2:        0003-add-dependencies.patch
# Fix conflict with chrono.hxx from smesh (see also in %%prep)
Patch3:        0004-chrono.patch

Source1:       macros.salome
%include %{SOURCE1}

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppunit-devel
BuildRequires: doxygen
BuildRequires: graphviz-devel
BuildRequires: jsoncpp-devel
BuildRequires: libxml2-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: paraview-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: PyQt4-devel
BuildRequires: qscintilla-devel
BuildRequires: qt-devel
BuildRequires: qwt-devel
BuildRequires: salome-gui-devel
BuildRequires: sip-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome YACS module.
The Salome yacs module allows to build, edit and execute calculation schemes.
See http://www.salome-platform.org/about/yacs


%package devel
Summary:       Development files for the Salome YACS module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome YACS module.


%package doc
Summary:       Documentation for the Salome YACS module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome YACS module.


%prep
%autosetup -p1 -n YACS_SRC_%{version}%{?pre:%{pre}}
%salome_prep

# Fix conflict with chrono.hxx from smesh (see also Patch4)
mv src/bases/chrono.hxx src/bases/YACSchrono.hxx

# Fix some lib -> %%{_libdir}
find . -type f -print0 | xargs -0 sed -i 's|module_root_dir,"lib"|module_root_dir,"%{_lib}"|g'
find . -type f -print0 | xargs -0 sed -i 's|lib/salome|%{_lib}/salome|g'


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files ..
make %{?_smp_mflags}


%install
%salome_install YACS

# I don't think this is needed
rm -r %{buildroot}%{_bindir}/HXX2SALOME_Test


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{python_sitelib}/salome/*
%{python_sitearch}/salome/
%{_datadir}/salome/resources/yacs/
%{_datadir}/salome/resources/pmml/
%{_datadir}/salome/yacssamples/
%{_datadir}/salome/yacssupervsamples/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_datadir}/idl/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/gui/YACS/
%doc %{_defaultdocdir}/salome/tui/YACS/


%changelog
* Fri Nov 21 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.2.b1
- Salome 7.5.0b1
