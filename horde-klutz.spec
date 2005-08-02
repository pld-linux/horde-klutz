#define	_rc		rc1
%define	_snap	2005-08-01
%define	_rel	0.1
%include	/usr/lib/rpm/macros.php
Summary:	Horde comics-fetching module
Name:		klutz
Version:	0.1
Release:	%{?_rc:%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2+
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{name}-HEAD-%{_snap}.tar.gz
# Source0-md5:	3d3ef21991c2f8b3ac42f37d9ff76ac5
Source1:	%{name}.conf
URL:		http://www.horde.org/klutz/
BuildRequires:	rpmbuild(macros) >= 1.226
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq		'pear(Horde.*)'

%define		hordedir		/usr/share/horde
%define		_sysconfdir		/etc/horde.org
%define		_appdir			%{hordedir}/%{name}

%description
Klutz is an application for viewing comic strips. It lets you view
comics by date or by comic strip.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Klutz) please visit <http://www.horde.org/>.

%prep
%setup -q -n %{?_snap:%{name}}%{!?_snap:%{name}-h3-%{version}%{?_rc:-%{_rc}}}

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.daily,%{_sysconfdir}/%{name}} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -pR	*.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -p $i $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/$(basename $i .dist)
done
echo "<?php ?>" > 		$RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php
cp -p  config/*.xml            $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
> $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{name} 	$RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_defaultdocdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs

install %{SOURCE1} 		$RPM_BUILD_ROOT%{_sysconfdir}/apache-%{name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{name}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{name}/conf.php.bak
fi

# CHECK FIRST DOES IT HAVE SQL AND FILE THERE.
if [ "$1" = 1 ]; then
%banner %{name} -e <<-EOF
	IMPORTANT:
	If you are installing Klutz for the first time, You may need to
	create the Klutz database tables. To do so run:
	zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{name}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{name}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{name}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{name}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{name}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{name}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{name}/comics.php
%attr(640,root,http) %{_sysconfdir}/%{name}/*.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
