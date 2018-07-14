%global pkgname xinit

Summary:    X.Org X11 X Window System xinit startup scripts
Name:       xorg-x11-%{pkgname}
Version:    1.4.0
Release:    2%{?dist}
License:    MIT
URL:        https://www.x.org

Source0:    https://xorg.freedesktop.org/archive/individual/app/%{pkgname}-%{version}.tar.bz2
Source10:   xinitrc-common
Source11:   xinitrc
Source12:   Xclients
Source13:   Xmodmap
Source14:   Xresources
# NOTE: Xsession is used by xdm/kdm/gdm and possibly others, so we keep it
#       here instead of the xdm package.
Source16:   Xsession
Source17:   localuser.sh
Source18:   xinit-compat.desktop
Source19:   xinit-compat

# Fedora specific patches
Patch1: xinit-1.0.2-client-session.patch
Patch5: 0003-startx-Make-startx-auto-display-select-work-with-per.patch
# Fedora specific patch to match the similar patch in the xserver
Patch6: xinit-1.3.4-set-XORG_RUN_AS_USER_OK.patch

BuildRequires:  automake gcc
BuildRequires:  pkgconfig(x11)
BuildRequires:  dbus-devel

# NOTE: startx needs xauth in order to run, but that is not picked up
#       automatically by rpm.  (Bug #173684)
Requires:   xorg-x11-xauth
# next two are for localuser.sh
Requires:   coreutils
Requires:   xhost

Provides:   %{pkgname} = %{version}

%description
X.Org X11 X Window System xinit startup scripts.

%package session
Summary:    Display manager support for ~/.xsession and ~/.Xclients

%description session
Allows legacy ~/.xsession and ~/.Xclients files to be used from display
managers.

%prep
%setup -q -n %{pkgname}-%{version}
%patch1 -p1
%patch5 -p1
%patch6 -p1

%build
%configure
make %{?_smp_mflags}

%install
%make_install
install -p -m644 -D %{SOURCE18} $RPM_BUILD_ROOT%{_datadir}/xsessions/xinit-compat.desktop

# Install Red Hat custom xinitrc, etc.
{
    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit

    install -p -m 644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc-common

    for script in %{SOURCE11} %{SOURCE12} %{SOURCE16} ; do
        install -p -m 755 $script $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/${script##*/}
    done

    install -p -m 644 %{SOURCE13} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xmodmap
    install -p -m 644 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/X11/Xresources

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d
    install -p -m 755 %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/xinitrc.d/localuser.sh

    mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/X11/xinit/Xclients.d

    mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
    install -p -m 755 %{SOURCE19} $RPM_BUILD_ROOT%{_libexecdir}
}

%files
%doc COPYING README ChangeLog
%{_bindir}/startx
%{_bindir}/xinit
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
%{_mandir}/man1/startx.1*
%{_mandir}/man1/xinit.1*

%files session
%{_libexecdir}/xinit-compat
%{_datadir}/xsessions/xinit-compat.desktop

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Adam Jackson <ajax@redhat.com> - 1.4.0-1
- xinit 1.4.0

* Mon Feb 19 2018 Peter Hutterer <peter.hutterer@redhat.com> 1.3.4-18
- Add BR for automake and gcc

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Hans de Goede <hdegoede@redhat.com> - 1.3.4-13
- Check for all 3 of SSH_AGENT, SSH_AGENT_PID and SSH_AUTH_SOCK to fix
  a regression introduced by the previous fix (rhbz#1352339)

* Mon Aug 29 2016 Hans de Goede <hdegoede@redhat.com> - 1.3.4-12
- Drop 0001-startx-Pass-nolisten-tcp-by-default.patch this is the
  server default now
- Check for SSH_AUTH_SOCK not SSH_AGENT in xinitrc-common (rhbz#1352339)

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Peter Hutterer <peter.hutterer@redhat.com>
- s/define/global/

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.4-9
- Fix typo in Xsession file (rhbz#1222299)

* Thu Apr 30 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.4-8
- Only set XORG_RUN_AS_USER_OK when no vt is specified (#1203780)

* Fri Mar 20 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.4-7
- Fix startx auto display select not working when a Xserver started by
  gdm is running

* Wed Mar 18 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.4-6
- Set XORG_RUN_AS_USER_OK when starting X on the current tty, to run X
  to run without root rights when possible

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.3.4-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Tue Feb  3 2015 Hans de Goede <hdegoede@redhat.com> - 1.3.4-4
- xinitrc-common: Do not override SSH_AGENT if already set (rhbz#1067676)

* Thu Jan 22 2015 Simone Caronni <negativo17@gmail.com> - 1.3.4-3
- Xorg without root rights breaks by streams redirection (#1177513).
- Format SPEC file; trim changelog.

* Wed Oct  1 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.4-2
- Add support for MATE to Xclients (#1147905)

* Thu Sep 11 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.4-1
- New upstream release 1.3.4
- Resolves #806491 #990213 #1006029
- Remove stale ck-xinit-session references from xinitrc-common (#910969)
- Make startx pass "-nolisten tcp" by default, use -listen as server
  option to disable this (#1111684)
- Teach Xclients script about lxde (#488602)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 25 2014 Hans de Goede <hdegoede@redhat.com> - 1.3.2-11
- Fix startx ignoring a server or display passed on the cmdline (#960955)
- Drop Fedora custom patch to unset XDG_SESSION_COOKIE, this was only for CK

* Thu Jan 23 2014 Dave Airlie <airlied@redhat.com> 1.3.2-10
- fix for ppc64le enable (#1056742)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 01 2012 Kevin Fenzi <kevin@scrye.com> 1.3.2-7
- Add patch to not switch tty's, so systemd-logind works right with startx. 
- Partially Fixes bug #806491 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 26 2012 Adam Jackson <ajax@redhat.com> 1.3.2-5
- xinit 1.3.2

* Thu Mar 08 2012 Adam Jackson <ajax@redhat.com> 1.3.1-5
- Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 16 2011 Adam Jackson <ajax@redhat.com> 1.3.1-2
- Drop ConsoleKit integration, being removed in F17

* Mon Jul 25 2011 Matěj Cepl <mcepl@redhat.com> - 1.3.1-1
- New upstream version. Patches updated.

* Sat May 28 2011 Matěj Cepl <mcepl@redhat.com> - 1.0.9-21
- xinitrc-common sources ~/.profile (Bug 551508)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
