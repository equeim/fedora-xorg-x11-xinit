%define pkgname xinit
# FIXME: Upstream version of xfs tarball is 0.99.0, which would require
# us to add an "Epoch: 1" to this package in order for rpm to upgrade from
# the FC4 (and earlier) monolithic xorg-x11-xfs-6.8.x rpm package.  Since
# it is currently unknown what the final upstream tarball version is likely
# to be called, I am avoiding adding Epoch, and instead using a 6.99.99.x
# version number for the time being.  This allows us to make sure xfs will
# upgrade from older releases to the new release, allows us to avoid adding
# an Epoch tag possibly unnecessarily - as Epoch is permanent and very evil.
# If upstream later names it "xfs-7.0", then we bump the version to that,
# and everything just works.
%define upstreamversion 0.99.0

Summary: X.Org X11 X Window System xinit startup scripts
Name: xorg-x11-%{pkgname}
Version: 0.99.0
Release: 1
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/X11R7.0-RC0/everything/%{pkgname}-%{upstreamversion}.tar.bz2
#Source10: mkxauth
#Source11: mkxauth.man
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires: xorg-x11-libX11-devel

# FIXME: monolithic twm packaging has a hard dep on xterm, which might still
# be required.  We'll have to examine the twm configuration files.
#Requires: xterm
#Provides: xauth
#Provides: mkxauth
#Obsoletes: XFree86-xauth, mkxauth
# NOTE: xauth moved from the XFree86 package to XFree86-xauth in
# XFree86-4.2.0-50.11, so this Conflicts line is required for upgrades
# from RHL 8 and older, and RHEL 2.1 to work properly when upgrading to
# a newer OS release.
# NOTE: xinit, startx moved to xorg-x11-xinit during the X.Org X11R7
# modularization.  These Conflicts lines ensure upgrades work smoothly.
Conflicts: XFree86, xorg-x11

%description
X.Org X11 X Window System xinit startup scripts

%prep
%setup -q -c %{name}-%{version}

%build
cd %{pkgname}-%{upstreamversion}
%configure
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
make XINITDIR=/etc/X11/xinit

%install
rm -rf $RPM_BUILD_ROOT
cd %{pkgname}-%{upstreamversion}
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
%makeinstall XINITDIR=$RPM_BUILD_ROOT/etc/X11/xinit
## Install mkxauth
#{
#   install -m 755 %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/
#   install -m 644 %{SOURCE11} $RPM_BUILD_ROOT%{_mandir}/man1/mkxauth.1
#}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc
%dir %{_bindir}
%{_bindir}/startx
%{_bindir}/xinit
%dir %{_sysconfdir}/X11
%dir %{_sysconfdir}/X11/xinit
# FIXME: We have to update the Xorg supplied xinitrc to the customized
# Red Hat version in 'xinitrc' package, along with other appropriate
# scripts.
%config %{_sysconfdir}/X11/xinit/xinitrc
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*

%changelog
* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
