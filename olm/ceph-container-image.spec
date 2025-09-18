
%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%{!?registry_url: %global registry_url container-registry.oracle.com/olcne}
%{!?registry: %global registry container-registry.oracle.com/olcne}

%global _name   	ceph
%global _buildhost	build-ol%{?oraclelinux}-%{?_arch}.oracle.com
%ifarch %{arm} arm64 aarch64
%global arch aarch64
%global custom_arch arm64
%else
%global arch x86_64
%global custom_arch amd64
%endif
%global ceph_tag %{registry}/ceph:v%{version}

Name:           %{_name}-container-image
Version:        19.3.0
Release:        1%{?dist}
Summary:        Ceph container image
License:        Apache-2.0
Group:          System/Management
Url:            https://github.com/ceph/ceph
Source:         %{name}-%{version}.tar.bz2

BuildRequires: podman

%description
Ceph container image

%prep
%setup -q -n %{name}-%{version}

%build
pushd container
NO_PUSH=true CI_CONTAINER=false VERSION="19.3.0" CEPH_VERSION="19.3.0" CONTAINER_REPO_HOSTNAME=container-registry.oracle.com \
    CONTAINER_REPO_ORGANIZATION=olcne CONTAINER_REPO=ceph ./build.sh
popd
podman save -o %{_name}.tar %{ceph_tag}

%install
%__install -D -m 644 %{_name}.tar %{buildroot}/usr/local/share/olcne/%{_name}.tar

%files
%license src/cephadm/containers/keepalived/LICENSE src/ceph-volume/plugin/zfs/LICENSE olm/SECURITY.md
/usr/local/share/olcne/%{_name}.tar

%changelog
* Thu Sep 18 2025 Olcne-Builder Jenkins <olcne-builder_us@oracle.com> - 19.3.0-1
- Added Oracle specific files for 19.3.0
