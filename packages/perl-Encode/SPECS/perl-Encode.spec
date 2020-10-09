# Because encoding sub-package has an independent version, version macro gets
# redefined.
%global cpan_version 3.07
Name:           perl-Encode
Epoch:          4
Version:        %{cpan_version}
# Keep increasing release number even when rebasing version because
# perl-encoding sub-package has independent version which does not change
# often and consecutive builds would clash on perl-encoding NEVRA. This is the
# same case as in perl.spec.
Release:        457%{?dist}
Summary:        Character encodings in Perl
# ucm:          UCD
# bin/encguess: Artistic 2.0
# other files:  GPL+ or Artistic
License:        (GPL+ or Artistic) and Artistic 2.0 and UCD
URL:            https://metacpan.org/release/Encode
Source0:        https://cpan.metacpan.org/authors/id/D/DA/DANKOGAI/Encode-%{cpan_version}.tar.gz
BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  perl-interpreter
BuildRequires:  perl(Config)
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.76
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# enc2xs is run at build-time
# Run-time:
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter) >= 5.57
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(Filter::Util::Call)
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(Getopt::Std)
# I18N::Langinfo is optional
BuildRequires:  perl(MIME::Base64)
BuildRequires:  perl(overload)
BuildRequires:  perl(parent) >= 0.221
# PerlIO::encoding is optional
# POSIX is optional
BuildRequires:  perl(re)
BuildRequires:  perl(Storable)
BuildRequires:  perl(utf8)
BuildRequires:  perl(vars)
BuildRequires:  perl(XSLoader)
# Tests:
# Benchmark not used
BuildRequires:  perl(blib)
BuildRequires:  perl(charnames)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(IO::Select)
BuildRequires:  perl(IPC::Open3)
# IPC::Run not used
# JSON::PP not used
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Tie::Scalar)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(parent) >= 0.221

