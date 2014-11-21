%global pre b1

Name:          salome-paravis
Version:       7.5.0
Release:       0.2%{?pre:.%pre}%{dist}
Summary:       Salome PARAVIS module

License:       LGPLv2+
URL:           http://www.salome-platform.org/

# Either download the latest release from
#  http://files.salome-platform.org/Salome/Salome$version/src$version.tar.gz
# and create a tarbal of the PARAVIS_SRC_$version folder contained within, or
#  $ git clone git://git.salome-platform.org/modules/paravis.git PARAVIS_SRC_$version$pre
#  $ (cd PARAVIS_SRC_$version$pre; git checkout tags/V${version//./_}$pre; rm -rf .git)
#  $ tar -cf PARAVIS_SRC_$version$pre.tar.gz PARAVIS_SRC_$version$pre
Source0:       PARAVIS_SRC_%{version}%{?pre:%{pre}}.tar.gz
# Search idl files in ${SALOME_INSTALL_IDLS}
Patch0:        0001-idl-dir.patch
# Fix getwrapperclasses
Patch1:        0002-getwrapclasses.patch
# Use paraview bundled vtk libraries
Patch2:        0003-paraview-vtk.patch
# Fix incompatibility between int and vtkIdType (aka long long int)
Patch3:        0004-vtkidtype.patch
# Fix lib/salome and lib/paraview install dirs
Patch4:        0005-install-dirs.patch
# Fix conflict between VERSION from kernel and VERSION from paravis
Patch5:        0006-conflicts.patch

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
BuildRequires: netcdf-cxx-devel
BuildRequires: numpy
BuildRequires: OCE-devel
BuildRequires: omniORB-devel
BuildRequires: omniORBpy-devel
BuildRequires: paraview-devel
BuildRequires: protobuf-devel
BuildRequires: python-devel
BuildRequires: python-sphinx
BuildRequires: qt-devel
BuildRequires: PyQt4-devel
BuildRequires: qwt-devel
BuildRequires: salome-kernel-devel
BuildRequires: salome-gui-devel
BuildRequires: salome-med-devel
BuildRequires: sip-devel
BuildRequires: swig
BuildRequires: libXmu-devel

Requires:      salome-kernel%{?_isa} = %{version}-%{release}
Requires:      salome-gui%{?_isa} = %{version}-%{release}
Requires:      salome-med%{?_isa} = %{version}-%{release}
Requires:      paraview

%description
SALOME is an open-source software that provides a generic platform for Pre- and
Post-Processing for numerical simulation. It is based on an open and flexible
architecture made of reusable components.

This package contains the Salome PARAVIS module.
The PARAVIS module allows creating, launching and following calculation jobs
on different types of computers.


%package devel
Summary:       Development files for the Salome PARAVIS module
Requires:      %{name}%{?_isa} = %{version}-%{release}
Requires:      salome-kernel-devel%{?_isa} = %{version}-%{release}
Requires:      salome-gui-devel%{?_isa} = %{version}-%{release}
Requires:      salome-med-devel%{?_isa} = %{version}-%{release}
# For %%{_includedir}/paraview
Requires:      paraview-devel

%description devel
Development files for the Salome PARAVIS module.


%package doc
Summary:       Documentation for the Salome PARAVIS module
BuildArch:     noarch
Requires:      salome-kernel-doc = %{version}-%{release}

%description doc
Documentation for the Salome PARAVIS module.


%prep
%autosetup -p1 -n PARAVIS_SRC_%{version}%{?pre:%{pre}}
%salome_prep

# Fix some lib -> %%{_libdir}
sed -i 's|"lib", "paraview"|"%{_lib}", "paraview"|' bin/paravis_setenv.py


%build
mkdir build
cd build
%cmake \
	-DKERNEL_ROOT_DIR=%{_prefix} \
	-DGUI_ROOT_DIR=%{_prefix} \
	-DMED_ROOT_DIR=%{_prefix} \
	-DPARAVIEW_ROOT_DIR=%{_datadir}/cmake/paraview \
	-DCMAKE_MODULE_PATH="%{_datadir}/salome/adm/cmake_files"  ..
make %{?_smp_mflags}


%install
%salome_install PARAVIS


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc COPYING
%{_libexecdir}/salome/*
%{_libdir}/salome/*
%{_libdir}/paraview/*
%{python_sitelib}/salome/*
%{_datadir}/salome/resources/paravis/
%{_datadir}/salome/env/%{name}.env

%files devel
%{_includedir}/salome/*
%{_includedir}/paraview/*
%{_datadir}/idl/salome/*
%{_datadir}/cmake/paraview/Modules/vtkMEDReader.cmake
%{_datadir}/salome/adm/cmake_files/*

%files doc
%doc doc/GeneralArchitecture.html*
%doc doc/GeneralArchitecture_html_m4ed0a034.gif
%doc doc/UserDocumentation.html


%changelog
* Fri Nov 21 2014 Sandro Mani <manisandro@gmail.com> - 7.5.0-0.2.b1
- Salome 7.5.0b1
