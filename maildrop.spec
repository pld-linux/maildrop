# TODO: use %%banner instead of ugly echoes
#
# Conditional build:
%bcond_without authlib	# disable courier-authlib
#
Summary:	maildrop - mail filter/mail delivery agent
Summary(pl.UTF-8):	maildrop - filtr pocztowy/dostarczyciel poczty
Name:		maildrop
Version:	2.5.5
Release:	3
License:	GPL v2 + OpenSSL exception
Group:		Applications/Mail
Source0:	http://downloads.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	5d71455ab26096ecf4f624fbee0320cb
Patch0:		%{name}-am-install.patch
URL:		http://www.courier-mta.org/maildrop/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_authlib:BuildRequires:	courier-authlib-devel >= 0.58-4}
BuildRequires:	db-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/maildrop
%define     skip_post_check_so	librfc2045.so.0.0.0 librfc822.so.0.0.0

%description
Maildrop is a combination of a mail filter/mail delivery agent.
Maildrop reads the message to be delivered to your mailbox, optionally
reads instructions from a file how to filter incoming mail, then based
on these instructions may deliver mail to an alternate mailbox, or
forward it, instead of dropping the message into your mailbox.

Maildrop uses a structured, real, meta-programming language in order
to define filtering instructions. Its basic features are fast and
efficient. At sites which carry a light load, the more advanced,
CPU-demanding, features can be used to build very sophisticated mail
filters. Maildrop deployments have been reported at sites that support
as many as 30,000 mailboxes.

This version is compiled with support for DB database files.

%description -l pl.UTF-8
Maildrop to połączenie filtra i dostarczyciela poczty. Czyta
wiadomość, która ma być dostarczona do skrzynki, opcjonalnie czyta
instrukcje z pliku jak filtrować przychodzącą pocztę, na podstawie
tych instrukcji może dostarczać pocztę do innej skrzynki, lub
forwardować zamiast wrzucać do podstawowej skrzynki.

Maildrop używa strukturalnego, rzeczywistego meta-języka programowania
do definiowania instrukcji filtrowania. Podstawowe możliwości są
szybkie i wydajne. Na serwerach z niewielkim obciążeniem można używać
bardziej zaawansowanych, obciążających procesor możliwości do
stworzenia przemyślanych filtrów pocztowych. Znane są przypadki
używania Maildropa na serwerach z 30 000 kontami pocztowymi.

Ta wersja jest skompilowana z obsługą plików baz DB.

%package libs
Summary:	Libraries for handling e-mail messages
Summary(pl.UTF-8):	Biblioteki do obsługi wiadomości e-mail
Group:		Libraries

%description libs
Libraries for handling e-mail messages.

%description libs -l pl.UTF-8
Biblioteki do obsługi wiadomości e-mail.

%package devel
Summary:	Header files for maildrop libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek maildrop
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
This package contains the header files that can be useful in
developing software that works with or processes E-mail messages.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe przydatne przy tworzeniu
oprogramowania pracującego z lub przetwarzającego wiadomości E-mail.

%package static
Summary:	Static maildrop libraries
Summary(pl.UTF-8):	Statyczne biblioteki maildrop
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static maildrop libraries.

%description static -l pl.UTF-8
Statyczne biblioteki maildrop.

%prep
%setup -q
%patch0 -p1

# confuses libtoolize, old contents not overwritten somewhy
find -name 'aclocal.m4' | xargs rm

%build
for d in . numlib liblock unicode rfc822 rfc2045 gdbmobj bdbobj makedat maildir maildrop; do
cd $d
	%{__libtoolize}
	%{__aclocal}
	%{__autoconf}
	%{__automake}
cd -
done
# Change Makefile.am files and force recreate Makefile.in's.
top=$(pwd)
find -type f -a '(' -name configure.in -o -name configure.ac ')' | while read a; do
	cd "$top/$(dirname "$a")"

	if [ -f Makefile.am ]; then
		sed -i -e '/_[L]DFLAGS=-static/d' Makefile.am
	fi

	%{__libtoolize}
	%{__aclocal}
	%{__autoconf}
	if grep -q AC_CONFIG_HEADER configure.in; then
		%{__autoheader}
	fi
	%{__automake}
done

%configure \
	--with-db=db \
	--with-etcdir=%{_sysconfdir} \
	--with-devel \
	--enable-maildirquota \
	--enable-syslog=1 \
	--enable-trusted-users='root mail daemon postmaster exim qmaild mmdf' \
	--enable-restrict-trusted=0 \
	--enable-maildrop-gid=maildrop \
	--disable-userdb  \
	%{!?with_authlib:--disable-authlib} \
	--enable-sendmail=/usr/lib/sendmail

%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	MAILDROPUID="" \
	MAILDROPGID=""

rm -rf html
mv $RPM_BUILD_ROOT%{_datadir}/maildrop/html .

# courier-authlib
%{__rm} $RPM_BUILD_ROOT%{_bindir}/makedat
%{__rm} $RPM_BUILD_ROOT%{_bindir}/makedatprog
# courier-imap-maildirmake
%{__rm} $RPM_BUILD_ROOT%{_bindir}/maildirmake
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man5/maildir*
# courier-imap-deliverquota
%{__rm} $RPM_BUILD_ROOT%{_bindir}/deliverquota

# small pld readme file
cat > README.pld <<'EOF'
To get "userdb" please install courier-authlib-userdb
To get "deliverquota" please install courier-imap-deliverquota
To get "maildirmake" please install courier-imap-maildirmake
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	echo
	echo Please read README.pld file
	echo
fi

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING INSTALL README README.postfix NEWS UPGRADE
%doc maildroptips.txt maildir/README.maildirquota.txt html/ README.pld
%attr(6755,root,mail) %{_bindir}/maildrop
%attr(6755,root,mail) %{_bindir}/lockmail
%attr(755,root,root) %{_bindir}/reformail
%attr(755,root,root) %{_bindir}/makemime
%attr(755,root,root) %{_bindir}/reformime
%attr(755,root,root) %{_bindir}/mailbot
%dir %{_sysconfdir}
%dir %{_datadir}/maildrop
%{_mandir}/man1/lockmail.1*
%{_mandir}/man1/mailbot.1*
%{_mandir}/man1/maildrop.1*
%{_mandir}/man1/makemime.1*
%{_mandir}/man1/reformail.1*
%{_mandir}/man1/reformime.1*
%{_mandir}/man7/maildropex.7*
%{_mandir}/man7/maildropfilter.7*
%{_mandir}/man7/maildropgdbm.7*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librfc2045.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librfc2045.so.0
%attr(755,root,root) %{_libdir}/librfc822.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librfc822.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librfc2045.so
%attr(755,root,root) %{_libdir}/librfc822.so
%{_libdir}/librfc2045.la
%{_libdir}/librfc822.la
%{_includedir}/rfc2045.h
%{_includedir}/rfc2047.h
%{_includedir}/rfc822.h
%{_mandir}/man3/rfc2045.3*
%{_mandir}/man3/rfc822.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/librfc2045.a
%{_libdir}/librfc822.a
