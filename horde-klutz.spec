%define	_hordeapp klutz
%define	_snap	2005-08-01
#define	_rc		rc1
%define	_rel	0.2
#
%include	/usr/lib/rpm/macros.php
Summary:	Horde comics-fetching module
Summary(pl):	Modu� Horde do pobierania komiks�w
Name:		%{_hordeapp}
Version:	0.1
Release:	%{?_rc:0.%{_rc}.}%{?_snap:0.%(echo %{_snap} | tr -d -).}%{_rel}
License:	GPL v2+
Group:		Applications/WWW
Source0:	ftp://ftp.horde.org/pub/snaps/%{_snap}/%{_hordeapp}-HEAD-%{_snap}.tar.gz
# Source0-md5:	3d3ef21991c2f8b3ac42f37d9ff76ac5
Source1:	%{_hordeapp}.conf
URL:		http://www.horde.org/klutz/
BuildRequires:	rpmbuild(macros) >= 1.226
BuildRequires:	tar >= 1:1.15.1
Requires:	apache >= 1.3.33-2
Requires:	apache(mod_access)
Requires:	horde >= 3.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# horde accesses it directly in help->about
%define		_noautocompressdoc  CREDITS
%define		_noautoreq		'pear(Horde.*)'

%define		hordedir	%{_datadir}/horde
%define		_sysconfdir	/etc/horde.org
%define		_appdir		%{hordedir}/%{name}

%description
Klutz is an application for viewing comic strips. It lets you view
comics by date or by comic strip.

The Horde Project writes web applications in PHP and releases them
under the GNU Public License. For more information (including help
with Klutz) please visit <http://www.horde.org/>.

%description -l pl
Klutz to aplikacja do ogl�dania pask�w komiks�w. Pozwala ogl�da�
komiksy po dacie albo pasku.

Projekt Horde tworzy aplikacje WWW w PHP i wydaje je na licencji GNU
General Public License. Wi�cej informacji (w��cznie z pomoc� dla
Klutza) mo�na znale�� na stronie <http://www.horde.org/>.

%prep
%setup -q -c -T -n %{?_snap:%{_hordeapp}-%{_snap}}%{!?_snap:%{_hordeapp}-%{version}%{?_rc:-%{_rc}}}
tar zxf %{SOURCE0} --strip-components=1

# considered harmful (horde/docs/SECURITY)
rm -f test.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp} \
	$RPM_BUILD_ROOT%{_appdir}/{docs,lib,locale,scripts,templates,themes}

cp -a *.php			$RPM_BUILD_ROOT%{_appdir}
for i in config/*.dist; do
	cp -a $i $RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/$(basename $i .dist)
done
echo '<?php ?>' >		$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php
cp -p config/conf.xml	$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.xml
touch					$RPM_BUILD_ROOT%{_sysconfdir}/%{_hordeapp}/conf.php.bak

cp -pR	lib/*			$RPM_BUILD_ROOT%{_appdir}/lib
cp -pR	locale/*		$RPM_BUILD_ROOT%{_appdir}/locale
cp -pR	templates/*		$RPM_BUILD_ROOT%{_appdir}/templates
cp -pR	themes/*		$RPM_BUILD_ROOT%{_appdir}/themes

ln -s %{_sysconfdir}/%{_hordeapp} $RPM_BUILD_ROOT%{_appdir}/config
ln -s %{_docdir}/%{name}-%{version}/CREDITS $RPM_BUILD_ROOT%{_appdir}/docs
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache-%{_hordeapp}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ ! -f %{_sysconfdir}/%{_hordeapp}/conf.php.bak ]; then
	install /dev/null -o root -g http -m660 %{_sysconfdir}/%{_hordeapp}/conf.php.bak
fi

# CHECK FIRST DOES IT HAVE SQL AND FILE THERE.
if [ "$1" = 1 ]; then
%banner %{name} -e <<-EOF
	IMPORTANT:
	If you are installing Klutz for the first time, You may need to
	create the Klutz database tables. To do so run:
	zcat %{_docdir}/%{name}-%{version}/scripts/sql/%{_hordeapp}.sql.gz | mysql horde
EOF
fi

%triggerin -- apache1 >= 1.3.33-2
%apache_config_install -v 1 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache1 >= 1.3.33-2
%apache_config_uninstall -v 1

%triggerin -- apache >= 2.0.0
%apache_config_install -v 2 -c %{_sysconfdir}/apache-%{_hordeapp}.conf

%triggerun -- apache >= 2.0.0
%apache_config_uninstall -v 2

%files
%defattr(644,root,root,755)
%doc README docs/* scripts
%attr(750,root,http) %dir %{_sysconfdir}/%{_hordeapp}
%attr(640,root,root) %config(noreplace) %{_sysconfdir}/apache-%{_hordeapp}.conf
%attr(660,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/conf.php
%attr(660,root,http) %config(noreplace) %ghost %{_sysconfdir}/%{_hordeapp}/conf.php.bak
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/[!c]*.php
%attr(640,root,http) %config(noreplace) %{_sysconfdir}/%{_hordeapp}/comics.php
%attr(640,root,http) %{_sysconfdir}/%{_hordeapp}/conf.xml

%dir %{_appdir}
%{_appdir}/*.php
%{_appdir}/config
%{_appdir}/docs
%{_appdir}/lib
%{_appdir}/locale
%{_appdir}/templates
%{_appdir}/themes
