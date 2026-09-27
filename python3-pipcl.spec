#
# Conditional build:
%bcond_without	doc	# API documentation
%bcond_with	tests	# test suite (requires network and pip-managed python env)

Summary:	Python packaging operations, including PEP-517 support, for use by a setup.py script
Summary(pl.UTF-8):	Operacje pakietowania w Pythonie wraz z obsługą PEP-517 do użycia w skrypcie setup.py
Name:		python3-pipcl
Version:	13
Release:	1
License:	AGPL v3
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/pipcl/
Source0:	https://files.pythonhosted.org/packages/source/p/pipcl/pipcl-%{version}.tar.gz
# Source0-md5:	3160e2e8dc057a61437f403b2ad3d0f9
URL:		https://pypi.org/project/pipcl/
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-installer
BuildRequires:	python3-packaging
%if %{with tests}
BuildRequires:	python3-pip
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-alabaster
BuildRequires:	python3-autodocsumm
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-modules >= 1:3.2
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The pipcl package provides Python build backend operations (including
PEP 517 support), for use by a setup.py script:
- Designed to help build complex Python extension packages.
- Can also be used to build simple pure-python packages.
- Works on Linux, Windows, MacOS and OpenBSD.
- Is a python module, not a framework, so does not impose any
  restrictions on usage.
- Can be used with any external build system by running commands,
  for example with `subprocess.run()` or enhanced wrapper
  `pipcl.run()`.

%description -l pl.UTF-8
Pakiet pipcl udostępnia operacje backendu budowania dla Pythona (wraz
z obsługą PIP 517) do używania w skrypcie setup.py:
- zaprojektowany, aby pomóc przy budowaniu złożonych rozszerzeń
  Pythona
- może być używany także do budowania prostych, czysto pythonowych
  pakietów
- działa na Linuksie, Windows, MacOS i OpenBSD
- jest to moduł Pythona, nie szkielet, więc nie narzuca ograniczeń w
  sposobie użycia
- może być używany z dowolnym zewnętrznym systemem budowania poprzez
  uruchamianie poleceń, np. z `subprocess.run()` lub rozszerzonym
  obudowaniem `pipcl.run()`.

%package apidocs
Summary:	API documentation for Python pipcl module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona pipcl
Group:		Documentation

%description apidocs
API documentation for Python pipcl module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona pipcl.

%prep
%setup -q -n pipcl-%{version}

%{__sed} -i -e '/pip install /d' docs/conf.py

%build
%py3_build_pyproject

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd)/src \
%{__python3} -m pytest tests
%endif

%if %{with doc}
PYTHONPATH=$(pwd)/src \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst
%{py3_sitescriptdir}/pipcl
%{py3_sitescriptdir}/pipcl-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
