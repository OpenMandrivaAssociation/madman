%define rel	2
%define git	20080904

%if %git
%define release		%{mkrel 0.%{git}.%{rel}}
%define distname	%{name}-%{git}.tar.lzma
%define dirname		%{name}
%else
%define release		%{mkrel %{rel}}
%define distname	%{name}-%{version}.tar.gz
%define dirname		%{name}-%{version}
%endif

Summary:	Music manager
Name:		madman
Version:	0.94
Release:	%{release}
License:	GPLv2+
URL:		https://madman.sourceforge.net
Group:		Sound
Source0:	http://downloads.sourceforge.net/%{name}/%{distname}
Source1:	%{name}-16.png
Source2:	%{name}-32.png
Source3:	%{name}-48.png
Source4:	mad2pl-0.1.tar.bz2
# Fix build with gcc 4.3 (bunch of missing includes) - AdamW 2008/09
Patch0:		madman-0.94-gcc43.patch
# Drop some bogus includes (breaks build) - AdamW 2008/09
Patch1:		madman-0.94-includes.patch
# Fix build of mad2pl with gcc 4.3 (includes) - AdamW 2008/09
Patch2:		mad2pl-0.1-includes.patch
BuildRoot:	%{_tmppath}/%{name}-%{version}
BuildRequires:	qt3-devel
BuildRequires:	xmms-devel
BuildRequires:	taglib-devel
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
%setup -q -n %{dirname}
%setup -q -n %{dirname} -T -D -a4
%patch0 -p1 -b .gcc43
%patch1 -p1 -b .includes
%patch2 -p1 -b .includes

%build
%configure_scons
%scons

# make mad2pl
pushd mad2pl
prefix=%{_prefix} make
popd

%install
rm -rf %{buildroot}
#gw includes wrong plugin dir
#scons_install
mkdir -p %{buildroot}{%_bindir,%_libdir/%{name}/}
install -m 755 ,build/release/main/%{name} %{buildroot}%{_bindir}
cp -r plugins %{buildroot}%{_libdir}/%{name}/
rm -f %{buildroot}%{_libdir}/%{name}/plugins/README
rm -f %{buildroot}%{_libdir}/%{name}/plugins/plugin_example

# install mad2pl
pwd
cd mad2pl
install mad2pl %{buildroot}/%{_bindir}
# rename README
cp README README.mad2pl

# clean scons files:
rm -rf %{buildroot}/%{_bindir}/.sconsign %{buildroot}/%{_libdir}/madman/plugins/.sconsign

# menu
mkdir -p %{buildroot}%{_datadir}/applications/
cat << EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Type=Application
Exec=%{_bindir}/%{name}
Icon=%{name}
Name=Madman
Comment=Music manager
Categories=Qt;Audio;Player;
EOF

mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps

# icons
install -m644 %{SOURCE1} %{buildroot}/%{_iconsdir}/hicolor/16x16/apps/%{name}.png
install -m644 %{SOURCE2} %{buildroot}/%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 %{SOURCE3} %{buildroot}/%{_iconsdir}/hicolor/48x48/apps/%{name}.png

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README mad2pl/README.mad2pl
%{_bindir}/*
%{_libdir}/%{name}
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_datadir}/applications/mandriva-%{name}.desktop

