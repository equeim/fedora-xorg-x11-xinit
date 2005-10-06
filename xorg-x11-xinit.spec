%define pkgname xinit
%define upstreamversion 0.99.0

Summary: X.Org X11 X Window System xinit startup scripts
Name: xorg-x11-%{pkgname}
Version: 0.99.0
Release: 2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
Source0: http://xorg.freedesktop.org/X11R7.0-RC0/everything/%{pkgname}-%{upstreamversion}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: libX11-devel

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
* Wed Oct  5 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag.
- Update BuildRequires to use new library package names.
- Tidy up spec file a bit.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
