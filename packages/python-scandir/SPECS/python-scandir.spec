# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2
%global _python_bytecompile_extra 1

%global pypi_name scandir
%global sum   A better directory iterator and faster os.walk() for Python
%global desc scandir() is a directory iteration function like os.listdir(), except that \
instead of returning a list of bare filenames, it yields DirEntry objects that \
include file type and stat information along with the name. Using scandir() \
increases the speed of os.walk() by 2-20 times (depending on the platform and \
file system) by avoiding unnecessary calls to os.stat() in most cases. \
scandir is included in the Python 3.5+ standard library.

%bcond_without python3

# Drop Python 2 with Fedora 32 and EL8
#%%if (0%%{?fedora} && 0%%{?fedora} < 32) || (0%%{?rhel} && 0%%{?rhel} < 8)
  %bcond_without python2
#%%else
#  %%bcond_with python2
#%%endif


Name:           python-%{pypi_name}
Version:        1.9.0
Release:        6%{?dist}
Summary:        %{sum}
URL:            https://github.com/benhoyt/scandir
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
License:        BSD

BuildRequires:  gcc

%if %{with python2}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools

# Additional build requirements for Python 2.6
%if 0%{?el6}
BuildRequires:  python-unittest2
%endif
%endif

%if %{with python3}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%if 0%{?with_python3_other}
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools
%endif

%description
%{desc}


# Python 2 package
%if %{with python2}
%package -n     python2-%{pypi_name}

Summary:        %{sum}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
%{desc}
%endif

# Python 3 package
%if %{with python3}
%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
%{desc}
%endif

# Python 3 other package
%if 0%{?with_python3_other}
%package -n     python%{python3_other_pkgversion}-%{pypi_name}
Summary:        %{sum}
%{?python_provide:%python_provide python%{python3_other_pkgversion}-%{pypi_name}}

%description -n python%{python3_other_pkgversion}-%{pypi_name}
%{desc}
%endif


%prep
%setup -q -n %{pypi_name}-%{version}


%build
%if %{with python2}
CFLAGS="$RPM_OPT_FLAGS" %py2_build
%endif

%if %{with python3}
CFLAGS="$RPM_OPT_FLAGS" %py3_build
%endif

%if 0%{?with_python3_other}
CFLAGS="$RPM_OPT_FLAGS" %py3_other_build
%endif


%install
%if 0%{?with_python3_other}
%{__python3_other} setup.py install --skip-build --root %{buildroot}
%endif

%if %{with python3}
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif

%if %{with python2}
%{__python2} setup.py install --skip-build --root %{buildroot}
%endif


%check
LANG=C.utf8
%if %{with python2}
%{__python2} test/run_tests.py
rm -rf test/testdir
%endif

%if %{with python3}
%{__python3} test/run_tests.py
rm -rf test/testdir
%endif

%if 0%{?with_python3_other}
%{__python3_other} setup.py test
rm -rf test/testdir
%endif


%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE*
%doc README* benchmark.py
%{python2_sitearch}/scandir*
%attr(755,root,root) %{python2_sitearch}/_scandir*.so
%endif

%if %{with python3}
%files -n python%{python3_pkgversion}-%{pypi_name}
%license LICENSE*
%doc README* benchmark.py

%{python3_sitearch}/scandir*
%{python3_sitearch}/__pycache__/scandir*
%attr(755,root,root) %{python3_sitearch}/_scandir*.so
%endif

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-%{pypi_name}
%license LICENSE*
%doc README* benchmark.py
%{python3_other_sitearch}/scandir*
%{python3_other_sitearch}/__pycache__/scandir*
%attr(755,root,root) %{python3_other_sitearch}/_scandir*.so
%endif


%changelog
* Wed Jul 31 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-6
- Restore python2-scandir in F31 (it is still needed by python2-pytest)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.0-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Mon Nov 05 2018 Avram Lubkin <aviso@fedoraproject.org> - 1.9.0-2
- Restore python2-scandir in F30 (bz#1645935)

* Sun Nov 04 2018 Avram Lubkin <aviso@fedoraproject.org> - 1.9.0-1
- Updated to 1.9.0 (bz#1614995)
- Don't include tests

* Sat Aug 04 2018 Avram Lubkin <aviso@fedoraproject.org> - 1.8-1
- Updated to 1.8 (bz#1611869)
- Rework spec for Python version conditionals and newer guidelines

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7-2
- Rebuilt for Python 3.7

* Mon Apr 16 2018 Avram Lubkin <aviso@fedoraproject.org> - 1.7-1
- Updated to 1.7 (bz#1394440)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3-2
- Rebuild for Python 3.6

* Fri Sep 02 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.3-1
- Updated to 1.3 (bz#1370901)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-3
- Build Python3 package for el7+

* Tue Jan 19 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-2
- Fixed typos and logic in spec file

* Mon Jan 18 2016 Avram Lubkin <aviso@fedoraproject.org> - 1.2-1
- Updated to version 1.2
- Use python2 macros instead of bare python macros
- Changed Python2 package name to python2-scandir for Fedora 24+
- Use python3_pkgversion for package names

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jul 22 2015 Avram Lubkin <aviso@fedoraproject.org> - 1.1-1
- Initial package.

