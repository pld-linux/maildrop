# $Id: maildrop.spec,v 1.1 2000-12-15 14:05:41 marcus Exp $
#
# Copyright 1998 - 2000 Double Precision, Inc.  See COPYING for
# distribution information.

%define courier_release %(release="`rpm -q --queryformat='.%{VERSION}' redhat-release 2>/dev/null`" ; echo "$release")

Summary: maildrop mail filter/mail delivery agent
Name: maildrop
Version: 1.2.2
Release: 1%{courier_release}
Copyright: GPL
Group: Applications/Mail
Source: http://www.flounder.net/~mrsam/maildrop/maildrop-1.2.2.tar.gz
Url: http://www.flounder.net/~mrsam/maildrop/
Packager: %{PACKAGER}
BuildRoot: /var/tmp/maildrop-build

%package devel
Summary: development tools for handling E-mail messages
Group: Applications/Mail

%package man
Summary: manual pages for maildrop
Group: Applications/Mail

%description

Maildrop is a combination mail filter/mail delivery agent.
Maildrop reads the message to be delivered to your mailbox,
optionally reads instructions from a file how filter incoming
mail, then based on these instructions may deliver mail to an
alternate mailbox, or forward it, instead of dropping the
message into your mailbox.

Maildrop uses a structured, real, meta-programming language in
order to define filtering instructions.  Its basic features are
fast and efficient.  At sites which carry a light load, the
more advanced, CPU-demanding, features can be used to build
very sophisticated mail filters.  Maildrop deployments have
been reported at sites that support as many as 30,000
mailboxes.

Maildrop mailing list -- http://maildropl.listbot.com

This version is compiled with support for GDBM database files,
maildir enhancements (folders+quotas), and userdb.

%description devel
The maildrop-devel package contains the libraries and header files
that can be useful in developing software that works with or processes
E-mail messages.

Install the maildrop-devel package if you want to develop applications
which use or process E-mail messages.

%description man
This package contains manual pages for maildrop and associated
utilities.
%prep
%setup
%configure --with-devel --enable-userdb --enable-maildirquota --enable-syslog=1 --enable-trusted-users='root mail daemon postmaster qmaild mmdf' --enable-restrict-trusted=0 --enable-sendmail=/usr/sbin/sendmail

%build
make
%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT
make install-strip DESTDIR=$RPM_BUILD_ROOT MAILDROPUID='' MAILDROPGID=''

find $RPM_BUILD_ROOT%{_mandir} ! -type d -print | perl -e '
 while (<>)
  {
    $f=$_;  
    chop $f;
    next if $f =~ /\.gz$/;
    if (-l $f)
    {
        $f2=readlink($f);
        unlink($f);
        symlink "$f2.gz", "$f.gz";
    }
    else
    {
        system("gzip <$f >$f.gz");
        unlink($f);
    }
 } '

mkdir htmldoc
cp $RPM_BUILD_ROOT%{_datadir}/maildrop/html/* htmldoc
rm -rf $RPM_BUILD_ROOT%{_datadir}/maildrop/html

%files
%defattr(-, bin, bin)
%{_datadir}/maildrop

%doc htmldoc/*

%attr(6555, root, mail) %{_bindir}/maildrop
%attr(6555, root, mail) %{_bindir}/dotlock
%{_bindir}/maildirmake
%{_bindir}/deliverquota
%{_bindir}/makedat
%{_bindir}/makedatprog
%{_bindir}/makeuserdb
%{_bindir}/pw2userdb
%{_bindir}/userdb
%{_bindir}/userdbpw
%{_bindir}/reformail
%{_bindir}/makemime
%{_bindir}/reformime
%{_bindir}/vchkpw2userdb

%doc maildir/README.maildirquota.html maildir/README.maildirquota.txt
%doc COPYING README README.postfix INSTALL NEWS UPGRADE ChangeLog maildroptips.txt

%files devel
%defattr(-, bin, bin)
%{_mandir}/man3/*
%{_includedir}/*
%{_libdir}/*

%files man
%defattr(-, bin, bin)
%{_mandir}/man[158]/*

%clean
rm -rf $RPM_BUILD_ROOT
