%define pkgname xinit

Summary:   X.Org X11 X Window System xinit startup scripts
Name:      xorg-x11-%{pkgname}
Version:   1.0.7
Release:   4%{?dist}
License:   MIT/X11
Group:     User Interface/X
URL:       http://www.x.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Source0:  ftp://ftp.x.org/pub/individual/app/%{pkgname}-%{version}.tar.bz2
Source10: xinitrc-common
Source11: xinitrc
Source12: Xclients
Source13: Xmodmap
Source14: Xresources
# NOTE: Xsession is used by xdm/kdm/gdm and possibly others, so we keep it
#       here instead of the xdm package.
Source16: Xsession
Source17: localuser.sh
Source100: ck-xinit-session.c

Patch1: xinit-1.0.2-client-session.patch
Patch2: xinit-1.0.7-poke-ck.patch
Patch3: xinit-1.0.7-unset.patch

BuildRequires: pkgconfig
BuildRequires: libX11-devel
BuildRequires: ConsoleKit-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: xorg-x11-util-macros
# NOTE: startx needs xauth in order to run, but that is not picked up
#       automatically by rpm.  (Bug #173684)
Requires: xauth
# next two are for localuser.sh
Requires: coreutils
Requires: xorg-x11-server-utils
Requires: ConsoleKit-x11
Requires: ConsoleKit-libs

# NOTE: Most of the xinitrc scripts/config files are now in xorg-x11-xinit,
# so the xinitrc package became unnecessary.  The xdm configs/scripts move
# to the xdm package.
Obsoletes: xinitrc

# We don't explicitly run dbus-launch anymore.  We depend on a dbus new enough
# that it installs its own .sh file in xinitrc.d to launch itself at session
# startup.
Conflicts: dbus < 1.1.4-3.fc9

%description
X.Org X11 X Window System xinit startup scripts

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1 -b .client-session
#%patch2 -p1 -b .poke-ck
%patch3 -p1 -b .unset

%build
autoreconf
%configure
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
make XINITDIR=/etc/X11/xinit
%{__cc} -o ck-xinit-session \
	`pkg-config --cflags ck-connector` $RPM_OPT_FLAGS \
	$RPM_SOURCE_DIR/ck-xinit-session.c \
	`pkg-config --libs ck-connector`

%install
rm -rf $RPM_BUILD_ROOT
# FIXME: Upstream should default to XINITDIR being this.  Make a patch to
# Makefile.am and submit it in a bug report or check into CVS.
%makeinstall XINITDIR=$RPM_BUILD_ROOT/etc/X11/xinit
install -m755 ck-xinit-session $RPM_BUILD_ROOT/%{_bindir}

# Install Red Hat custom xinitrc, etc.
{
    for script in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE16} ; do
        install -m 755 $script $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/${script##*/}
    done

    install -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xmodmap
    install -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xresources

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
    install -m 755 %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/localuser.sh

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/Xclients.d
}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING README NEWS ChangeLog
%{_bindir}/startx
%{_bindir}/xinit
%{_bindir}/ck-xinit-session
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
#%dir %{_mandir}/man1
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*

