Summary:	RPM update notifier daemon
Summary(pl.UTF-8):	Demon powiadamiający o uaktualnionych RPM-ach
Name:		yum-updatesd
Version:	0.9
Release:	1
Epoch:		1
License:	GPL v2
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.bz2
# Source0-md5:	b03a3b3bf78a11fec240c82bf2f53b2b
URL:		http://linux.duke.edu/yum/
Source1:	%{name}.init
Source2:	%{name}.sysconfig
BuildRequires:	rpm-pythonprov
BuildRequires:	sed >= 4.0
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus
Requires:	python-dbus
Requires:	python-gamin
Requires:	python-pygobject >= 2.0
Requires:	rc-scripts
Requires:	yum >= 3.2.25-3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib

%description
This is a daemon which periodically checks for updates and can send
notifications via mail, dbus or syslog.

%description -l pl.UTF-8
Ten pakiet zawiera demona regularnie sprawdzającego dostępność
uaktualnień, mogącego wysyłać uaktualnienia pocztą elektroniczną,
poprzez dbus lub sysloga.

%prep
%setup -q
%{__sed} -i -e 's,/usr/libexec/,%{_libexecdir}/,' yum-updatesd
%{__sed} -i -e 's,\$(PREFIX)/libexec,%{_libexecdir},' Makefile

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -p %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/yum-updatesd
cp -a %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/yum-updatesd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add yum-updatesd
%service yum-updatesd restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del yum-updatesd
	%service -q yum-updatesd stop
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/yum/yum-updatesd.conf
/etc/dbus-1/system.d/yum-updatesd.conf
%attr(755,root,root) %{_sbindir}/yum-updatesd
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/yum-updatesd
%attr(754,root,root) /etc/rc.d/init.d/yum-updatesd
%attr(755,root,root) %{_libexecdir}/yum-updatesd-helper
%{_mandir}/man5/yum-updatesd.conf.5*
%{_mandir}/man8/yum-updatesd.8*
