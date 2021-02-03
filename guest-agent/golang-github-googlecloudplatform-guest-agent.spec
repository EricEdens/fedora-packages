# Generated by go2rpm 1.3
%bcond_without check

%global services        google-guest-agent.service google-startup-scripts.service google-shutdown-scripts.service

# https://github.com/GoogleCloudPlatform/guest-agent
%global goipath         github.com/GoogleCloudPlatform/guest-agent
Version:                20201217.02
%global tag             20201217.02

%gometa

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        Google Compute Engine guest environment

License:        ASL 2.0
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires: golang(cloud.google.com/go/storage)
BuildRequires: golang(github.com/go-ini/ini)
BuildRequires: golang(github.com/golang/groupcache/lru)
BuildRequires: golang(github.com/golang/protobuf/proto)
BuildRequires: golang(github.com/GoogleCloudPlatform/guest-logging-go/logger)
BuildRequires: golang(github.com/kardianos/service)
BuildRequires: golang(github.com/tarm/serial)
BuildRequires: golang(google.golang.org/grpc)
BuildRequires: golang(google.golang.org/grpc/codes)
BuildRequires: golang(google.golang.org/grpc/status)
BuildRequires: systemd-rpm-macros

Provides: google-guest-agent = %{version}-%{release}

Requires: systemd

%description
This package contains scripts, configuration, and init files
for features specific to the Google Compute Engine cloud environment.

%gopkg

%prep
%goprep

# Skip wsfc_test.go: It's specific for Windows, and it assumes that network is available,
# so it fails in a network-jailed build environment.
rm google_guest_agent/wsfc_test.go

%build
for cmd in google_guest_agent google_metadata_script_runner; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vd                     %{buildroot}%{_sysconfdir}/default
install -m 0755 -vd                     %{buildroot}%{_unitdir}
install -m 0755 -vd                     %{buildroot}%{_presetdir}

install -m 0755 -vp %{gobuilddir}/bin/*             %{buildroot}%{_bindir}
install -m 0644 -vp instance_configs.cfg            %{buildroot}%{_sysconfdir}/default
install -m 0644 -vp google-guest-agent.service      %{buildroot}%{_unitdir}
install -m 0644 -vp google-startup-scripts.service  %{buildroot}%{_unitdir}
install -m 0644 -vp google-shutdown-scripts.service %{buildroot}%{_unitdir}
install -m 0644 -vp 90-google-guest-agent.preset    %{buildroot}%{_presetdir}

%if %{with check}
%check
%gocheck
%endif

%files
%defattr(-,root,root,-)
%license LICENSE
%doc CONTRIBUTING.md README.md
%config(noreplace) %{_sysconfdir}/default/instance_configs.cfg
%{_bindir}/google_guest_agent
%{_bindir}/google_metadata_script_runner
%{_unitdir}/google-guest-agent.service
%{_unitdir}/google-startup-scripts.service
%{_unitdir}/google-shutdown-scripts.service
%{_presetdir}/90-google-guest-agent.preset

%post
%systemd_post %{services}

%preun
%systemd_preun %{services}

%postun
%systemd_postun_with_restart %{services}


%changelog
* Mon Jan 25 23:45:46 UTC 2021 Eric Edens <ericedens@google.com> - 20201217.02-1
- Initial package

