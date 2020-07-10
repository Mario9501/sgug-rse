Name:           perl-App-FatPacker
Version:        0.010008
Release:        3%{?dist}
Summary:        Pack dependencies onto a script file
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/App-FatPacker
Source0:        https://cpan.metacpan.org/authors/id/M/MS/MSTROUT/App-FatPacker-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  findutils
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(B)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(File::Path)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Spec::Unix)
BuildRequires:  perl(Getopt::Long)
# Tests:
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Test::More) >= 0.82
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
This tool does all the work of tracing, collecting packlists, extracting
perl modules in fatlib, and then concatenating them into a packed script.

%prep
%setup -q -n App-FatPacker-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor
%{make_build}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
make test

%files
%doc Changes README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.010008-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.010008-2
- Perl 5.30 rebuild

* Mon Feb 18 2019 Petr Pisar <ppisar@redhat.com> - 0.010008-1
- 0.010008 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.010007-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.010007-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.010007-6
- Perl 5.28 rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.010007-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.010007-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.010007-3
- Perl 5.26 rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.010007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Petr Pisar <ppisar@redhat.com> - 0.010007-1
- 0.010007 bump

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.010005-3
- Perl 5.24 rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.010005-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 15 2015 Petr Pisar <ppisar@redhat.com> - 0.010005-1
- 0.010005 bump

* Mon Jun 29 2015 Petr Pisar <ppisar@redhat.com> - 0.010004-1
- 0.010004 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.010003-2
- Perl 5.22 rebuild

* Mon Apr 20 2015 Petr Pisar <ppisar@redhat.com> - 0.010003-1
- 0.010003 bump

* Wed Aug 27 2014 Jitka Plesnikova <jplesnik@redhat.com> - 0.010002-2
- Perl 5.20 rebuild

* Mon Aug 18 2014 Petr Pisar <ppisar@redhat.com> - 0.010002-1
- 0.010002 bump

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.010001-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 20 2014 Petr Pisar <ppisar@redhat.com> - 0.010001-1
- 0.010001 bump

* Tue Jan 07 2014 Petr Pisar <ppisar@redhat.com> 0.010000-1
- Specfile autogenerated by cpanspec 1.78.