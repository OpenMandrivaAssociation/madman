%define name	madman
%define version	0.93
%define release	%mkrel 3

Summary:	Madman is a music manager
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
URL:		http://madman.sourceforge.net
Group:		Sound
Source0:	http://prdownloads.sourceforge.net/madman/%{name}-%{version}.tar.bz2
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Source4:	mad2pl-0.1.tar.bz2
Patch0:		madman-0.93-gcc3.4.patch.bz2
Patch1:         madman-fix-scons-0.96.1.patch.bz2
BuildRequires:	qt3-devel
BuildRequires:	xmms-devel
BuildRequires:	libid3tag-devel
BuildRequires:	oggvorbis-devel
BuildRequires:	scons

%description
Madman makes your digital music experience what it should have
been from the start. Fun, not clumsy. Organized, not a mess.
Cool, not technical.

Madman automatically creates an index of all the digital music
that you have. So, if you know you have that cool old Indie
album lying around somewhere, but you just can't remember where,
use madman's intelligent search features to see where it is.
You don't even need to remember the exact spelling, madman's
fuzzy search finds what you're looking for anyway. 
  

%prep
%setup -q
%setup -q -T -D -a4
%patch0 -p1
%patch1 -p0

%build
scons %_smp_mflags prefix=%{_prefix}

# make mad2pl
cd mad2pl
prefix=%{_prefix} make
cd ..

%install
rm -rf %{buildroot}
#gw includes wrong plugin dir
#scons prefix=%{buildroot}%{_prefix} install
mkdir -p %buildroot{%_bindir,%_libdir/%name/}
install -m 755 main/%name %buildroot%_bindir
cp -r plugins %buildroot%_libdir/%name/
rm -f %buildroot%_libdir/%name/plugins/README
rm -f %buildroot%_libdir/%name/plugins/plugin_example

# install mad2pl
pwd
cd mad2pl
install mad2pl %{buildroot}/%{_bindir}
# rename README
cp README README.mad2pl

# clean scons files:
rm -rf %{buildroot}/%{_bindir}/.sconsign %{buildroot}/%{_libdir}/madman/plugins/.sconsign

# menu
(cd $RPM_BUILD_ROOT
mkdir -p ./usr/lib/menu
cat > .%{_menudir}/%name <<EOF
?package(%name):\
command="%{_bindir}/%{name}"\
icon="%name.png"\
title="Madman"\
longtitle="Madman, a music manager."\
needs="x11"\
section="Multimedia/Sound"
EOF
)

install -d %buildroot/%_miconsdir
install -d %buildroot/%_liconsdir
install -d %buildroot/%_iconsdir

# icons
install -m644 %SOURCE1 %buildroot/%_miconsdir/%name.png
install -m644 %SOURCE2 %buildroot/%_iconsdir/%name.png
install -m644 %SOURCE3 %buildroot/%_liconsdir/%name.png

# no files yet
#%%{find_lang} %name


%post
%{update_menus}

%postun
%{clean_menus}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc COPYING README mad2pl/README.mad2pl
%{_bindir}/*
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%{_libdir}/%{name}/plugins/*
%{_iconsdir}/%name.png
%{_liconsdir}/%name.png
%{_miconsdir}/%name.png
%{_menudir}/%{name}


