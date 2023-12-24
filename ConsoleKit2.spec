Summary:	ConsoleKit2 - a framework for defining and tracking users, login sessions, and seats
Summary(pl.UTF-8):	ConsoleKit2 - szkielet do definiowania i śledzenia użytkowników, sesji logowania i stanowisk
Name:		ConsoleKit2
Version:	1.2.6
Release:	0.1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/ConsoleKit2/ConsoleKit2/releases
Source0:	https://github.com/ConsoleKit2/ConsoleKit2/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	9d43cdea3319e9d859f83ae613bacae1
Source1:	ConsoleKit.tmpfiles
URL:		https://github.com/ConsoleKit2/ConsoleKit2
BuildRequires:	acl-devel
BuildRequires:	autoconf >= 2.62
BuildRequires:	automake >= 1:1.9
BuildRequires:	cgmanager-devel
BuildRequires:	dbus-devel >= 0.82
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools >= 0.19
BuildRequires:	glib2-devel >= 1:2.40
# for <sys/inotify.h>
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	gobject-introspection-devel >= 1.30.0
BuildRequires:	gtk-doc >= 1.14
BuildRequires:	libdrm-devel >= 2.4.60
BuildRequires:	libevdev-devel >= 0.2
BuildRequires:	libselinux-devel >= 1.0
BuildRequires:	libtool >= 2:2
BuildRequires:	pam-devel >= 0.80
BuildRequires:	pkgconfig
BuildRequires:	polkit-devel >= 0.92
BuildRequires:	rpmbuild(macros) >= 1.626
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 1:190
BuildRequires:	xmlto
BuildRequires:	xorg-lib-libX11-devel >= 1.0.0
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-dirs = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus >= 0.82
Requires:	filesystem >= 3.0-25
Requires:	rc-scripts >= 0.4.3.0
Requires:	systemd-units >= 38
Provides:	udev-acl = 1:182-1
Obsoletes:	ConsoleKit
Obsoletes:	ConsoleKit-systemd
Obsoletes:	udev-acl < 1:182
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ConsoleKit2 is a framework for defining and tracking users, login
sessions, and seats. It allows multiple users to be logged in at the
same time and share hardware for their graphical session. ConsoleKit2
will keep track of those resources and whichever session is active
will have use of the hardware at that time.

%description -l pl.UTF-8
ConsoleKit to szkielet do definiowania i śledzenia użytkowników, sesji
logowania i stanowisk. Pozwala na jednoczesne logowanie wielu
użytkowników i współdzielenie sprzętu do sesji graficznej. ConsoleKit2
śledzi zasoby, i w zależności od tego, która sesja jest aktywna,
pozwala jej na używanie sprzętu w tym czasie.

%package libs
Summary:	ConsoleKit library
Summary(pl.UTF-8):	Biblioteka ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Requires:	dbus-libs >= 0.82
Requires:	glib2 >= 1:2.40
Obsoletes:	ConsoleKit-libs

%description libs
ConsoleKit library.

%description libs -l pl.UTF-8
Biblioteka ConsoleKit.

%package dirs
Summary:	ConsoleKit directories
Summary(pl.UTF-8):	Katalogi ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Libraries
Obsoletes:	ConsoleKit-dirs

%description dirs
ConsoleKit directories.

%description dirs -l pl.UTF-8
Katalogi ConsoleKit.

%package devel
Summary:	Header files for ConsoleKit
Summary(pl.UTF-8):	Pliki nagłówkowe ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	dbus-devel >= 0.82

%description devel
Header files for ConsoleKit.

%description devel -l pl.UTF-8
Pliki nagłówkowe ConsoleKit.

%package static
Summary:	Static ConsoleKit library
Summary(pl.UTF-8):	Statyczna biblioteka ConsoleKit
License:	AFL v2.1 or GPL v2
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ConsoleKit library.

%description static -l pl.UTF-8
Statyczna biblioteka ConsoleKit.

%package x11
Summary:	X11 session support for ConsoleKit
Summary(pl.UTF-8):	Obsługa sesji X11 dla pakietu ConsoleKit
License:	GPL v2+
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}
Requires:	xorg-lib-libX11 >= 1.0.0
Obsoletes:	ConsoleKit-x11

%description x11
X11 session support utilities for ConsoleKit.

%description x11 -l pl.UTF-8
Narzędzia obsługujące sesje X11 dla pakietu ConsoleKit.

%prep
%setup -q

