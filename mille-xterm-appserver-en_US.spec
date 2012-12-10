Summary:	Mille-xterm application server english patch
Name:		mille-xterm-appserver-en_US
Version:	1.0
Release:	%mkrel 5
License:	GPL
Group:		System/Servers
Source0:	%{name}-%{version}.tar.bz2
Requires:	mille-xterm-appserver >= 1.0
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The mille-xterm application server is the component that terminal will connect
to get their display. It has a full desktop installed and configured for users.

This package translates parts of the application server from French to English.

%prep

%setup -q

%build
#nothing to be done here

%install
rm -fr %{buildroot}

pushd src/mille-xterm
mkdir -p %{buildroot}%{_sysconfdir}/mille-xterm/{postsession.d,presession.d,usersession.d}
cp postsession.d/50_kill_ltspfs.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/postsession.d/.50_kill_ltspfs.sh.en_US
cp presession.d/10_generate_sshkeys.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/presession.d/.10_generate_sshkeys.sh.en_US
cp presession.d/11_getlts.sh 		%{buildroot}%{_sysconfdir}/mille-xterm/presession.d/.11_getlts.sh.en_US
cp presession.d/20_sendsshkeys.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/presession.d/.20_sendsshkeys.sh.en_US
cp presession.d/50_start_ltspfs.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/presession.d/.50_start_ltspfs.sh.en_US
cp usersession.d/50_mount_ltspfs.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/usersession.d/.50_mount_ltspfs.sh.en_US
cp usersession.d/70_fix_apps.sh 	%{buildroot}%{_sysconfdir}/mille-xterm/usersession.d/.70_fix_apps.sh.en_US
popd

pushd src
mkdir -p %{buildroot}%{_sysconfdir}/custom/apps/firefox/config
mkdir -p %{buildroot}%{_sysconfdir}/custom/apps/thunderbird/rootinstall
mkdir -p %{buildroot}%{_sysconfdir}/custom/share/doc/HTML
mkdir -p %{buildroot}%{_sysconfdir}/X11/gdm
cp custom/apps/firefox/config/userinstall 	%{buildroot}%{_sysconfdir}/custom/apps/firefox/config/.userinstall.en_US
cp custom/apps/thunderbird/rootinstall/tbdic 	%{buildroot}%{_sysconfdir}/custom/apps/thunderbird/rootinstall/.tbdic.en_US
cp custom/share/doc/HTML/index.html 		%{buildroot}%{_sysconfdir}/custom/share/doc/HTML/.index.html.en_US
cp gdm/killsessions				%{buildroot}%{_sysconfdir}/X11/gdm/.killsessions.en_US
popd

%clean
rm -rf %{buildroot}

%post

# We have to manage 4 files that are part of other packages
# It's safe to do that because they are managed as config files in other packages

# First, make a backup
for file in 	%{_sysconfdir}/mille-xterm/postsession.d/50_kill_ltspfs.sh 	\
		%{_sysconfdir}/mille-xterm/presession.d/10_generate_sshkeys.sh	\
		%{_sysconfdir}/mille-xterm/presession.d/11_getlts.sh		\
		%{_sysconfdir}/mille-xterm/presession.d/20_sendsshkeys.sh	\
		%{_sysconfdir}/mille-xterm/presession.d/50_start_ltspfs.sh	\
		%{_sysconfdir}/mille-xterm/usersession.d/50_mount_ltspfs.sh	\
		%{_sysconfdir}/mille-xterm/usersession.d/70_fix_apps.sh		\
		%{_sysconfdir}/custom/apps/firefox/config/userinstall		\
		%{_sysconfdir}/custom/apps/thunderbird/rootinstall/tbdic	\
		%{_sysconfdir}/custom/share/doc/HTML/index.html			\
		%{_sysconfdir}/X11/gdm/killsessions

do
	DN=`dirname $file`
	BN=`basename $file`
	if [ -f $file ]; then
		# Do not overwrite already existing
		# backup (in case of upgrade)
		if [ ! -f $DN/.$BN.orig ]; then
			if [ -f $file.mille_xterm_saved ]; then
				mv -f $file.mille_xterm_saved $DN/.$BN.orig
			else
				mv -f $file $DN/.$BN.orig
			fi
		fi
	fi
	# Now, copy mille-xterm config files to replace existing ones
	cp -f  $DN/.$BN.en_US $file
