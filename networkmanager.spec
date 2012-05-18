%define	major_glib	4
%define major_glib_vpn	1
%define major_util	2
%define libnm_glib		%mklibname nm-glib %{major_glib}
%define libnm_glib_devel	%mklibname -d nm-glib
%define libnm_glib_vpn		%mklibname nm-glib-vpn %{major_glib_vpn}
%define libnm_glib_vpn_devel	%mklibname -d nm-glib-vpn
%define libnm_util		%mklibname nm-util %{major_util}
%define libnm_util_devel	%mklibname -d nm-util

#define snapshot 0

%define	rname	NetworkManager
Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	0.9.4.0
Release:	%{?snapshot:0.%{snapshot}.}6
Group:		System/Base
License:	GPLv2+
URL:		http://www.gnome.org/projects/NetworkManager/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/NetworkManager/0.9/%{rname}-%{version}%{?snapshot:.%{snapshot}}.tar.xz
Source1:	README.urpmi
# XXX: repository MIA?? patch manually regenerated...
# This patch is build from GIT at git://git.mandriva.com/projects/networkmanager.git
# DO NOT CHANGE IT MANUALLY.
# To generate patch use
#	git diff master..mdv
# Current mdv tip: 2e93ff7
Patch1:		networkmanager-0.9.4.0-mdv.patch
# Fedora patches
Patch2:		networkmanager-0.8.1.999-explain-dns1-dns2.patch
# Mandriva specific patches
Patch50:	networkmanager-0.9.2.0-systemd-start-after-resolvconf.patch
Patch51:	networkmanager-0.9.4.0-add-systemd-alias.patch
# fixed Patch52:	networkmanager-fix-includes.patch
Patch54:	NetworkManager-0.9.3.995-add-missing-linkage.patch
Patch55:	networkmanager-0.9.4.0-format_not_a_string_literal.patch
Patch56:	networkmanager-0.9.4.0-ensure-bindings-created-NMClient-object-work.patch
Patch57:	networkmanager-0.9.4.0-initialize-NMRemoteSettings-in-nm_remote_settings_new.patch
Patch59:	nm-polkit-permissive.patch
Patch60:	networkmanager-0.9.4.0-mdv-nscd-systemd.patch
Patch61:	networkmanager-0.9.4.0-cl-fix-nm-nocheck-con-up.patch



# upstream patches
# (fhimpe) Make it use correct location for dhclient lease files
BuildRequires:	pkgconfig(libnl-1)
BuildRequires:	wpa_supplicant
BuildRequires:	libiw-devel
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(nss) intltool
BuildRequires:	gtk-doc pkgconfig(ext2fs)
BuildRequires:	ppp-devel
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(gudev-1.0)
#BuildRequires:	dhcp-client
BuildRequires:	iptables
BuildRequires:	pkgconfig(gobject-introspection-1.0)
# (bor) for systemd support, pkg-config; move to systemd?
BuildRequires:	systemd-units
BuildRequires:	pkgconfig(libsystemd-login)
BuildRequires:	pkgconfig(libsoup-2.4)
Requires(post):	systemd-units rpm-helper
Requires(preun):systemd-units rpm-helper
Requires(postun):systemd-units
Requires:	wpa_supplicant >= 0.7.3-2
Requires:	wireless-tools
Requires:	dhcp-client
Requires:	mobile-broadband-provider-info
Requires:	modemmanager
Requires:	dhcp-client
Requires:	dnsmasq-base
Requires:	ppp = %(rpm -q --queryformat "%{VERSION}" ppp )
Requires:	iproute2
Requires:	iptables
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

%package -n	%{libnm_util}
Summary:	Shared library for nm_util
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-util 0}
%rename		%{_lib}nm_util1

%description -n %{libnm_util}
Shared library for nm-util.

%package -n	%{libnm_util_devel}
Summary:	Development files for nm_util
Group:		Development/C
Obsoletes:	%{mklibname networkmanager-util 0 -d}
Provides:	nm-util-devel = %{EVRD}
Requires:	%{libnm_util} = %{EVRD}
Obsoletes:	%{_lib}nm_util-devel < 0.7.996

%description -n %{libnm_util_devel}
Development files for nm-util.

%package -n	%{libnm_glib}
Summary:	Shared library for nm_glib
Group:		System/Libraries
Obsoletes:	%{mklibname networkmanager-glib 0}

%description -n	%{libnm_glib}
This package contains the libraries that make it easier to use some
NetworkManager functionality from applications that use glib.

%package -n	%{libnm_glib_devel}
Summary:	Development files for nm_glib
Group:		Development/C
Provides:	nm-glib-devel = %{EVRD}
Obsoletes:	%{mklibname networkmanager-glib 0 -d}
Requires:	%{libnm_glib} = %{EVRD}
Obsoletes:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{libnm_glib_devel}
Development files for nm-glib.

%package -n	%{libnm_glib_vpn}
Summary:	Shared library for nm-glib-vpn
Group:		System/Libraries
Conflicts:	%{_lib}nm-glib1 < 0.7.996

%description -n	%{libnm_glib_vpn}
This package contains the libraries that make it easier to use some
NetworkManager VPN functionality from applications that use glib.

%package -n	%{libnm_glib_vpn_devel}
Summary:	Development files for nm-glib-vpn
Group:		Development/C
Provides:	nm-glib-vpn-devel = %{EVRD}
Requires:	%{libnm_glib_vpn} = %{EVRD}
Conflicts:	%{_lib}nm_glib-devel < 0.7.996

%description -n %{libnm_glib_vpn_devel}
Development files for nm-glib-vpn.

