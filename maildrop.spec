Summary:	maildrop mail filter/mail delivery agent
Summary(pl):	maildrop - filtr pocztowy/dostarczyciel poczty
Name:		maildrop
Version:	1.3.5
Release:	1
License:	GPL
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico
Source0:	ftp://ftp1.sourceforge.net/pub/sourceforge/courier/%{name}-%{version}.tar.gz
URL:		http://www.flounder.net/~mrsam/maildrop/
Requires:	courier-imap-userdb
Requires:	courier-imap-maildirmake
Requires:	courier-imap-deliverquota
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Maildrop is a combination mail filter/mail delivery agent. Maildrop
reads the message to be delivered to your mailbox, optionally reads
instructions from a file how filter incoming mail, then based on these
instructions may deliver mail to an alternate mailbox, or forward it,
instead of dropping the message into your mailbox.

Maildrop uses a structured, real, meta-programming language in order
to define filtering instructions. Its basic features are fast and
efficient. At sites which carry a light load, the more advanced,
CPU-demanding, features can be used to build very sophisticated mail
filters. Maildrop deployments have been reported at sites that support
as many as 30,000 mailboxes.

Maildrop mailing list -- http://maildropl.listbot.com/

This version is compiled with support for GDBM database files, maildir
enhancements (folders+quotas), and userdb.

%package devel
Summary:	development tools for handling E-mail messages
Group:		Applications/Mail
Group(de):	Applikationen/Post
Group(pl):	Aplikacje/Poczta
Group(pt):	Aplicações/Correio Eletrônico

%description devel
The maildrop-devel package contains the libraries and header files
that can be useful in developing software that works with or processes
E-mail messages.

Install the maildrop-devel package if you want to develop applications
which use or process E-mail messages.

%prep
%setup -q

%build
%configure2_13 \
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

gzip -9nf maildir/README.maildirquota.txt AUTHORS README README.postfix \
	NEWS UPGRADE ChangeLog maildroptips.txt INSTALL

rm -f $RPM_BUILD_ROOT/%{_mandir}/man1/maildirmake.1
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/deliverquota*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/makeuserdb*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/userdb*
rm -f $RPM_BUILD_ROOT/%{_mandir}/man8/*pw2userdb*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc maildir/*.gz *.gz

%attr(6555,root,mail) %{_bindir}/maildrop
%attr(6555,root,mail) %{_bindir}/dotlock
%attr(755,root,root) %{_bindir}/makedat
%attr(755,root,root) %{_bindir}/makedatprog
%attr(755,root,root) %{_bindir}/reformail
%attr(755,root,root) %{_bindir}/makemime
%attr(755,root,root) %{_bindir}/reformime
%dir %{_datadir}/maildrop
%dir %{_datadir}/maildrop/scripts
%attr(755,root,root) %{_datadir}/maildrop/scripts/*
%{_mandir}/man[158]/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_libdir}/*
%{_mandir}/man3/*
