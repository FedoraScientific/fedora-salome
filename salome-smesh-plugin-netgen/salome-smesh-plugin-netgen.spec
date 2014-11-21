%global pre b1

Name:          salome-smesh-plugin-netgen
Version:       7.5.0
Release:       0.2%{?pre:.%pre}%{dist}
Summary:       Netgen plugin for the Salome meshing (SMESH) module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the SMESH_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/plugins/netgenplugin.git NETGENPLUGIN_SRC_$version$pre
#  $ (cd NETGENPLUGIN_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf NETGENPLUGIN_SRC_$version$pre.tar.gz NETGENPLUGIN_SRC_$version$pre
Source0:       NETGENPLUGIN_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch0:        0001-idl-dir.patch
# Fix conflict between VERSION from kernel and VERSION from netgen-plugin
Patch1:        0002-conflicts.patch
# Fix some ROOT_DIR variables
Patch2:        0003-root-dirs.patch
# Adapt for fedora netgen package
Patch3:        004-netgen.patch

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
BuildRequires: netgen-mesher-devel-private
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
BuildRequires: salome-geom-devel
BuildRequires: salome-gui-devel
BuildRequires: salome-smesh-devel
BuildRequires: sip-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}
Requires:      salome-geom%{?_isa} = %{version}-%{release}
Requires:      salome-smesh%{?_isa} = %{version}-%{release}

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Netgen plugin for the Salome meshing (SMESH) module.


%package devel
Summary:       Development files for the Netgen SMESH plugin
Requires:      salome-smesh-plugin-netgen%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-geom-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}
Requires:      salome-smesh-devel%{?_isa} = %{version}-%{release}

%description devel
Development files for the Netgen SMESH plugin.

%package doc
Summary:       Documentation for the Netgen SMESH plugin
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Netgen SMESH plugin.


%prep
%autosetup -p1 -n NETGENPLUGIN_SRC_%{version}%{?pre:%{pre}}
%salome_prep


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DGEOM_ROOT_DIR=%{_prefix} \
	-DSMESH_ROOT_DIR=%{_prefix} \
	-DCMAKE_MODULE_PATH=%{_datadir}/salome/adm/cmake_files ..
make %{?_smp_mflags}


%install
%salome_install


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{python_sitelib}/salome/*
%{python_sitearch}/salome/salome/*
%{_datadir}/salome/resources/netgenplugin/

%files devel
%{_includedir}/salome/*
%{_datadir}/idl/salome/*
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc %{_defaultdocdir}/salome/examples/NETGENPLUGIN/
%doc %{_defaultdocdir}/salome/gui/NETGENPLUGIN/


%changelog
* Fri Nov 21 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.2.b1
- Salome 7.5.0b1