%build
%{__gtkdocize}
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-silent-rules \
	--enable-docbook-docs \
	--enable-pam-module \
	--enable-static \
	--enable-udev-acl \
	--with-pam-module-dir=/%{_lib}/security \
	--with-pid-file=%{_localstatedir}/run/console-kit-daemon.pid \
	--with-systemdsystemunitdir=%{systemdunitdir} \

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{systemdtmpfilesdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{systemdtmpfilesdir}/%{name}.conf

%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib*.la
%{__rm} $RPM_BUILD_ROOT/%{_lib}/security/*.{a,la}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

# use triggerun not triggerpostun - old init script is needed to stop service
%triggerun -- ConsoleKit < 0.2.4
%service -q ConsoleKit stop
/sbin/chkconfig --del ConsoleKit

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post
%systemd_post console-kit-daemon.service

%preun
%systemd_preun console-kit-daemon.service

%postun
%systemd_reload

%triggerpostun -- ConsoleKit < 0.4.5-9
%systemd_trigger console-kit-daemon.service

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO
%attr(755,root,root) %{_bindir}/ck-history
%attr(755,root,root) %{_bindir}/ck-launch-session
%attr(755,root,root) %{_bindir}/ck-list-sessions
%attr(755,root,root) %{_sbindir}/ck-log-system-restart
%attr(755,root,root) %{_sbindir}/ck-log-system-start
%attr(755,root,root) %{_sbindir}/ck-log-system-stop
%attr(755,root,root) %{_sbindir}/console-kit-daemon
%{_mandir}/man1/ck-history.1*
%{_mandir}/man1/ck-launch-session.1*
%{_mandir}/man1/ck-list-sessions.1*
%{_mandir}/man1/console-kit-daemon.1m*
%attr(755,root,root) %{_libexecdir}/ck-collect-session-info
%attr(755,root,root) %{_libexecdir}/ck-remove-directory
%attr(755,root,root) %{_libdir}/ConsoleKit/scripts/*
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_datadir}/polkit-1/actions/org.freedesktop.consolekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ConsoleKit.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Seat.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Session.xml
/etc/dbus-1/system.d/ConsoleKit.conf
/etc/X11/xinit/xinitrc.d/90-consolekit
%config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/consolekit
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_mandir}/man8/pam_ck_connector.8*
%{systemdunitdir}/basic.target.wants/console-kit-log-system-start.service
%{systemdunitdir}/console-kit-daemon.service
%{systemdunitdir}/console-kit-log-system-restart.service
%{systemdunitdir}/console-kit-log-system-start.service
%{systemdunitdir}/console-kit-log-system-stop.service
%{systemdunitdir}/halt.target.wants/console-kit-log-system-stop.service
%{systemdunitdir}/kexec.target.wants/console-kit-log-system-restart.service
%{systemdunitdir}/poweroff.target.wants/console-kit-log-system-stop.service
%{systemdunitdir}/reboot.target.wants/console-kit-log-system-restart.service

%attr(755,root,root) /lib/udev/udev-acl
%attr(755,root,root) %{_libexecdir}/udev-acl
%attr(755,root,root) %{_libdir}/ConsoleKit/run-seat.d/udev-acl.ck
/lib/udev/rules.d/70-udev-acl.rules
/lib/udev/rules.d/71-udev-seat.rules

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libck-connector.so.0
%attr(755,root,root) %{_libdir}/libconsolekit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libconsolekit.so.1
%{_libdir}/girepository-1.0/libconsolekit-1.0.typelib

%files dirs
%defattr(644,root,root,755)
%{systemdtmpfilesdir}/%{name}.conf
%dir %{_sysconfdir}/ConsoleKit
#%dir %{_sysconfdir}/ConsoleKit/run-session.d
#%dir %{_sysconfdir}/ConsoleKit/run-seat.d
%dir %{_sysconfdir}/ConsoleKit/seats.d
%dir %{_libdir}/ConsoleKit
%dir %{_libdir}/ConsoleKit/run-session.d
%dir %{_libdir}/ConsoleKit/run-seat.d
%dir %{_libdir}/ConsoleKit/scripts
%dir %{_localstatedir}/run/ConsoleKit
%dir %{_localstatedir}/log/ConsoleKit

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so
%attr(755,root,root) %{_libdir}/libconsolekit.so
%dir %{_includedir}/ConsoleKit
%{_includedir}/ConsoleKit/ck-connector
%{_includedir}/ConsoleKit/libconsolekit.h
%{_includedir}/ConsoleKit/sd-login.h
%{_datadir}/gir-1.0/libconsolekit-1.0.gir
%{_pkgconfigdir}/ck-connector.pc
%{_pkgconfigdir}/libconsolekit.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libck-connector.a
%{_libdir}/libconsolekit.a

%files x11
%defattr(644,root,root,755)
%attr(755,root,root) %{_libexecdir}/ck-get-x11-server-pid
%attr(755,root,root) %{_libexecdir}/ck-get-x11-display-device
