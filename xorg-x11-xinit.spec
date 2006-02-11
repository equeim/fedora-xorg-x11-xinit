%define pkgname xinit

Summary: X.Org X11 X Window System xinit startup scripts
Name: xorg-x11-%{pkgname}
Version: 1.0.1
Release: 1.2
License: MIT/X11
Group: User Interface/X
URL: http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0: http://xorg.freedesktop.org/releases/X11R7.0-RC4/everything/%{pkgname}-%{version}.tar.bz2
Source10: xinitrc-common
Source11: xinitrc
Source12: Xclients
Source13: Xmodmap
Source14: Xresources
Source15: xinput.sh
# NOTE: Xsession is used by xdm/kdm/gdm and possibly others, so we keep it
#       here instead of the xdm package.
Source16: Xsession

BuildRequires: libX11-devel
# NOTE: startx needs xauth in order to run, but that is not picked up
#       automatically by rpm.  (Bug #173684)
Requires: xauth

# NOTE: xinit, startx moved to xorg-x11-xinit during the X.Org X11R7
# modularization.  These Conflicts lines ensure upgrades work smoothly.
Conflicts: XFree86, xorg-x11

# NOTE: Most of the xinitrc scripts/config files are now in xorg-x11-xinit,
# so the xinitrc package became unnecessary.  The xdm configs/scripts move
# to the xdm package.
Obsoletes: xinitrc

%description
X.Org X11 X Window System xinit startup scripts

%prep
%setup -q -n %{pkgname}-%{version}

%build
%configure
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
make XINITDIR=/etc/X11/xinit

%install
rm -rf $RPM_BUILD_ROOT
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
%makeinstall XINITDIR=$RPM_BUILD_ROOT/etc/X11/xinit

# Install Red Hat custom xinitrc, etc.
{
    for script in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE16} ; do
        install -m 755 $script $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/${script##*/}
    done

    install -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xmodmap
    install -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xresources

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
    install -m 755 %{SOURCE15} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/xinput.sh

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/Xclients.d
}

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
%{_sysconfdir}/X11/xinit/xinitrc
%{_sysconfdir}/X11/xinit/xinitrc-common
%config(noreplace) %{_sysconfdir}/X11/Xmodmap
%config(noreplace) %{_sysconfdir}/X11/Xresources
%dir %{_sysconfdir}/X11/xinit/Xclients.d
%{_sysconfdir}/X11/xinit/Xclients
%{_sysconfdir}/X11/xinit/Xsession
%dir %{_sysconfdir}/X11/xinit/xinitrc.d
%{_sysconfdir}/X11/xinit/xinitrc.d/*
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/startx.1x*
%{_mandir}/man1/xinit.1x*

%changelog
* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.1-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-1
- Updated to xinit 1.0.1 from X11R7.0

* Fri Dec 16 2005 Mike A. Harris <mharris@redhat.com> 1.0.0-1
- Updated to xinit 1.0.0 from X11R7 RC4.
- Changed manpage dir from man1x to man1 to match upstream default.

* Tue Nov 22 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-6
- Add "Requires: xauth" for startx, to fix bug (#173684)

* Mon Nov 14 2005 Jeremy Katz <katzj@redhat.com> 0.99.3-5
- Do not provide xinit anymore, gdm has been fixed and that breaks things
  with the obsoletes

* Sat Nov 12 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-4
- Added Xsession script from xinitrc, as it is very similar codebase, which
  shares "xinitrc-common" anyway, and all of the display managers use it.

* Fri Nov 11 2005 Mike A. Harris <mharris@redhat.com> 0.99.3-3
- Updated to xinit 0.99.3 from X11R7 RC2.

* Mon Nov 7 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added "Provides: xinitrc = 5.0.0-1" for temporary compatibility between
  monolithic and modular X.  This will be removed however for FC5.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Import custom Red Hat xinit scripts from xinitrc package.
- Obsolete xinitrc package, as we include the scripts/configs here now.
- Fix all scripts/configs to avoid the now obsolete /usr/X11R6 prefix.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to xinit 0.99.2 from X11R7 RC1.
- Change manpage location to 'man1x' in file manifest.

* Wed Oct  5 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag.
- Update BuildRequires to use new library package names.
- Tidy up spec file a bit.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
