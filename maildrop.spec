#
# TODO:
#   - unpackaged files which already exist in courier.spec and
#     courier-authlib.spec, should they be packaged here too?
#     warning: Installed (but unpackaged) file(s) found:
#        /usr/bin/makedat
#        /usr/bin/makedatprog
#
# Conditional build:
%bcond_without authlib	# disable courier-authlib
#
Summary:	maildrop - mail filter/mail delivery agent
Summary(pl.UTF-8):	maildrop - filtr pocztowy/dostarczyciel poczty
Name:		maildrop
Version:	2.0.4
Release:	1
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	6a760efe429716ab0be67a1ddc554ed7
Patch0:		%{name}-db.patch
URL:		http://www.courier-mta.org/maildrop/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_authlib:BuildRequires:	courier-authlib-devel >= 0.58-4}
BuildRequires:	db-devel
BuildRequires:	fam-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pcre-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/maildrop

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

%package devel
Summary:	Development tools for handling E-mail messages
Summary(pl.UTF-8):	Narzędzia programisty do obsługi wiadomości E-mail
Group:		Applications/Mail

%description devel
The maildrop-devel package contains the libraries and header files
that can be useful in developing software that works with or processes
E-mail messages.

Install the maildrop-devel package if you want to develop applications
which use or process E-mail messages.

%description devel -l pl.UTF-8
Ten pakiet zawiera biblioteki i pliki nagłówkowe przydatne przy
tworzeniu oprogramowania pracującego z lub przetwarzającego wiadomości
E-mail.

%prep
%setup -q
%patch0 -p1

%build

for d in . numlib liblock unicode rfc822 rfc2045 gdbmobj bdbobj makedat maildir maildrop; do
cd $d
	%{__libtoolize}
	%{__aclocal}
	%{__autoconf}
	%{__automake}
cd -
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
	--enable-sendmail=%{_sbindir}/sendmail

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	MAILDROPUID="" \
	MAILDROPGID=""

rm -rf html
mv $RPM_BUILD_ROOT%{_datadir}/maildrop/html .

# courier-imap-maildirmake
rm -f $RPM_BUILD_ROOT%{_bindir}/maildirmake
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/maildir*
# courier-imap-deliverquota
rm -f $RPM_BUILD_ROOT%{_bindir}/deliverquota
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/deliverquota*

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

%files
%defattr(644,root,root,755)
%doc maildir/README.maildirquota.txt AUTHORS README README.postfix
%doc NEWS UPGRADE ChangeLog maildroptips.txt INSTALL README.pld
%doc html/
%dir %{_sysconfdir}
%attr(6755,root,mail) %{_bindir}/maildrop
%attr(6755,root,mail) %{_bindir}/lockmail
%attr(755,root,root) %{_bindir}/reformail
%attr(755,root,root) %{_bindir}/makemime
%attr(755,root,root) %{_bindir}/reformime
%attr(755,root,root) %{_bindir}/mailbot
%dir %{_datadir}/maildrop
%{_mandir}/man[17]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man3/*