%changelog
* Mon Feb 11 2008 Adam Jackson <ajax@redhat.com> 1.0.7-4
- xinit-1.0.7-unset.patch: Unset various session-related environment
  variables at the top of startx. (#431899)

* Mon Feb  4 2008 Ray Strode <rstrode@redhat.com> 1.0.7-3
- don't special case dbus-launch. dbus-x11 now installs
  a script into /etc/X11/xinit/xinitrc.d.
- Drop the weird grep rule for extensions ending in .sh
  when sourcing /etc/X11/xinit/xinitrc.d

* Fri Oct 12 2007 Nalin Dahyabhai <nalin@redhat.com> 1.0.7-2
- Try opening the console-kit session after the user's UID has already
  been granted access to the server by localuser.sh, so that console-kit-daemon
  can connect and ask the server for information just by having switch to the
  user's UID (#287941).

* Mon Sep 24 2007 Adam Jackson <ajax@redhat.com> 1.0.7-1
- xinit 1.0.7

* Tue Aug 21 2007 Adam Jackson <ajax@redhat.com> - 1.0.2-27
- Rebuild for build id

* Mon Aug 6 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-26
- Bump release

* Mon Aug 6 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-25
- Fix typo: s/unask/umask/ - Bug 250882, Jan ONDREJ (ondrejj@salstar.sk)

* Thu Aug 2 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-24
- Fix bug 212167, CVE-2006-5214

* Sun Jul 29 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-23
- Fix Xsession to run the login shell inside the setgid ssh-agent, rather
  than the other way around. This preserves LD_LIBRARY_PRELOAD.
	Patch from Stefan Becker, bug 164869.

* Fri Jul 27 2007 Soren Sandmann <sandmann@redhat.com> 1.0.2-22
- Remove xinput.sh. Bug 244963.

* Mon May 21 2007 Adam Jackson <ajax@redhat.com> 1.0.2-21
- localuser.sh: Run silently.

* Sat Apr 22 2007 Matthias Clasen <mclasen@redhat.com> 1.0.2-20
- Don't install INSTALL

* Thu Apr 19 2007 Warren Togami <wtogami@redhat.com> 1.0.2-19
- disable SCIM by default in non-Asian languages #237054
  If you want to use SCIM, use im-chooser to enable it.

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-18
- Man pages are now in section 1, not in section 1x

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-17
- Also BR xorg-x11-util-macros since we autoreconf

* Mon Apr 02 2007 David Zeuthen <davidz@redhat.com> 1.0.2-16
- Add ConsoleKit support (#233183)

* Mon Nov 27 2006 Adam Jackson <ajax@redhat.com> 1.0.2-15
- Bump EVR to fix 6 to 7 updates.

* Fri Nov 10 2006 Ray Strode <rstrode@redhat.com> - 1.0.2-14
- start client in its own session with no controlling tty
  (bug 214649)

* Mon Oct 23 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-13
- Update Xsession to not use switchdesk for the hard coded kde and twm
  cases.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.2-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-11.fc6
- Bump and rebuild.

* Mon Sep 25 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-10.fc6
- Move hardcoded xsetroot background color to fallback cases (#205901).

* Thu Aug 17 2006 Kristian Høgsberg <krh@redhat.com> - 1.0.2-9.fc6
- Start ssh-agent for startx also (#169259).

* Sat Jul 22 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-8.fc6
- Fix SourceN line for localuser.sh to not collide.

* Fri Jul 21 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-7.fc6
- Added localuser.sh.

* Wed Jul 19 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-6.fc6
- Added fix to Xclients script, based on patch from bug (#190799)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 1.0.2-5.1.fc6
- rebuild

* Wed Jul 05 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-5.fc6
- Implemented changes to xinput.sh based on suggestions from (#194458)

* Wed Jun 21 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-4
- Added documentation to doc macro.

* Tue Jun 20 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-3
- Added xinit-1.0.2-setuid.diff to fix potential security issue (#196094)

* Tue Jun 06 2006 Mike A. Harris <mharris@redhat.com> 1.0.2-2
- Added "BuildRequires: pkgconfig" for bug (#194187)

* Thu Apr 27 2006 Adam Jackson <ajackson@redhat.com> 1.0.2-1
- Update xinit to 1.0.2

* Thu Feb 16 2006 Mike A. Harris <mharris@redhat.com> 1.0.1-2
- Change Conflicts to Obsoletes for xorg-x11 and XFree86 (#181414)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> 1.0.1-1.1
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

* Mon Nov 07 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-3
- Added "Provides: xinitrc = 5.0.0-1" for temporary compatibility between
  monolithic and modular X.  This will be removed however for FC5.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-2
- Import custom Red Hat xinit scripts from xinitrc package.
- Obsolete xinitrc package, as we include the scripts/configs here now.
- Fix all scripts/configs to avoid the now obsolete /usr/X11R6 prefix.

* Mon Oct 31 2005 Mike A. Harris <mharris@redhat.com> 0.99.2-1
- Updated to xinit 0.99.2 from X11R7 RC1.
- Change manpage location to 'man1x' in file manifest.

* Wed Oct 05 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-2
- Use Fedora-Extras style BuildRoot tag.
- Update BuildRequires to use new library package names.
- Tidy up spec file a bit.

* Wed Aug 24 2005 Mike A. Harris <mharris@redhat.com> 0.99.0-1
- Initial build.
