# NM relies on binutils __stop_SECTIONNAME symbols
# not currently generated by lld
# gold is currently removed so disable it for now
#global optflags %{optflags} -fuse-ld=gold

%define url_ver %(echo %{version}|cut -d. -f1,2)

%define rname NetworkManager
%define api 1.0

%define majglib 4
%define libnm_glib %mklibname nm-glib %{majglib}
%define girclient %mklibname nmclient-gir %{api}
%define devnm_glib %mklibname -d nm-glib

%define majvpn 1
%define libnm_glib_vpn %mklibname nm-glib-vpn %{majvpn}
%define devnm_glib_vpn %mklibname -d nm-glib-vpn

%define majutil 2
%define libnm_util %mklibname nm-util %{majutil}
%define girname %mklibname %{name}-gir %{api}
%define devnm_util %mklibname -d nm-util

%define majlibnm 0
%define libnm %mklibname nm %{majlibnm}
%define nm_girname %mklibname nm-gir %{api}
%define devnm %mklibname -d nm
%define ppp_version 2.5.2

Name:		networkmanager
Summary:	Network connection manager and user applications
Version:	1.50.2
Release:	1
Group:		System/Base
License:	GPLv2+
Url:		https://www.gnome.org/projects/NetworkManager/
#Source0:	https://download.gnome.org/sources/NetworkManager/%{url_ver}/%{rname}-%{version}.tar.xz
Source0:    https://gitlab.freedesktop.org/NetworkManager/NetworkManager/-/archive/%{version}/NetworkManager-%{version}.tar.bz2    
Source1:	NetworkManager.conf
Source3:	00-wifi-backend.conf

# OpenMandriva specific patches
Patch51:	networkmanager-0.9.8.4-add-systemd-alias.patch
#Patch52:	networkmanager-1.26.0-no-we-are-not-redhat.patch
BuildRequires:	meson
BuildRequires:	cmake
BuildRequires:	gtk-doc
BuildRequires:	docbook-dtd42-xml
BuildRequires:	iptables
BuildRequires:	pkgconfig(readline)
BuildRequires:	ppp-devel = %{ppp_version}
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	pkgconfig(gudev-1.0)
BuildRequires:	pkgconfig(libnl-3.0)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(libsystemd)
BuildRequires:	pkgconfig(nss)
BuildRequires:	systemd-rpm-macros
BuildRequires:	pkgconfig(glibmm-2.4)
BuildRequires:	pkgconfig(gnutls)
BuildRequires:	pkgconfig(polkit-gobject-1)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(libndp)
BuildRequires:	pkgconfig(libnewt)
BuildRequires:	pkgconfig(mm-glib)
BuildRequires:	pkgconfig(bluez)
BuildRequires:	pkgconfig(libteamdctl)
BuildRequires:	pkgconfig(libteam)
BuildRequires:	pkgconfig(jansson)
BuildRequires:	pkgconfig(libcurl)
BuildRequires:	python3dist(pygobject)
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(vapigen)
BuildRequires:	pkgconfig(mobile-broadband-provider-info)
# So we can locate polkit-agent-helper-1
BuildRequires:	polkit
# For wext support
BuildRequires:	kernel-headers >= 4.11
#BuildRequires:	python-gobject3-devel
Requires:	iproute2
%systemd_requires
Provides:	NetworkManager = %{EVRD}
Obsoletes:	dhcdbd
Obsoletes:	%{libnm_glib} < %{EVRD}
Obsoletes:	%{libnm_glib_vpn} < %{EVRD}
Conflicts:	%{_lib}nm_util1 < 0.7.996
# For a long time, initscripts has been just a collection
# of legacy networking scripts. Time to drop it for good.
Obsoletes:	initscripts < 11.0-1
# Let's not give people upgrading from monolithic NM (shipped until 4.2)
# a nasty surprise...
Recommends:	%{name}-wifi = %{EVRD}

