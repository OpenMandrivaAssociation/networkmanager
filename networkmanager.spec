%define	url_ver %(echo %{version}|cut -d. -f1,2)

%define	rname NetworkManager
%define	api 1.0

%define majglib 4
%define libnm_glib %mklibname nm-glib %{majglib}
%define girclient %mklibname	nmclient-gir %{api}
%define devnm_glib %mklibname -d nm-glib

%define majvpn 1
%define libnm_glib_vpn %mklibname nm-glib-vpn %{majvpn}
%define devnm_glib_vpn %mklibname -d nm-glib-vpn

%define majutil 2
%define libnm_util %mklibname nm-util %{majutil}
%define girname %mklibname	%{name}-gir %{api}
%define devnm_util %mklibname -d nm-util

%define	majlibnm	0
%define	libnm		%mklibname nm %{majlibnm}
%define	nm_girname	%mklibname nm-gir %{api}
%define	devnm		%mklibname -d nm
%define	ppp_version	2.4.7

Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	1.0.10
Release:	1
Group:		System/Base
License:	GPLv2+
Url:		http://www.gnome.org/projects/NetworkManager/
Source0:	https://download.gnome.org/sources/NetworkManager/%{url_ver}/%{rname}-%{version}.tar.xz
Source2:	00-server.conf

# Fedora patches
Patch2:		networkmanager-0.8.1.999-explain-dns1-dns2.patch
# Not upstream, from fedora
Patch3:        0001-rh1116999-resolv-conf-symlink.patch
# from arch
Patch4:        0001-Add-Requires.private-glib-2.0.patch

# OpenMandriva specific patches
Patch51:	networkmanager-0.9.8.4-add-systemd-alias.patch

BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	iptables
BuildRequires:	readline-devel
BuildRequires:	systemd-units
BuildRequires:	wpa_supplicant
BuildRequires:	libiw-devel
BuildRequires:	ppp-devel = %{ppp_version}
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	pkgconfig(libsystemd-login)
# Temporary while systemd package is missing req
BuildRequires:	libsystemd-devel
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(nss)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libndp)
BuildRequires:	pkgconfig(libnewt)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libteamdctl)
Requires:	dhcp-client-daemon
Requires:	dnsmasq-base
Requires:	iproute2
Requires:	iptables
Requires:	mobile-broadband-provider-info
Requires:	modemmanager
Requires:	ppp = %{ppp_version}
Requires(post,preun,postun):	rpm-helper
Requires:	wireless-tools
Requires:	wpa_supplicant >= 0.7.3-2
Suggests:	nscd
Provides:	NetworkManager = %{EVRD}
Obsoletes:	dhcdbd
Conflicts:	%{_lib}nm_util1 < 0.7.996
Conflicts:	initscripts < 9.24-5

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.

%package -n	%{libnm}
Summary:	Shared library for nm_util
Group:		System/Libraries

%description -n	%{libnm}
Shared library for nm.

%package -n %{nm_girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{nm_girname}
GObject Introspection interface description for NM.

%package -n	%{devnm}
Summary:	Development files for NM
Group:		Development/C
Provides:	nm-devel = %{EVRD}
Requires:	%{nm_girname} = %{EVRD}

%description -n	%{devnm}
Development files for NM.

%package -n	%{libnm_util}
Summary:	Shared library for nm_util
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-util 0}
%rename		%{_lib}nm_util1

%description -n	%{libnm_util}
Shared library for nm-util.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-util2 < 0.9.8.0-2

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package -n	%{devnm_util}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	nm-util-devel = %{EVRD}
Requires:	%{libnm_util} = %{EVRD}
Requires:	%{girname} = %{version}-%{release}
Obsoletes:	%{_lib}nm_util-devel < 0.7.996

%description -n	%{devnm_util}
Development files for nm-util.

%package -n	%{libnm_glib}
Summary:	Shared library for nm_glib
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-glib 0}

%description -n	%{libnm_glib}
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.

%package -n %{girclient}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib4 < 0.9.8.0-2

