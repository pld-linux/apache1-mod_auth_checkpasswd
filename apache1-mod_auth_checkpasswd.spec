%define		mod_name	auth_checkpasswd
%define 	apxs		/usr/sbin/apxs1
Summary:	This is the CHECKPASSWD authentication module for Apache
Summary(pl.UTF-8):	To jest moduł Apache uwierzytelniający przez CHECKPASSWD
Name:		apache1-mod_%{mod_name}
Version:	1.0
Release:	3
License:	GPL
Group:		Networking/Daemons
Source0:	mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7f699981ada026656affe2e35409bdf2
Patch0:		%{name}-aplog.patch
BuildRequires:	apache1-apxs
BuildRequires:	apache1-devel >= 1.3.33-2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(triggerpostun):	%{apxs}
Requires:	apache1(EAPI)
Obsoletes:	apache-mod_auth_checkpasswd <= 1.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

%description
This is an authentication module for Apache that uses an external
application compatible with DJB's "checkpasswd". The application may
be setuid, which gives you a possibility to verify passwords using
regular /etc/shadow.

%description -l pl.UTF-8
To jest moduł uwierzytelniający dla Apache który wykorzystuje
zewnętrzną aplikację kompatybilną z "checkpasswd" DJB. Aplikacja może
być suidowana, co daje możliwość weryfikowania haseł wykorzystując
zwykły plik /etc/shadow.

%prep
%setup -q -c -n "mod_%{mod_name}-%{version}"
%patch0 -p1

%build
%{apxs} -c mod_%{mod_name}.c -o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}/conf.d}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

echo 'LoadModule %{mod_name}_module	modules/mod_%{mod_name}.so' > \
	$RPM_BUILD_ROOT%{_sysconfdir}/conf.d/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q apache restart

%postun
if [ "$1" = "0" ]; then
	%service -q apache restart
fi

%triggerpostun -- apache1-mod_%{mod_name} < 1.0-1.1
# check that they're not using old apache.conf
if grep -q '^Include conf\.d' /etc/apache/apache.conf; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/conf.d/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