%description
NetworkManager attempts to keep an active network connection available at all
times.  It is intended only for the desktop use-case, and is not intended for
usage on servers.   The point of NetworkManager is to make networking
configuration and setup as painless and automatic as possible.  If using DHCP,
NetworkManager is _intended_ to replace default routes, obtain IP addresses
from a DHCP server, and change nameservers whenever it sees fit.

%package -n %{libnm}
Summary:	Shared library for nm_util
Group:		System/Libraries
Obsoletes:	%{libnm_util} < %{EVRD}

%description -n %{libnm}
Shared library for nm.

%package -n %{nm_girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries

%description -n %{nm_girname}
GObject Introspection interface description for NM.

%package -n %{devnm}
Summary:	Development files for NM
Group:		Development/C
Provides:	nm-devel = %{EVRD}
Requires:	%{libnm} = %{EVRD}
Obsoletes:	%{devnm_util} < %{EVRD}
Obsoletes:	%{devnm_glib} < %{EVRD}

%description -n %{devnm}
Development files for NM.

%package -n %{girname}
Summary:	GObject Introspection interface description for %{name}
Group:		System/Libraries
Conflicts:	%{_lib}nm-util2 < 0.9.8.0-2
Obsoletes:	%{girclient} < %{EVRD}

%description -n %{girname}
GObject Introspection interface description for %{name}.

%package adsl
Summary:	Support for controlling ADSL connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description adsl
Support for controlling ADSL connections with NetworkManager

%package bluetooth
Summary:	Support for controlling BlueTooth connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Requires:	bluez

%description bluetooth
Support for controlling BlueTooth connections with NetworkManager

%package openvswitch
Summary:	Support for controlling OpenVSwitch with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description openvswitch
Support for controlling OpenVSwitch with NetworkManager

%package team
Summary:	Support for teaming network connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description team
Support for teaming network connections with NetworkManager

%package wifi
Summary:	Support for controlling WiFi connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Requires:	wireless-regdb
Requires:	(wpa_supplicant or iwd)
# Change once iwd becomes better than wireless-tools on non-Intel:
Suggests:	wpa_supplicant

%description wifi
Support for controlling WiFi connections with NetworkManager

%package wwan
Summary:	Support for controlling WWAN connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Requires:	modemmanager

%description wwan
Support for controlling WWAN connections with NetworkManager

%package ppp
Summary:	Support for controlling PPP connections with NetworkManager
Group:		System/Libraries
Requires:	%{name} = %{EVRD}
Requires:	ppp = %{ppp_version}
Requires:	modemmanager

%description ppp
Support for controlling PPP connections with NetworkManager

%package ifcfg-rh
Summary:	NetworkManager support for Red Hat style ifcfg-* config files
Group:		System/Libraries
Requires:	%{name} = %{EVRD}

%description ifcfg-rh
NetworkManager support for Red Hat style ifcfg-* config files

OpenMandriva does not use Red Hat style ifcfg-* config files, but some
third party applications (such as cloud-init) do. Install this package
if you need to run those applications.

%prep
%autosetup -p1 -n %{rname}-%{version}

%build
%define _disable_ld_no_undefined 1

%meson \
    -Dsystemdsystemunitdir="%{_unitdir}" \
    -Dsystem_ca_path="%{_sysconfdir}/pki/tls/certs" \
    -Dudev_dir="$(dirname %{_udevrulesdir})" \
    -Diptables="%{_bindir}/iptables-nft" \
    -Ddist_version="%{version}-%{release}" \
    -Dsession_tracking_consolekit=false \
    -Dsession_tracking=systemd \
    -Dsuspend_resume=systemd \
    -Dmodify_system=true \
    -Difcfg_rh=true \
    -Dofono=true \
    -Dselinux=false \
    -Dconfig_logging_backend_default=journal \
    -Dlibaudit=no \
    -Diwd=true \
    -Dpppd_plugin_dir="%{_libdir}/pppd/%{ppp_version}" \
    -Dteamdctl=true \
    -Dbluez5_dun=true \
    -Debpf=true \
    -Dresolvconf=no \
    -Dconfig_dns_rc_manager_default=auto \
    -Ddhcpcanon=no \
    -Ddhcpcd=no \
    -Dnft=%{_sbindir}/nft \
    -Dconfig_dhcp_default=internal \
    -Dintrospection=true \
    -Dvapi=true \
    -Ddocs=true \
    -Dtests=no \
    -Dmore_logging=false \
    -Dld_gc=false \
    -Dcrypto=gnutls \
    -Dqt=false

%meson_build

%install
%meson_install

cp %{SOURCE1} %{buildroot}%{_sysconfdir}/NetworkManager/

# create a VPN directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/VPN

# create keyfile plugin system-settings directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/system-connections

install -d %{buildroot}%{_prefix}/lib/%{rname}/conf.d/
install -d %{buildroot}%{_localstatedir}/lib/%{rname}/
touch %{buildroot}%{_localstatedir}/lib/%{rname}/%{rname}-intern.conf

# create a dnsmasq.d directory
install -d %{buildroot}%{_sysconfdir}/%{rname}/dnsmasq.d
install -d %{buildroot}%{_sysconfdir}/%{rname}/dnsmasq-shared.d/

install -d %{buildroot}%{_datadir}/gnome-vpn-properties

install -d %{buildroot}%{_localstatedir}/lib/NetworkManager

# (tpg) Those are not required with systemd-udevd v210 or newer
rm -rf %{buildroot}/lib/udev/rules.d/84-nm-drivers.rules

#rhbz#974811
ln -sr %{buildroot}%{_unitdir}/NetworkManager-dispatcher.service %{buildroot}%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service

# (bor) clean up on uninstall
install -d %{buildroot}%{_localstatedir}/lib/%{rname}
cd %{buildroot}%{_localstatedir}/lib/%{rname} && {
    touch %{rname}.state
    touch timestamps
cd -
}

cp %{SOURCE3} %{buildroot}%{_prefix}/lib/%{rname}/conf.d/

install -d %{buildroot}%{_presetdir}
cat > %{buildroot}%{_presetdir}/86-%{name}.preset << EOF
enable NetworkManager.service
enable NetworkManager-dispatcher.service
EOF

%find_lang %{rname}

%post
if [ -S /run/udev/control ]; then
    /bin/udevadm control --reload-rules || :
    /bin/udevadm trigger --subsystem-match=net || :
fi
%systemd_post NetworkManager.service NetworkManager-dispatcher.service nm-cloud-setup.service

%preun
if [ $1 -eq 0 ]; then
# Package removal, not upgrade
    /bin/systemctl --no-reload disable NetworkManager.service >/dev/null 2>&1 || :
fi
%systemd_preun NetworkManager-wait-online.service NetworkManager-dispatcher.service nm-cloud-setup.service

%postun
/bin/udevadm control --reload-rules || :
/bin/udevadm trigger --subsystem-match=net || :
%systemd_postun NetworkManager.service NetworkManager-dispatcher.service nm-cloud-setup.service

%files -f %{rname}.lang
%doc AUTHORS NEWS README* TODO
%dir %{_sysconfdir}/%{rname}
%config(noreplace) %{_sysconfdir}/%{rname}/NetworkManager.conf
%dir %{_sysconfdir}/%{rname}/conf.d
%dir %{_sysconfdir}/%{rname}/dispatcher.d
%dir %{_sysconfdir}/%{rname}/dnsmasq.d
%dir %{_sysconfdir}/%{rname}/dnsmasq-shared.d
%dir %{_sysconfdir}/%{rname}/system-connections
%dir %{_sysconfdir}/NetworkManager/VPN
%dir %{_prefix}/lib/%{rname}
%dir %{_prefix}/lib/%{rname}/conf.d
%{_bindir}/nmcli
%{_bindir}/nmtui
%{_bindir}/nmtui-connect
%{_bindir}/nmtui-edit
%{_bindir}/nmtui-hostname
%{_bindir}/nm-online
%{_sbindir}/%{rname}
%{_libexecdir}/nm-daemon-helper
%{_libexecdir}/nm-dhcp-helper
%{_libexecdir}/nm-dispatcher
#{_libexecdir}/nm-iface-helper
%{_libexecdir}/nm-initrd-generator
%{_libexecdir}/nm-priv-helper
%{_libexecdir}/nm-cloud-setup
%dir %{_libdir}/NetworkManager
%dir %{_libdir}/NetworkManager/%{version}-%{release}
%{_libdir}/pppd/*.*.*/nm-pppd-plugin.so
%dir %{_localstatedir}/lib/%{rname}
%ghost %{_localstatedir}/lib/%{rname}/*
%{_datadir}/bash-completion/completions/nmcli
%{_datadir}/dbus-1/interfaces/org.freedesktop.NetworkManager*.xml
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_dispatcher.service
%{_datadir}/dbus-1/system.d/nm-dispatcher.conf
%{_datadir}/dbus-1/system.d/org.freedesktop.NetworkManager.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.nm_priv_helper.service
%{_datadir}/dbus-1/system.d/nm-priv-helper.conf
%{_datadir}/polkit-1/actions/org.freedesktop.NetworkManager.policy
%{_udevrulesdir}/*.rules
%{_prefix}/lib/firewalld/zones/nm-shared.xml
%{_prefix}/lib/NetworkManager/dispatcher.d/
%{_presetdir}/86-%{name}.preset
%{_unitdir}/NetworkManager-wait-online.service
%{_unitdir}/NetworkManager-dispatcher.service
%{_unitdir}/nm-priv-helper.service
%dir %{_unitdir}/NetworkManager.service.d
%{_unitdir}/nm-cloud-setup.service
%{_unitdir}/nm-cloud-setup.timer
%{_unitdir}/dbus-org.freedesktop.nm-dispatcher.service
%{_unitdir}/NetworkManager.service
%doc %{_mandir}/man1/*.1*
%doc %{_mandir}/man5/*.5*
%doc %{_mandir}/man7/nmcli-examples.7*
%doc %{_mandir}/man8/*.8*
%{_datadir}/doc/NetworkManager/examples/server.conf

%files adsl
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-adsl.so

%files bluetooth
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-bluetooth.so

%files openvswitch
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-ovs.so
%{_unitdir}/NetworkManager.service.d/NetworkManager-ovs.conf
%doc %{_mandir}/man7/nm-openvswitch.7*

%files team
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-team.so

%files wifi
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-wifi.so
%{_prefix}/lib/%{rname}/conf.d/00-wifi-backend.conf

%files wwan
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-device-plugin-wwan.so
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-wwan.so

%files ppp
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-ppp-plugin.so

%files -n %{libnm}
%{_libdir}/libnm.so.%{majlibnm}*

%files -n %{nm_girname}
%{_libdir}/girepository-1.0/NM-%{api}.typelib

%files -n %{devnm}
%dir %{_includedir}/libnm
%{_includedir}/libnm/*.h
%doc %{_datadir}/gtk-doc/html/libnm
%doc %{_datadir}/gtk-doc/html/NetworkManager
%{_datadir}/gir-1.0/NM-1.0.gir
%{_libdir}/pkgconfig/libnm.pc
%{_libdir}/libnm.so
%{_datadir}/vala/vapi/libnm.deps
%{_datadir}/vala/vapi/libnm.vapi

%files -n %{girname}
%{_libdir}/girepository-1.0/NM-%{api}.typelib

%files ifcfg-rh
%{_libdir}/NetworkManager/%{version}-%{release}/libnm-settings-plugin-ifcfg-rh.so
%{_prefix}/libexec/nm-ifdown
%{_prefix}/libexec/nm-ifup
%{_datadir}/dbus-1/system.d/nm-ifcfg-rh.conf