%{?perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\((Encode::ConfigLocal|MY)\\)

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\((Exporter|parent)\\)$

%description
The Encode module provides the interface between Perl strings and the rest
of the system. Perl strings are sequences of characters.

%package -n perl-encoding
Summary:        Write your Perl script in non-ASCII or non-UTF-8
Version:        3.00
License:        GPL+ or Artistic
# Keeping this sub-package arch-specific because it installs files into
# arch-specific directories.
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(Carp)
# Config not needed on perl ≥ 5.008
# Consider Filter::Util::Call as mandatory, bug #1165183, CPAN RT#100427
Requires:       perl(Filter::Util::Call)
# I18N::Langinfo is optional
Suggests:       perl(PerlIO::encoding)
Requires:       perl(utf8)
Conflicts:      perl-Encode < 2:2.64-2

%description -n perl-encoding
With the encoding pragma, you can write your Perl script in any encoding you
like (so long as the Encode module supports it) and still enjoy Unicode
support.

However, this encoding module is deprecated under perl 5.18. It uses
a mechanism provided by perl that is deprecated under 5.18 and higher, and may
be removed in a future version.

The easiest and the best alternative is to write your script in UTF-8.

# To mirror files from perl-devel (bug #456534)
# Keep architecture specific because files go into vendorarch
%package devel
Summary:        Perl Encode Module Generator
Version:        %{cpan_version}
License:        (GPL+ or Artistic) and UCD
Requires:       %{name}%{?_isa} = %{epoch}:%{cpan_version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Recommends:     perl-devel%{?_isa}
Requires:       perl(Encode)

%description devel
enc2xs builds a Perl extension for use by Encode from either Unicode Character
Mapping files (.ucm) or Tcl Encoding Files (.enc). You can use enc2xs to add
your own encoding to perl. No knowledge of XS is necessary.


%prep
%setup -q -n Encode-%{cpan_version}

%build
# Additional scripts can be installed by appending MORE_SCRIPTS, UCM files by
# INSTALL_UCM.
perl Makefile.PL INSTALLDIRS=vendor NO_PACKLIST=1 NO_PERLLOCAL=1 \
    OPTIMIZE="$RPM_OPT_FLAGS"
%{make_build}

%install
%{make_install}
find $RPM_BUILD_ROOT -type f -name '*.bs' -empty -delete
%{_fixperms} $RPM_BUILD_ROOT/*

%check
unset AUTHOR_TESTING ENC2XS_NO_COMMENTS ENC2XS_VERBOSE MAKEFLAGS PERL_CORE \
    PERL_ENCODING PERL_ENCODE_DEBUG
make test

%files
%doc AUTHORS Changes README
%{_bindir}/encguess
%{_bindir}/piconv
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Encode*
%exclude %{perl_vendorarch}/Encode/*.e2x
%exclude %{perl_vendorarch}/Encode/encode.h
%{_mandir}/man1/encguess.*
%{_mandir}/man1/piconv.*
%{_mandir}/man3/Encode.*
%{_mandir}/man3/Encode::*

%files -n perl-encoding
%doc AUTHORS Changes README
%{perl_vendorarch}/encoding.pm
%{_mandir}/man3/encoding.*

%files devel
%{_bindir}/enc2xs
%{_mandir}/man1/enc2xs.*
%{perl_vendorarch}/Encode/*.e2x
%{perl_vendorarch}/Encode/encode.h

%changelog
* Mon Sep 14 2020  HAL <notes2@gmx.de> - 4:3-07-457
- compiles on Irix 6.5 with sgug-rse gcc 9.2 passing all tests

* Mon Jul 27 2020 Petr Pisar <ppisar@redhat.com> - 4:3.07-457
- 3.07 bump

* Mon May 04 2020 Petr Pisar <ppisar@redhat.com> - 4:3.06-444
- 3.06 bump

* Thu Mar 19 2020 Petr Pisar <ppisar@redhat.com> - 4:3.05-443
- 3.05 bump

* Wed Mar 11 2020 Petr Pisar <ppisar@redhat.com> - 4:3.04-442
- 3.04 bump

* Mon Mar 02 2020 Petr Pisar <ppisar@redhat.com> - 4:3.03-441
- 3.03 bump

* Thu Jan 02 2020 Petr Pisar <ppisar@redhat.com> - 4:3.02-440
- 3.02 bump

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:3.01-439
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4:3.01-438
- Increase release to favour standalone package

* Wed Mar 13 2019 Petr Pisar <ppisar@redhat.com> - 4:3.01-10
- 3.01 bump

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4:3.00-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 31 2019 Petr Pisar <ppisar@redhat.com> - 4:3.00-8
- 3.00 bump

* Mon Jan 21 2019 Petr Pisar <ppisar@redhat.com> - 4:2.99-7
- 2.99 bump

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.98-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.98-5
- Perl 5.28 rebuild

* Mon Apr 23 2018 Petr Pisar <ppisar@redhat.com> - 4:2.98-4
- 2.98 bump

* Wed Feb 21 2018 Petr Pisar <ppisar@redhat.com> - 4:2.97-3
- 2.97 bump

* Mon Feb 19 2018 Petr Pisar <ppisar@redhat.com> - 4:2.96-2
- Preserve a warning on Perl 5.26.1 (bug #1544345)

* Mon Feb 12 2018 Petr Pisar <ppisar@redhat.com> - 4:2.96-1
- 2.96 bump

* Thu Feb 08 2018 Petr Pisar <ppisar@redhat.com> - 4:2.95-1
- 2.95 bump

* Tue Jan 09 2018 Petr Pisar <ppisar@redhat.com> - 4:2.94-16
- 2.94 bump

* Mon Oct 09 2017 Petr Pisar <ppisar@redhat.com> - 4:2.93-15
- 2.93 bump

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.92-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.92-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Petr Pisar <ppisar@redhat.com> - 4:2.92-12
- 2.92 bump

* Thu Jun 22 2017 Petr Pisar <ppisar@redhat.com> - 4:2.91-11
- 2.91 bump

* Thu Jun 22 2017 Petr Pisar <ppisar@redhat.com> - 4:2.90-10
- Fix "use parent q{Encode::Encoding}" (CPAN RT#122167)

* Mon Jun 12 2017 Petr Pisar <ppisar@redhat.com> - 4:2.90-9
- 2.90 bump

* Sat Jun 03 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.89-8
- Perl 5.26 rebuild

* Fri Apr 21 2017 Petr Pisar <ppisar@redhat.com> - 4:2.89-7
- 2.89 bump

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.88-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Petr Pisar <ppisar@redhat.com> - 4:2.88-5
- 2.88 bump

* Mon Oct 31 2016 Petr Pisar <ppisar@redhat.com> - 4:2.87-4
- 2.87 bump

* Fri Sep 30 2016 Petr Pisar <ppisar@redhat.com> - 4:2.86-3
- Fix Encode::encode_utf8(undef) to return undef (CPAN RT#116904)
- Refuse non-shortests UTF-8 representations in strict mode
- Fix panic when encoding undefined scalars

* Fri Sep 16 2016 Petr Pisar <ppisar@redhat.com> - 4:2.86-2
- Add Artistic 2.0 into license tag because of encguess tool

* Thu Aug 11 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.86-1
- 2.86 bump

* Tue Aug 09 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.85-1
- 2.85 bump

* Tue Aug 02 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.84-11
- Avoid loading optional modules from default . (CVE-2016-1238)

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4:2.84-10
- Increase epoch to favour standalone package

* Mon Apr 18 2016 Petr Pisar <ppisar@redhat.com> - 3:2.84-9
- Weak perl-Encode-devel dependency on perl-devel to Recommends level
  (bug #1129443)

* Mon Apr 11 2016 Petr Pisar <ppisar@redhat.com> - 3:2.84-8
- 2.84 bump

* Thu Mar 24 2016 Petr Pisar <ppisar@redhat.com> - 3:2.83-7
- 2.83 bump

* Tue Feb 09 2016 Petr Pisar <ppisar@redhat.com> - 3:2.82-6
- 2.82 bump

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3:2.80-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Petr Pisar <ppisar@redhat.com> - 3:2.80-4
- 2.80 bump

* Fri Jan 22 2016 Petr Pisar <ppisar@redhat.com> - 3:2.79-3
- 2.79 bump

* Thu Sep 24 2015 Petr Pisar <ppisar@redhat.com> - 3:2.78-2
- 2.78 bump

* Wed Sep 16 2015 Petr Pisar <ppisar@redhat.com> - 3:2.77-1
- 2.77 bump

* Fri Jul 31 2015 Petr Pisar <ppisar@redhat.com> - 3:2.76-2
- Increase release number to have unique perl-encoding NEVRA

* Fri Jul 31 2015 Petr Pisar <ppisar@redhat.com> - 3:2.76-1
- 2.76 bump

* Wed Jul 01 2015 Petr Pisar <ppisar@redhat.com> - 3:2.75-1
- 2.75 bump

* Thu Jun 25 2015 Petr Pisar <ppisar@redhat.com> - 3:2.74-1
- 2.74 bump

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3:2.73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.73-2
- Perl 5.22 rebuild
- Increase Epoch to favour standalone package

* Mon Apr 20 2015 Petr Pisar <ppisar@redhat.com> - 2:2.73-1
- 2.73 bump

* Mon Mar 16 2015 Petr Pisar <ppisar@redhat.com> - 2:2.72-1
- 2.72 bump

* Thu Mar 12 2015 Petr Pisar <ppisar@redhat.com> - 2:2.71-1
- 2.71 bump

* Wed Mar 04 2015 Petr Pisar <ppisar@redhat.com> - 2:2.70-2
- Correct license from (GPL+ or Artistic) to ((GPL+ or Artistic) and UCD)

* Thu Feb 05 2015 Petr Pisar <ppisar@redhat.com> - 2:2.70-1
- 2.70 bump

* Fri Jan 23 2015 Petr Pisar <ppisar@redhat.com> - 2:2.68-1
- 2.68 bump

* Fri Dec 05 2014 Petr Pisar <ppisar@redhat.com> - 2:2.67-1
- 2.67 bump

* Wed Dec 03 2014 Petr Pisar <ppisar@redhat.com> - 2:2.66-1
- 2.66 bump

* Tue Nov 18 2014 Petr Pisar <ppisar@redhat.com> - 2:2.64-2
- Consider Filter::Util::Call dependency as mandatory (bug #1165183)
- Sub-package encoding module

* Mon Nov 03 2014 Petr Pisar <ppisar@redhat.com> - 2:2.64-1
- 2.64 bump

* Mon Oct 20 2014 Petr Pisar <ppisar@redhat.com> - 2:2.63-1
- 2.63 bump

* Wed Sep 03 2014 Jitka Plesnikova <jplesnik@redhat.com> - 2:2.62-5
- Increase Epoch to favour standalone package

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.62-4
- Perl 5.20 rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Petr Pisar <ppisar@redhat.com> - 1:2.62-1
- 2.62 bump

* Wed Apr 30 2014 Petr Pisar <ppisar@redhat.com> - 1:2.60-1
- 2.60 bump

* Mon Apr 14 2014 Petr Pisar <ppisar@redhat.com> - 1:2.59-1
- 2.59 bump

* Mon Mar 31 2014 Petr Pisar <ppisar@redhat.com> - 1:2.58-1
- 2.58 bump

* Fri Jan 03 2014 Petr Pisar <ppisar@redhat.com> - 1:2.57-1
- 2.57 bump

* Mon Sep 16 2013 Petr Pisar <ppisar@redhat.com> - 1:2.55-1
- 2.55 bump

* Mon Sep 02 2013 Petr Pisar <ppisar@redhat.com> - 1:2.54-1
- 2.54 bump

* Wed Aug 21 2013 Jitka Plesnikova <jplesnik@redhat.com> - 1:2.52-1
- 2.52 bump

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.51-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-6
- Specify more dependencies

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-5
- Put epoch into dependecny declaration

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-4
- Link minimal build-root packages against libperl.so explicitly

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-3
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-2
- Perl 5.18 rebuild

* Fri Jul 12 2013 Petr Pisar <ppisar@redhat.com> - 1:2.51-1
- Increase epoch to compete with perl.spec

* Fri May 17 2013 Petr Pisar <ppisar@redhat.com> - 2.51-2
- Specify all dependencies

* Thu May 02 2013 Petr Pisar <ppisar@redhat.com> - 2.51-1
- 2.51 bump

* Mon Apr 29 2013 Petr Pisar <ppisar@redhat.com> - 2.50-1
- 2.50 bump (recoding does not launders taintedness)

* Tue Mar 05 2013 Petr Pisar <ppisar@redhat.com> - 2.49-1
- 2.49 bump

* Mon Feb 18 2013 Petr Pisar <ppisar@redhat.com> - 2.48-1
- 2.48 bump

* Thu Sep 20 2012 Petr Pisar <ppisar@redhat.com> 2.47-1
- Specfile autogenerated by cpanspec 1.78.
- Make devel sub-package architecture specific due to file location
