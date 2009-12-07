Summary:	Update notification daemon
Name:		yum-updatesd
Version:	0.9
Release:	0.1
Epoch:		1
License:	GPL v2
Group:		Base
Source0:	%{name}-%{version}.tar.bz2
URL:		http://linux.duke.edu/yum/
BuildRequires:	python
Requires(post):	/sbin/chkconfig
Requires(post):	/sbin/service
Requires(preun):	/sbin/chkconfig
Requires(preun):	/sbin/service
Requires:	dbus-python
Requires:	gamin-python
Requires:	pygobject2
Requires:	python >= 2.4
Requires:	yum >= 3.2.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
yum-updatesd provides a daemon which checks for available updates and
can notify you when they are available via email, syslog or dbus.

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add yum-updatesd
service yum-updatesd restart

%preun
if [ "$1" = 0 ]; then
	/sbin/chkconfig --del yum-updatesd
	%service yum-updatesd stop
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) /etc/rc.d/init.d/yum-updatesd
%config(noreplace) %{_sysconfdir}/yum/yum-updatesd.conf
/etc/dbus-1/system.d/yum-updatesd.conf
%attr(755,root,root) %{_sbindir}/yum-updatesd
%{_libexecdir}/yum-updatesd-helper
%{_mandir}/man*/yum-updatesd*
