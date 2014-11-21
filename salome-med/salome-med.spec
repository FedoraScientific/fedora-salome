%global pre b1

Name:          salome-med
Version:       7.5.0
Release:       0.2%{?pre:.%pre}%{dist}
Summary:       Salome MED module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the MED_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/med.git MED_SRC_$version$pre
#  $ (cd MED_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf MED_SRC_$version$pre.tar.gz MED_SRC_$version$pre
Source0:       MED_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Correctly inherit directory paths from salome-kernel config
Patch0:        0001-use-kernel-directories.patch
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch1:        0002-idl-dir.patch
# Fix hardcoded adm directories
Patch2:        0003-adm-dir.patch
# Fix compilation against new metis (ugly, reinterpret_cast-ing pointers)
Patch3:        0004-metis.patch
# Fix conflict between VERSION from kernel and VERSION from med
Patch4:        0005-conflicts.patch

Source1:       macros.salome
%include %{SOURCE1}

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppunit-devel
BuildRequires: doxygen
BuildRequires: graphviz-devel
BuildRequires: hdf5-devel
BuildRequires: jsoncpp-devel
BuildRequires: libxml2-devel
BuildRequires: med-devel
BuildRequires: metis-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: paraview-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: qt-devel
BuildRequires: qwt-devel
BuildRequires: salome-kernel-devel
BuildRequires: salome-gui-devel
BuildRequires: scotch-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome MED module.
The Salome MED module provides a standard for storing and recovering computer
data associated to numerical meshes and fields.
See http://www.salome-platform.org/about/med


%package devel
Summary:       Development files for the Salome MED module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome MED module.


%package doc
Summary:       Documentation for the Salome MED module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome MED module.


%prep
%autosetup -p1 -n MED_SRC_%{version}%{?pre:%{pre}}
%salome_prep


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files ..
make %{?_smp_mflags}


%install
%salome_install MED


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{python_sitelib}/salome/*
%{python_sitearch}/salome/*.*
%{python_sitearch}/salome/xmed/
%{_datadir}/salome/resources/med/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_datadir}/idl/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/dev/MED/
%doc %{_defaultdocdir}/salome/gui/MED/
%doc %{_defaultdocdir}/salome/tui/MED/


%changelog
* Fri Nov 21 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.2.b1
- Salome 7.5.0b1
