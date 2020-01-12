Name:       plymouth-lite

Summary:    Boot splash screen based on Fedora's Plymouth code
Version:    0.7.0
Release:    2
Group:      System/Base
License:    GPLv2
URL:        https://github.com/nemomobile/plymouth-lite
Source0:    %{name}-%{version}.tar.bz2
Source1:    %{name}-start.service
Source2:    %{name}-halt.service
Source3:    %{name}-reboot.service
Source4:    %{name}-poweroff.service
Source5:    default.conf
Requires:   systemd
Requires(preun): systemd
Requires(post): systemd
Requires(postun): systemd
BuildRequires:  pkgconfig(libpng)
BuildRequires:  glibc-devel
BuildRequires:  pkgconfig(zlib)

%description
Boot splash screen based on Fedora's Plymouth code.

%package theme-default
Summary: Default theme of %{name}
Requires: %{name}

%description theme-default
Default theme of %{name} for glacier

%prep
%setup -q -n %{name}-%{version}

%build
# >> build pre
# << build pre

%configure --disable-static
make %{?jobs:-j%jobs}

# >> build post
# << build post

%install
rm -rf %{buildroot}
# >> install pre
# << install pre
%make_install

# >> install post
install -D -m 644 %{SOURCE1} %{buildroot}/lib/systemd/system/%{name}-start.service
install -d %{buildroot}/lib/systemd/system/sysinit.target.wants/
ln -s ../%{name}-start.service %{buildroot}/lib/systemd/system/sysinit.target.wants/%{name}-start.service

install -D -m 644 %{SOURCE2} %{buildroot}/lib/systemd/system/%{name}-halt.service
install -d %{buildroot}/lib/systemd/system/halt.target.wants/
ln -s ../%{name}-halt.service %{buildroot}/lib/systemd/system/halt.target.wants/%{name}-halt.service

install -D -m 644 %{SOURCE3} %{buildroot}/lib/systemd/system/%{name}-reboot.service
install -d %{buildroot}/lib/systemd/system/reboot.target.wants/
ln -s ../%{name}-reboot.service %{buildroot}/lib/systemd/system/reboot.target.wants/%{name}-reboot.service

install -D -m 644 %{SOURCE4} %{buildroot}/lib/systemd/system/%{name}-poweroff.service
install -d %{buildroot}/lib/systemd/system/poweroff.target.wants/
ln -s ../%{name}-poweroff.service %{buildroot}/lib/systemd/system/poweroff.target.wants/%{name}-poweroff.service
# << install post

install -D -m 644 %{SOURCE5} %{buildroot}/var/lib/environment/plymouth/default.conf

%preun
if [ "$1" -eq 0 ]; then
systemctl stop %{name}-start.service
systemctl stop %{name}-halt.service
systemctl stop %{name}-reboot.service
systemctl stop %{name}-poweroff.service
fi

%post
systemctl daemon-reload
systemctl reload-or-try-restart %{name}-start.service
systemctl reload-or-try-restart %{name}-halt.service
systemctl reload-or-try-restart %{name}-reboot.service
systemctl reload-or-try-restart %{name}-poweroff.service

%postun
systemctl daemon-reload

%files
%defattr(-,root,root,-)
%{_bindir}/ply-image
/lib/systemd/system/%{name}-start.service
/lib/systemd/system/sysinit.target.wants/%{name}-start.service
/lib/systemd/system/%{name}-halt.service
/lib/systemd/system/halt.target.wants/%{name}-halt.service
/lib/systemd/system/%{name}-reboot.service
/lib/systemd/system/reboot.target.wants/%{name}-reboot.service
/lib/systemd/system/%{name}-poweroff.service
/lib/systemd/system/poweroff.target.wants/%{name}-poweroff.service

%files theme-default
%{_datadir}/plymouth/splash.png
/var/lib/environment/plymouth/default.conf