done

if [ -f %{_sysconfdir}/X11/gdm/gdm.conf ] ; then
	if [ ! -f %{_sysconfdir}/X11/gdm/.gdm.conf.orig ] ; then
		if [ -f %{_sysconfdir}/X11/gdm/gdm.conf.mille_xterm_saved ] ; then
			mv -f %{_sysconfdir}/X11/gdm/gdm.conf.mille_xterm_saved %{_sysconfdir}/X11/gdm/.gdm.conf.orig
		else
			cp %{_sysconfdir}/X11/gdm/gdm.conf %{_sysconfdir}/X11/gdm/.gdm.conf.orig
		fi
	fi
	perl -pi -e "s/Bienvenue sur/Welcome to/g;" /etc/X11/gdm/gdm.conf
fi

if [ -f /var/www/html/state.php ] ; then
	perl -pi -e "s/utilisateurs connectés/connected users/g;" /var/www/html/state.php
fi


%preun

%postun
#Only if package is uninstalled
if [ "$1" = "0" ]; then
  # Replace original files in case of uninstall
  for file in 	%{_sysconfdir}/mille-xterm/presession.d/50_kill_ltspfs.sh	\
		%{_sysconfdir}/mille-xterm/presession.d/10_generate_sshkeys.sh	\
		%{_sysconfdir}/mille-xterm/presession.d/11_getlts.sh		\
		%{_sysconfdir}/mille-xterm/presession.d/20_sendsshkeys.sh	\
		%{_sysconfdir}/mille-xterm/presession.d/50_start_ltspfs.sh	\
		%{_sysconfdir}/mille-xterm/usersession.d/50_mount_ltspfs.sh	\
		%{_sysconfdir}/mille-xterm/usersession.d/70_fix_apps.sh		\
		%{_sysconfdir}/custom/apps/firefox/config/userinstall		\
		%{_sysconfdir}/custom/apps/thunderbird/rootinstall/tbdic	\
		%{_sysconfdir}/custom/share/doc/HTML/index.html			\
		%{_sysconfdir}/X11/gdm/killsessions
  do
	DN=`dirname $file`
	BN=`basename $file`
	if [ -f $DN/.$BN.orig ]; then
		mv -f $DN/.$BN.orig $file
	# support older schema
	elif [ -f $file.mille_xterm_saved ]; then
		mv -f $file.mille_xterm_saved $file
	fi
  done

	if [ -f %{_sysconfdir}/X11/gdm/.gdm.conf.orig ] ; then
		mv -f %{_sysconfdir}/X11/gdm/.gdm.conf.orig %{_sysconfdir}/X11/gdm/gdm.conf
	elif [ -f %{_sysconfdir}/X11/gdm/gdm.conf.mille_xterm_saved ] ; then
		mv -f %{_sysconfdir}/X11/gdm/gdm.conf.mille_xterm_saved %{_sysconfdir}/X11/gdm/gdm.conf
	fi
fi


%files
%defattr(-,root,root,-)
%{_sysconfdir}/mille-xterm
%{_sysconfdir}/X11/gdm/.killsessions.en_US
%{_sysconfdir}/custom/apps/firefox/config/.userinstall.en_US
%{_sysconfdir}/custom/apps/thunderbird/rootinstall/.tbdic.en_US
%{_sysconfdir}/custom/share/doc/HTML/.index.html.en_US




%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-5mdv2011.0
+ Revision: 620329
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 1.0-4mdv2010.0
+ Revision: 430028
- rebuild

* Tue Jul 29 2008 Thierry Vignaud <tv@mandriva.org> 1.0-3mdv2009.0
+ Revision: 252429
- rebuild

* Fri Dec 21 2007 Olivier Blin <oblin@mandriva.com> 1.0-1mdv2008.1
+ Revision: 136579
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.0-1mdv2007.0
+ Revision: 117757
- Import mille-xterm-appserver-en_US

* Tue Jan 23 2007 Mikael Andersson <mikael.andersson@envitory.se> 1.0-1mdk
- initial Mandriva package

