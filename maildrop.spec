Summary:	maildrop - mail filter/mail delivery agent
Summary(pl):	maildrop - filtr pocztowy/dostarczyciel poczty
Name:		maildrop
Version:	1.7.0
Release:	2
License:	GPL
Group:		Applications/Mail
Source0:	http://dl.sourceforge.net/courier/%{name}-%{version}.tar.bz2
# Source0-md5:	fa2dbbb84795e459db36ea0013f6f214
URL:		http://www.courier-mta.org/maildrop/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	gdbm-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

This version is compiled with support for GDBM database files, maildir
enhancements (folders+quotas), and userdb.

%description -l pl
Maildrop to po��czenie filtra i dostarczyciela poczty. Czyta
wiadomo��, kt�ra ma by� dostarczona do skrzynki, opcjonalnie czyta
instrukcje z pliku jak filtrowa� przychodz�c� poczt�, na podstawie
tych instrukcji mo�e dostarcza� poczt� do innej skrzynki, lub
forwardowa� zamiast wrzuca� do podstawowej skrzynki.

Maildrop u�ywa strukturalnego, rzeczywistego meta-j�zyka programowania
do definiowania instrukcji filtrowania. Podstawowe mo�liwo�ci s�
szybkie i wydajne. Na serwerach z niewielkim obci��eniem mo�na u�ywa�
bardziej zaawansowanych, obci��aj�cych procesor mo�liwo�ci do
stworzenia przemy�lanych filtr�w pocztowych. Znane s� przypadki
u�ywania Maildropa na serwerach z 30 000 kontami pocztowymi.

Ta wersja jest skompilowana z obs�ug� plik�w baz GDBM, rozszerzeniami
maildir (foldery i quoty) oraz userdb.

%package devel
Summary:	Development tools for handling E-mail messages
Summary(pl):	Narz�dzia programisty do obs�ugi wiadomo�ci E-mail
Group:		Applications/Mail

%description devel
The maildrop-devel package contains the libraries and header files
that can be useful in developing software that works with or processes
E-mail messages.

Install the maildrop-devel package if you want to develop applications
which use or process E-mail messages.

%description devel -l pl
Ten pakiet zawiera biblioteki i pliki nag��wkowe przydatne przy
tworzeniu oprogramowania pracuj�cego z lub przetwarzaj�cego wiadomo�ci
E-mail.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-devel \
	--enable-userdb \
	--enable-maildirquota \
	--enable-syslog=1 \
	--enable-trusted-users='root mail daemon postmaster exim qmaild mmdf' \
	--enable-restrict-trusted=0 \
	--enable-sendmail=/usr/lib/sendmail
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	MAILDROPUID="" \
	MAILDROPGID=""

mv $RPM_BUILD_ROOT%{_datadir}/maildrop/html .

# courier-imap-userdb
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/makeuserdb*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/userdb*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/*pw2userdb*
# courier-imap-maildirmake
rm -f $RPM_BUILD_ROOT%{_bindir}/maildirmake
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/maildirmake.1
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/maildir*
# courier-imap-deliverquota
rm -f $RPM_BUILD_ROOT%{_bindir}/deliverquota
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/deliverquota*

# small pld readme file
cat > README.pld <<EOF
To get \"makeusedb\" please install courier-imap-userdb

To get \"deliverquota\" please install courier-imap-deliverquota

To get \"maildirmake\" please install courier-imap-maildirmake

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
%doc NEWS UPGRADE ChangeLog maildroptips.txt INSTALL html README.pld
%attr(6755,root,mail) %{_bindir}/maildrop
%attr(6755,root,mail) %{_bindir}/lockmail
%attr(755,root,root) %{_bindir}/makedat
%attr(755,root,root) %{_bindir}/makedatprog
%attr(755,root,root) %{_bindir}/reformail
%attr(755,root,root) %{_bindir}/makemime
%attr(755,root,root) %{_bindir}/reformime
%attr(755,root,root) %{_bindir}/mailbot
%dir %{_datadir}/maildrop
%dir %{_datadir}/maildrop/scripts
%attr(755,root,root) %{_datadir}/maildrop/scripts/*
%{_mandir}/man[1578]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man3/*
