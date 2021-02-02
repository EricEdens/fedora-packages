# Generated by go2rpm 1.3
%bcond_without check

# https://github.com/GoogleCloudPlatform/guest-agent
%global goipath         github.com/GoogleCloudPlatform/guest-agent
Version:                20201217.02
%global tag             20201217.02

%gometa

%global common_description %{expand:
Provides guest environment for instances running on Google Cloud Platform.}

%global golicenses      LICENSE
%global godocs          CONTRIBUTING.md README.md

Name:           %{goname}
Release:        1%{?dist}
Summary:        None

# Upstream license specification: BSD-3-Clause and Apache-2.0 and Zlib
License:        BSD and ASL 2.0 and zlib
URL:            %{gourl}
Source0:        %{gosource}

BuildRequires:  golang(cloud.google.com/go/storage)
BuildRequires:  golang(github.com/go-ini/ini)
BuildRequires:  golang(github.com/golang/groupcache/lru)
BuildRequires:  golang(github.com/golang/protobuf/proto)
BuildRequires:  golang(github.com/GoogleCloudPlatform/guest-logging-go/logger)
BuildRequires:  golang(github.com/kardianos/service)
BuildRequires:  golang(github.com/tarm/serial)
BuildRequires:  golang(google.golang.org/grpc)
BuildRequires:  golang(google.golang.org/grpc/codes)
BuildRequires:  golang(google.golang.org/grpc/status)

%description
%{common_description}

%gopkg

%prep
%goprep

# Skip wsfc_test.go, which assumes that network is available.
rm google_guest_agent/wsfc_test.go

%build
for cmd in google_guest_agent google_metadata_script_runner; do
  %gobuild -o %{gobuilddir}/bin/$(basename $cmd) %{goipath}/$cmd
done

%install
install -m 0755 -vd                     %{buildroot}%{_bindir}
install -m 0755 -vd                     %{_sysconfdir}/default
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
%{_unitdir}/google-startup-scripts.service
%{_presetdir}/90-google-guest-agent.preset

%changelog
* Mon Jan 25 23:45:46 UTC 2021 Eric Edens <ericedens@google.com> - 20201217.02-1
- Initial package
