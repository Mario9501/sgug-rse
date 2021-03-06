Name:           perl-Config-AutoConf
Version:        0.317
Release:        6%{?dist}
Summary:        A module to implement some of AutoConf macros in pure Perl
License:        GPL+ or Artistic
URL:            https://metacpan.org/release/Config-AutoConf
Source0:        https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Config-AutoConf-%{version}.tar.gz
BuildArch:      noarch
# Build
BuildRequires:  gcc
BuildRequires:  perl-interpreter
BuildRequires:  perl-generators
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Runtime
BuildRequires:  perl(base)
BuildRequires:  perl(Capture::Tiny)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(Text::ParseWords)
# Tests only
BuildRequires:  perl(Cwd)
BuildRequires:  perl(ExtUtils::CBuilder)
# Unused BuildRequires:  perl(IO::String)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "$(perl -V:version)"; echo $version))

%description
This module simulates some of the tasks autoconf macros do.  To detect
a command, a library and similar.

%prep
%setup -q -n Config-AutoConf-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README.md
%{perl_vendorlib}/*
%{_mandir}/man3/*

%changelog
* Tue Oct 06 2020  HAL <notes2@gmx.de> - 0.317-6
- compiles on Irix 6.5 with sgug-rse gcc 9.2. All tests pass.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 0.317-5
- Perl 5.30 rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.317-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Jitka Plesnikova <jplesnik@redhat.com> - 0.317-2
- Perl 5.28 rebuild

* Sun Jun 10 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.317-1
- Update to 0.317

* Sun Apr 22 2018 Emmanuel Seyman <emmanuel@seyman.fr> - 0.316-1
- Update to 0.316

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.315-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug 06 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.315-1
- Update to 0.315

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.314-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 0.314-2
- Perl 5.26 rebuild

* Sun Apr 02 2017 Emmanuel Seyman <emmanuel@seyman.fr> - 0.314-1
- Update to 0.314

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.313-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 31 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.313-1
- Update to 0.313

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 0.311-6
- Perl 5.24 rebuild

* Sun Mar 20 2016 Emmanuel Seyman <emmanuel@seyman.fr> - 0.311-5
- Replace glibc-headers as a glibc-headers with gcc (#1230486)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.311-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.311-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 11 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.311-2
- Perl 5.22 rebuild

* Wed Jun 10 2015 Petr Šabata <contyk@redhat.com> - 0.311-1
- 0.311 bump

* Thu Jun 04 2015 Jitka Plesnikova <jplesnik@redhat.com> - 0.309-2
- Perl 5.22 rebuild

* Wed Feb 18 2015 Petr Šabata <contyk@redhat.com> - 0.309-1
- 0.309 bump

* Thu Nov 06 2014 Petr Šabata <contyk@redhat.com> 0.305-1
- Initial packaging