%description -n %{girclient}
GObject Introspection interface description for %{name}.

%package -n	%{devnm_glib}
Summary:	Development files for nm_glib
Group:		Development/C
Provides:	nm-glib-devel = %{EVRD}
Requires:	%{libnm_glib} = %{EVRD}
Requires:	%{girclient} = %{version}-%{release}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Obsoletes:	%{_lib}nm_glib-devel < 0.7.996

%description -n	%{devnm_glib}
Development files for nm-glib.

%package -n	%{libnm_glib_vpn}
Summary:	Shared library for nm-glib-vpn
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib1 < 0.7.996

%description -n	%{libnm_glib_vpn}
This package contains the libraries that make it easier to use some
NetworkManager VPN functionality from applications that use glib.

%package -n	%{devnm_glib_vpn}
Summary:	Development files for nm-glib-vpn
Group:		Development/C
Provides:	nm-glib-vpn-devel = %{EVRD}
Requires:	%{libnm_glib_vpn} = %{EVRD}
Conflicts:	%{_lib}nm_glib-devel < 0.7.996

%description -n	%{devnm_glib_vpn}
Development files for nm-glib-vpn.

%prep
%setup -qn %{rname}-%{version}
%apply_patches
autoreconf -fi
intltoolize -f

%build
%define	_disable_ld_no_undefined 1
%configure \
	--with-crypto=nss \
	--enable-more-warnings=no \
	--with-docs=yes \
	--with-system-ca-path=%{_sysconfdir}/pki/tls/certs \
	--with-resolvconf=no \
	--with-session-tracking=systemd \
	--with-suspend-resume=systemd \
	--with-systemdsystemunitdir=%{_systemunitdir} \
	--with-tests=yes \
	--with-dhcpcd=/sbin/dhcpcd \
	--with-dhclient=/sbin/dhclient \
	--with-iptables=/sbin/iptables \
	--enable-polkit \
	--enable-polkit-agent \
	--enable-ppp \
	--enable-concheck \
	--with-wext=yes \
	--enable-modify-system \
	--with-modem-manager-1=yes \
	--disable-vala \
	--with-udev-dir=/lib/udev \
	--with-system-libndp=yes \
	--with-nmtui \
	--enable-teamdctl \
	--enable-introspection=yes \
	--enable-bluez5-dun \
	--enable-lto \
	--enable-wifi \
	--with-pppd-plugin-dir=%{_libdir}/pppd/%{ppp_version} \
	--with-dist-version=%{version}-%{release}

%make

%install
%makeinstall_std

# ifcfg-mdv currently broken, so just use ifcfg-rh for now untill it gets fixed
cat > %{buildroot}%{_sysconfdir}/NetworkManager/NetworkManager.conf << EOF
[main]
plugins=ifcfg-rh,keyfile
EOF

# Create netprofile module 
install -d %{buildroot}%{_sysconfdir}/netprofile/modules/
cat > %{buildroot}%{_sysconfdir}/netprofile/modules/01_networkmanager << EOF
# netprofile module
#
# this module contains settings for saving/restore the NetworkManager configuration
# in different network profiles

NAME="networkmanager"
DESCRIPTION="Networkmanager connection settings"

# list of files to be saved by netprofile
FILES="/etc/NetworkManager/"

# list of services to be restarted by netprofile
SERVICES="networkmanager"
EOF
chmod  755 %{buildroot}%{_sysconfdir}/netprofile/modules/01_networkmanager

install -m644 -p %{SOURCE2} -D %{buildroot}%{_sysconfdir}/NetworkManager/conf.d/00-server.conf

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN

install -m755 clients/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online


# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

# create a dnsmasq.d directory
install -d $%{buildroot}%{_sysconfdir}/NetworkManager/dnsmasq.d

install -d $%{buildroot}%{_datadir}/gnome-vpn-properties

install -d $%{buildroot}%{_localstatedir}/lib/NetworkManager

#rhbz#974811
ln -sr %{buildroot}%{_unitdir}/NetworkManager-dispatcher.service %{buildroot}%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service

