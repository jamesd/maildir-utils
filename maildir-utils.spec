%global repo mu

# For a snapshot based on a commit, just specify the commit id
# and update the date in checkout below
# N.B., remove the % in front of global
#global commit cb0025b352765e84c4de3a136d4e143ca07cd198
%if "%{?commit}" != ""
%global checkout .20170922git%(c=%{commit}; echo ${c:0:8})
%else
%global commit %{version}
%endif

%global _hardened_build 1

# maildir-utils-toys requires pkgconfig(webkitgtk-3.0) which f27-f29 does not have
%global _disable_webkit --disable-webkit

Name:		maildir-utils
Version:	1.2
Release:	1%{?checkout}%{?dist}
Summary:	mu is a tool for e-mail messages stored in the Maildir-format
License:	GPLv3+
URL:		http://www.djcbsoftware.nl/code/mu/
Source0:	https://github.com/djcb/%{repo}/archive/%{commit}.tar.gz#/%{name}-%{commit}.tar.gz

BuildRequires:	autoconf
BuildRequires:	autoconf-archive >= 2015.09.25
BuildRequires:	automake
BuildRequires:	gcc-c++
BuildRequires:	libtool
BuildRequires:	texinfo
BuildRequires:	pkgconfig(gmime-3.0)
BuildRequires:	pkgconfig(xapian-core)
Requires:	gmime
Requires:	xapian-core-libs
%{?f27:Obsoletes: maildir-utils-toys < 0.9.18-3.20170922gitcb0025b3}

%description
A tool for dealing with e-mail messages stored in the
Maildir-format. mu’s purpose in life is to help you to quickly find
the messages you need; in addition, it allows you to view messages,
extract attachments, create new maildirs, and so on.

%if 0%{!?_disable_webkit:1}
%package -n maildir-utils-toys
Summary:	mu additional toys
BuildRequires:	pkgconfig(gtk+-3.0)
BuildRequires:	pkgconfig(webkitgtk-3.0)
Requires:	%{name} = %{version}-%{release}
Requires:	gtk3
Requires:	webkitgtk3

%description -n maildir-utils-toys
%{summary}
%endif

%package -n emacs-mu4e
Summary:	mu4e e-mail reader for GNU Emacs
BuildArch:	noarch
BuildRequires:	emacs-nox
Requires:	%{name} = %{version}-%{release}
Requires:	emacs(bin) >= %{_emacs_version}

%description -n emacs-mu4e
%{summary}

%package -n emacs-mu4e-el
Summary:	Elisp source files for mu4e e-mail reader
BuildArch:	noarch
Requires:	emacs-mu4e = %{version}-%{release}

%description -n emacs-mu4e-el
%{summary}


%prep
%autosetup -n %{repo}-%{commit}


%build
autoreconf -i
%configure --enable-mu4e %{?_disable_webkit}
%make_build


%install
%make_install
%if 0%{!?_disable_webkit:1}
%{__install} -p -m 755 toys/mug/mug %{buildroot}%{_bindir}
%{__install} -p -m 755 toys/msg2pdf/msg2pdf %{buildroot}%{_bindir}
%endif
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

%if 0%{!?_disable_webkit:1}
%files -n maildir-utils-toys
%{_bindir}/mug
%{_bindir}/msg2pdf
%endif

%files -n emacs-mu4e
%doc %{_docdir}/mu/mu4e-about.org
%{_emacs_sitelispdir}/mu4e/*.elc
%{_infodir}/mu4e.info*

%files -n emacs-mu4e-el
%{_emacs_sitelispdir}/mu4e/*.el


%changelog
* Wed Apr 10 2019 James Davidson <james@greycastle.net> - 1.2-1
- Update to 1.2

* Sun Feb  4 2018 James Davidson <james@greycastle.net> - 1.0-1
- Update to 1.0

* Fri Nov 24 2017 James Davidson <james@greycastle.net> - 0.9.18-3.20170922gitcb0025b3
- Don't build maildir-utils-toys package in f27

* Fri Sep 22 2017 James Davidson <james@greycastle.net> - 0.9.18-2.20170922gitcb0025b3
- Update to upstream commit cb0025b3
- Fix licence to GPLv3+
- Add creation of maildir-utils-toys package

* Sat Jan  7 2017 James Davidson <james@greycastle.net> - 0.9.18-1
- Update to 0.9.18

* Sat Nov 12 2016 James Davidson <james@greycastle.net> - 0.9.17-1.
- Update to 0.9.17

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
