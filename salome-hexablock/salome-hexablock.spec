%global pre b1

Name:          salome-hexablock
Version:       7.5.0
Release:       0.2%{?pre:.%pre}%{dist}
Summary:       Salome hexablock module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the HEXABLOCK_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/hexablock.git HEXABLOCK_SRC_$version$pre
#  $ (cd HEXABLOCK_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf HEXABLOCK_SRC_$version$pre.tar.gz HEXABLOCK_SRC_$version$pre
Source0:       HEXABLOCK_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Fix compilation with -Werror=format-security
Patch0:        0001-format-security.patch
# Rename various files which can cause conflicts (see also %%prep)
Patch1:        0002-conflicts.patch

Source1:       macros.salome
%include %{SOURCE1}

BuildRequires: boost-devel
BuildRequires: cmake
BuildRequires: cppunit-devel
BuildRequires: doxygen
BuildRequires: gcc-gfortran
BuildRequires: graphviz-devel
BuildRequires: hdf5-devel
BuildRequires: jsoncpp-devel
BuildRequires: libxml2-devel
BuildRequires: med-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: paraview-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: qt-devel
BuildRequires: PyQt4-devel
BuildRequires: qwt-devel
BuildRequires: salome-kernel-devel
BuildRequires: salome-gui-devel
BuildRequires: salome-geom-devel
BuildRequires: sip-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}
Requires:      salome-geom%{?_isa} = %{version}-%{release}

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome HEXABLOCK module.
The Salome meshing module aims at helping users to build hexahedral meshes by
creating of a model of the blocks. 


%package devel
Summary:       Development files for the Salome HEXABLOCK module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}
Requires:      salome-geom-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome HEXABLOCK module.


%package doc
Summary:       Documentation for the Salome HEXABLOCK module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome HEXABLOCK module.


%prep
%autosetup -p1 -n HEXABLOCK_SRC_%{version}%{?pre:%{pre}}
%salome_prep

# Rename file to avoid conflicts (see also Patch1)
mv bin/myrunSalome.py bin/runSalomeHexablock.py


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DGEOM_ROOT_DIR=%{_prefix} \
	-DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files ..
make %{?_smp_mflags}


%install
%salome_install HEXABLOCK


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{_datadir}/salome/resources/hexablock/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/gui/HEXABLOCK/


%changelog
* Fri Nov 21 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.2.b1
- Salome 7.5.0b1
