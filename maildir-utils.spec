%global commit 52b7aae43915eeb5858389fa783c00b09a16d49b
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global checkout 20160611git%{shortcommit}

Name:		maildir-utils
Version:	0.9.16
Release:	2.%{checkout}%{?dist}
Summary:	mu is a tool for e-mail messages stored in the Maildir-format
Group:		Applications/Internet
License:	GPLv3
URL:		http://www.djcbsoftware.nl/code/mu/
Source0:	https://github.com/djcb/mu/archive/%{commit}/mu-%{commit}.tar.gz

BuildRequires:	autoconf, automake, libtool, texinfo, gmime-devel, xapian-core-devel
Requires:	gmime, xapian-core-libs

%description
A tool for dealing with e-mail messages stored in the
Maildir-format. mu’s purpose in life is to help you to quickly find
the messages you need; in addition, it allows you to view messages,
extract attachments, create new maildirs, and so on.

%package -n emacs-mu4e
Summary:	mu4e e-mail reader for GNU Emacs
Group:		Applications/Editors
BuildArch:	noarch
BuildRequires:	emacs-nox
Requires:	%{name} = %{version}-%{release}, emacs(bin) >= %{_emacs_version}

%description -n emacs-mu4e
%{summary}

%package -n emacs-mu4e-el
Summary:	Elisp source files for mu4e e-mail reader
Group:		Applications/Editors
BuildArch:	noarch
Requires:	emacs-mu4e = %{version}-%{release}

%description -n emacs-mu4e-el
%{summary}


%prep
%setup -qn mu-%{commit}


%build
autoreconf -i
%configure --enable-mu4e
%make_build


%install
%make_install
# Remove empty useless directory
rm -f %{buildroot}/%{_infodir}/dir


%post -n emacs-mu4e
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir 2>/dev/null || :


%preun -n emacs-mu4e
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete %{_infodir}/%{name}.info \
    %{_infodir}/dir 2>/dev/null || :
fi


%files
%doc %{_docdir}/mu/NEWS.org
%{_bindir}/mu
%{_mandir}/man*/*


%files -n emacs-mu4e
%doc %{_docdir}/mu/mu4e-about.org
%{_emacs_sitelispdir}/mu4e/*.elc
%{_infodir}/mu4e.info*

%files -n emacs-mu4e-el
%{_emacs_sitelispdir}/mu4e/*.el


%changelog
* Sat Jun 25 2016 James Davidson <james@greycastle.net> - 0.9.16-2.20160611git52b7aae4
- Change package name to maildir-utils to avoid conflict
- Update to upstream commit 52b7aae4

* Wed Feb 10 2016 James Davidson <james@greycastle.net> - 0.9.16-1
- Update to 0.9.16

* Wed Dec  2 2015 James Davidson <james@greycastle.net> - 0.9.15-2
- Update emacs-mu4e packaging

* Fri Nov 13 2015 James Davidson <james@greycastle.net> - 0.9.15-1
- Update to 0.9.15

* Fri Sep 25 2015 James Davidson <james@greycastle.net> - 0.9.13-1
- Update to 0.9.13

* Fri Jul 17 2015 James Davidson <james@greycastle.net> - 0.9.12-2.20150601git3804c0d
- Update mu package requires and description

* Wed Jul  1 2015 James Davidson <james@greycastle.net> - 0.9.12-1.20150601git3804c0d
- Initial packaging