# (bor) clean up on uninstall
install -d %{buildroot}%{_localstatedir}/lib/%{rname}
pushd %{buildroot}%{_localstatedir}/lib/%{rname} && {
	touch %{rname}.state
	touch timestamps
popd
}

%find_lang %{rname}

%post

# bug 1395
# need to handle upgrade from minimal ifcfg files
# networkmanager < 0.9.10 treated a file with missing BOOTPROTO
# as BOOTPROTO=dhcp, later version treat it as IPV4 disabled
# so we add a BOOTPROTO to any ifcfg files without one
for x in /etc/sysconfig/network-scripts/ifcfg-*;
do
   if [ $(basename $x) != "ifcfg-lo" ]; then
       grep -q ^BOOTPROTO $x || echo BOOTPROTO=dhcp >> $x
   fi
done


%files -f %{rname}.lang
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-ifcfg-rh.conf
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/NetworkManager.conf
%config(noreplace) %{_sysconfdir}/netprofile/modules/01_networkmanager
%dir %{_sysconfdir}/%{rname}/conf.d
%config(noreplace) %{_sysconfdir}/%{rname}/conf.d/00-server.conf
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/system-connections
%dir %{_sysconfdir}/NetworkManager/VPN
%{_bindir}/nmcli
%{_bindir}/nmtui
%{_bindir}/nmtui-connect
%{_bindir}/nmtui-edit
%{_bindir}/nmtui-hostname
%{_bindir}/nm-online
%{_sbindir}/%{rname}
%{_libexecdir}/nm-avahi-autoipd.action
%{_libexecdir}/nm-dhcp-helper
%{_libexecdir}/nm-dispatcher
%{_libexecdir}/nm-iface-helper
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%attr(0755,root,root) %dir %{_localstatedir}/run/%{rname}
%dir %{_localstatedir}/lib/%{rname}
%ghost %{_localstatedir}/lib/%{rname}/*
%{_datadir}/bash-completion/completions/nmcli
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
/lib/udev/rules.d/*.rules
%{_systemunitdir}/NetworkManager-wait-online.service
%{_systemunitdir}/NetworkManager-dispatcher.service
%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service
%{_systemunitdir}/NetworkManager.service
%{_systemunitdir}/network-online.target.wants/NetworkManager-wait-online.service
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%{_datadir}/doc/NetworkManager/examples/server.conf

%files -n %{libnm}
%{_libdir}/libnm.so.%{majlibnm}*

%files -n %{nm_girname}
%{_libdir}/girepository-1.0/NM-%{api}.typelib

%files -n %{devnm}
%dir %{_includedir}/libnm
%{_includedir}/libnm/*.h
%doc %{_datadir}/gtk-doc/html/libnm
%{_datadir}/gir-1.0/NM-1.0.gir
%{_libdir}/pkgconfig/libnm.pc
%{_libdir}/libnm.so

%files -n %{libnm_util}
%{_libdir}/libnm-util.so.%{majutil}*

%files -n %{girname}
%{_libdir}/girepository-1.0/NetworkManager-%{api}.typelib

%files -n %{devnm_util}
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%doc %{_datadir}/gtk-doc/html/%{rname}
%doc %{_datadir}/gtk-doc/html/libnm-util
%{_datadir}/gir-1.0/NetworkManager-1.0.gir
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%{_libdir}/libnm-glib.so.%{majglib}*

%files -n %{girclient}
%{_libdir}/girepository-1.0/NMClient-%{api}.typelib

%files -n %{libnm_glib_vpn}
%{_libdir}/libnm-glib-vpn.so.%{majvpn}*

%files -n %{devnm_glib}
%dir %{_includedir}/libnm-glib
%exclude %{_includedir}/libnm-glib/nm-vpn*.h
%doc %{_datadir}/gtk-doc/html/libnm-glib
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/libnm-glib.so
%{_datadir}/gir-1.0/NMClient-1.0.gir

%files -n %{devnm_glib_vpn}
%{_includedir}/libnm-glib/nm-vpn*.h
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/libnm-glib-vpn.so

