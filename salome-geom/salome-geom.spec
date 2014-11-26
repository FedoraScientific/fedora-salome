%global pre rc1

Name:          salome-geom
Version:       7.5.0
Release:       0.3%{?pre:.%pre}%{dist}
Summary:       Salome CAD (GEOM) module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the GEOM_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/geom.git GEOM_SRC_$version$pre
#  $ (cd GEOM_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf GEOM_SRC_$version$pre.tar.gz GEOM_SRC_$version$pre
Source0:       GEOM_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch1:        0001-idl-dir.patch
# Fix hardcoded salome_adm directory
Patch2:        0002-adm-dir.patch
# Fix conflict between VERSION from kernel and VERSION from geom
Patch3:        0003-conflicts.patch
# Fix KERNEL_ROOT_DIR incorrectly searched in ENV
Patch4:        0004-kernel-root-dir.patch
# Search VTK modules in paraview dir
Patch5:        0005-vtk-libs.patch

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
BuildRequires: netcdf-cxx-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: opencv-devel
BuildRequires: paraview-devel
BuildRequires: protobuf-devel
BuildRequires: pugixml-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: qt-devel
BuildRequires: qtwebkit-devel
BuildRequires: qwt-devel
BuildRequires: salome-kernel-devel
BuildRequires: salome-gui-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome CAD (GEOM) module.
The Salome CAD (GEOM) module provides versatile functionalities for creation,
visualization and modification of geometric CAD models.
See http://www.salome-platform.org/about/geometry


%package devel
Summary:       Development files for the Salome CAD module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Salome CAD (GEOM) module.


%package doc
Summary:       Documentation for the Salome CAD (GEOM) module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome CAD (GEOM) module.


%prep
%autosetup -p1 -n GEOM_SRC_%{version}%{?pre:%{pre}}
%salome_prep


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files  ..
make %{?_smp_mflags}


%install
%salome_install GEOM


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{python_sitelib}/salome/*
%{python_sitearch}/salome/*.*
%{python_sitearch}/salome/salome/*
%{python_sitearch}/salome/shared_modules/*
%{_datadir}/salome/resources/geom/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_datadir}/idl/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/gui/GEOM/
%doc %{_defaultdocdir}/salome/tui/GEOM/
%doc %{_defaultdocdir}/salome/examples/GEOM/


%changelog
* Wed Nov 26 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.3.rc1
- Salome 7.5.0rc1
