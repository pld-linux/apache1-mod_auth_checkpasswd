%define		mod_name	auth_checkpasswd
%define 	apxs		/usr/sbin/apxs
Summary:	This is the CHECKPASSWD authentication module for Apache
Summary(pl):	To jest modu� Apache autentykuj�cy przez CHECKPASSWD
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	4
License:	GPL
Group:		Networking/Daemons
Source0:	mod_%{mod_name}-%{version}.tar.gz
# Source0-md5:	7f699981ada026656affe2e35409bdf2
Patch0:		%{name}-aplog.patch
BuildRequires:	%{apxs}
BuildRequires:	apache(EAPI)-devel
Requires(post,preun):	%{apxs}
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR)

%description
This is an authentication module for Apache that uses an external
application compatible with DJB's "checkpasswd". The application may
be setuid, which gives you a possibility to verify passwords using
regular /etc/shadow.

%description -l pl
To jest modu� autentykuj�cy dla Apache kt�ry wykorzystuje zewn�trzn�
aplikacj� kompatybiln� z "checkpasswd" DJB. Aplikacja mo�e by�
suidowana, co daje mo�liwo�� weryfikowania hase� wykorzystuj�c zwyk�y
plik /etc/shadow.

%prep
%setup -q -c -n "mod_%{mod_name}-%{version}"
%patch -p1

%build
%{apxs} \
	-c mod_%{mod_name}.c \
	-o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{apxs} -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	%{apxs} -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_pkglibdir}/*