%prep
%setup -q -n %{rname}-%{version}
%patch1 -p1 -b .mdv~
%patch2 -p1 -b .explain-dns1-dns2~
%patch50 -p1 -b .after-resolvconf~
%patch51 -p1 -b .systemd-alias~
%patch54 -p1 -b .link~
#patch55 -p1 -b .str~
#patch56 -p1 -b .rhbz802536~
#patch57 -p1 -b .rhbz#806664~
#patch58 -p1 -b .nscd_poke~
%patch59 -p1 -b .permissive~
%patch60 -p1 -b .nscd_mdv~
%patch61 -p1 -b .nocheck~
autoreconf -f

%build
%configure2_5x	--disable-static \
		--disable-rpath \
		--with-distro=mandriva \
		--with-crypto=nss \
		--enable-more-warnings=no \
		--with-docs=yes \
		--with-system-ca-path=%{_sysconfdir}/pki/tls/certs \
		--with-resolvconf=yes \
		--with-session-tracking=systemd \
		--with-systemdsystemunitdir=%{_systemunitdir} \
		--with-tests=yes \
		--with-dhcpcd=/sbin/dhcpcd \
		--with-dhclient=/sbin/dhclient \
		--with-iptables=/sbin/iptables \
		--with-resolvconf=/sbin/resolvconf \
		--enable-polkit \
		--enable-ppp \
		--enable-concheck \
		--with-wext=yes \
		--enable-polkit

%make

%install
%makeinstall_std

cat > %{buildroot}%{_sysconfdir}/NetworkManager/NetworkManager.conf << EOF
[main]
plugins=ifcfg-mdv,keyfile
EOF

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN
install -m755 test/.libs/nm-online -D %{buildroot}%{_bindir}/nm-online

# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

# Add readme displayed by urpmi
cp %{SOURCE1} .

# link service file to match alias
ln -sf %{_systemunitdir}/%{rname}.service %{buildroot}%{_systemunitdir}/%{name}.service

# (bor) clean up on uninstall
install -d %{buildroot}%{_localstatedir}/lib/%{rname}
pushd %{buildroot}%{_localstatedir}/lib/%{rname} && {
	touch %{rname}.state
	touch timestamps
popd
}

%find_lang %{rname}

find %{buildroot} -name \*.la|xargs rm -f


%post
%_post_service %{rname} %{rname}.service 

%preun
%_preun_service %{rname} %{rname}.service

%postun
%_postun_unit %{rname}.service 

%files -f %{rname}.lang
%doc AUTHORS CONTRIBUTING ChangeLog NEWS README TODO
%doc README.urpmi
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_sysconfdir}/dbus-1/system.d/nm-avahi-autoipd.conf
%{_sysconfdir}/dbus-1/system.d/nm-dhcp-client.conf
%{_sysconfdir}/dbus-1/system.d/nm-dispatcher.conf
%{_sysconfdir}/dbus-1/system.d/nm-ifcfg-rh.conf
%{_initrddir}/%{name}
#%{_initrddir}/%{rname}dispatcher
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/NetworkManager.conf
%{_sbindir}/%{rname}
#%{_sbindir}/%{rname}Dispatcher
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/system-connections
%dir %{_sysconfdir}/NetworkManager/VPN
%{_bindir}/nmcli
%{_bindir}/nm-tool
%{_bindir}/nm-online
%{_libdir}/nm-dispatcher.action
%{_libexecdir}/nm-dhcp-client.action
%{_libexecdir}/nm-avahi-autoipd.action
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_mandir}/man8/*.8*
%dir %{_libdir}/NetworkManager
%{_libdir}/NetworkManager/*.so
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%dir %{_localstatedir}/run/%{rname}
%dir %{_localstatedir}/lib/%{rname}
%ghost %{_localstatedir}/lib/%{rname}/*
%{_libexecdir}/nm-crash-logger
%dir %{_datadir}/%{rname}
%{_datadir}/%{rname}/gdb-cmd
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
%{_datadir}/gtk-doc/html/*
/lib/udev/rules.d/*.rules
%{_systemunitdir}/NetworkManager-wait-online.service
%{_systemunitdir}/NetworkManager.service
%{_systemunitdir}/networkmanager.service
%{_datadir}/dbus-1/system-services/org.freedesktop.NetworkManager.service

%files -n %{libnm_util}
%{_libdir}/libnm-util.so.%{major_util}*
%{_libdir}/girepository-1.0/NetworkManager-1.0.typelib

%files -n %{libnm_util_devel}
%dir %{_includedir}/%{rname}
%{_includedir}/%{rname}/*.h
%{_libdir}/pkgconfig/%{rname}.pc
%{_libdir}/pkgconfig/libnm-util.pc
%{_libdir}/libnm-util.so

%files -n %{libnm_glib}
%{_libdir}/libnm-glib.so.%{major_glib}*
%{_libdir}/girepository-1.0/NMClient-1.0.typelib

%files -n %{libnm_glib_vpn}
%{_libdir}/libnm-glib-vpn.so.%{major_glib_vpn}*

%files -n %{libnm_glib_devel}
%dir %{_includedir}/libnm-glib
%exclude %{_includedir}/libnm-glib/nm-vpn*.h
%{_includedir}/libnm-glib/*.h
%{_libdir}/pkgconfig/libnm-glib.pc
%{_libdir}/libnm-glib.so
%{_datadir}/gir-1.0/NMClient-1.0.gir
%{_datadir}/gir-1.0/NetworkManager-1.0.gir

%files -n %{libnm_glib_vpn_devel}
%{_includedir}/libnm-glib/nm-vpn*.h
%{_libdir}/pkgconfig/libnm-glib-vpn.pc
%{_libdir}/libnm-glib-vpn.so
