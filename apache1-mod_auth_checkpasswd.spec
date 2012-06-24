%define		mod_name	auth_checkpasswd
Summary:	This is the CHECKPASSWD authentication module for Apache
Summary(pl):	To jest modu� Apache autentykuj�cy przez CHECKPASSWD
Name:		apache-mod_%{mod_name}
Version:	1.0
Release:	1
License:	GPL
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	mod_%{mod_name}-%{version}.tar.gz
BuildRequires:	/usr/sbin/apxs
BuildRequires:	apache(EAPI)-devel
Prereq:		/usr/sbin/apxs
Requires:	apache(EAPI)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(/usr/sbin/apxs -q LIBEXECDIR)

%description
This is an authentication module for Apache that uses an external
application compatibile with DJB's "checkpasswd".
The application may be setuid, which gives you a possibility to verify
passwords using regular /etc/shadow.

%description -l pl
To jest modu� autentykuj�cy dla Apache kt�ry wykorzystuje zewn�trzn�
aplikacj� kompatybiln� z "checkpasswd" DJB.
Aplikacja mo�e by� suidowana, co daje mo�liwo�� weryfikowania hase�
wykorzystuj�c zwyk�y plik /etc/shadow.

%prep 
%setup -q -c -n "mod_%{mod_name}-%{version}"

%build
/usr/sbin/apxs \
	-c mod_%{mod_name}.c \
	-o mod_%{mod_name}.so

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_pkglibdir}

install mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}

gzip -9nf README

%post
/usr/sbin/apxs -e -a -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
if [ -f /var/lock/subsys/httpd ]; then
	/etc/rc.d/init.d/httpd restart 1>&2
fi

%preun
if [ "$1" = "0" ]; then
	/usr/sbin/apxs -e -A -n %{mod_name} %{_pkglibdir}/mod_%{mod_name}.so 1>&2
	if [ -f /var/lock/subsys/httpd ]; then
		/etc/rc.d/init.d/httpd restart 1>&2
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_pkglibdir}/*
