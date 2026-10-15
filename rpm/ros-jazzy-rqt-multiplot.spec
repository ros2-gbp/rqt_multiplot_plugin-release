%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

%global __cmake_in_source_build 1

Name:           ros-jazzy-rqt-multiplot
Version:        0.1.0
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS rqt_multiplot package

License:        GNU Lesser General Public License v3.0 (LGPL-3.0)
URL:            https://index.ros.org/p/rqt_multiplot/#jazzy
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-devel
Requires:       qt5-qtbase-devel
Requires:       qt5-qtsvg-devel
Requires:       qwt-qt5-devel
Requires:       ros-jazzy-ament-index-cpp
Requires:       ros-jazzy-diagnostic-msgs
Requires:       ros-jazzy-fastcdr
Requires:       ros-jazzy-geometry-msgs
Requires:       ros-jazzy-pluginlib
Requires:       ros-jazzy-qt-gui-cpp
Requires:       ros-jazzy-rcl
Requires:       ros-jazzy-rclcpp
Requires:       ros-jazzy-rclpy
Requires:       ros-jazzy-ros-babel-fish
Requires:       ros-jazzy-rosbag2-cpp
Requires:       ros-jazzy-rosbag2-storage
Requires:       ros-jazzy-rosbag2-storage-default-plugins
Requires:       ros-jazzy-rosbag2-storage-mcap
Requires:       ros-jazzy-rosidl-runtime-c
Requires:       ros-jazzy-rosidl-runtime-cpp
Requires:       ros-jazzy-rosidl-typesupport-fastrtps-cpp
Requires:       ros-jazzy-rosidl-typesupport-introspection-cpp
Requires:       ros-jazzy-rqt-gui
Requires:       ros-jazzy-rqt-gui-cpp
Requires:       ros-jazzy-sensor-msgs
Requires:       ros-jazzy-std-msgs
Requires:       ros-jazzy-type-description-interfaces
Requires:       ros-jazzy-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qwt-qt5-devel
BuildRequires:  ros-jazzy-ament-cmake
BuildRequires:  ros-jazzy-ament-index-cpp
BuildRequires:  ros-jazzy-fastcdr
BuildRequires:  ros-jazzy-pluginlib
BuildRequires:  ros-jazzy-qt-gui-cpp
BuildRequires:  ros-jazzy-rcl
BuildRequires:  ros-jazzy-rclcpp
BuildRequires:  ros-jazzy-ros-babel-fish
BuildRequires:  ros-jazzy-rosbag2-cpp
BuildRequires:  ros-jazzy-rosbag2-storage
BuildRequires:  ros-jazzy-rosbag2-storage-default-plugins
BuildRequires:  ros-jazzy-rosbag2-storage-mcap
BuildRequires:  ros-jazzy-rosidl-runtime-c
BuildRequires:  ros-jazzy-rosidl-runtime-cpp
BuildRequires:  ros-jazzy-rosidl-typesupport-fastrtps-cpp
BuildRequires:  ros-jazzy-rosidl-typesupport-introspection-cpp
BuildRequires:  ros-jazzy-rqt-gui
BuildRequires:  ros-jazzy-rqt-gui-cpp
BuildRequires:  ros-jazzy-type-description-interfaces
BuildRequires:  ros-jazzy-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  clang-tools-extra
BuildRequires:  ros-jazzy-ament-cmake-clang-format
BuildRequires:  ros-jazzy-ament-cmake-gtest
BuildRequires:  ros-jazzy-builtin-interfaces
BuildRequires:  ros-jazzy-diagnostic-msgs
BuildRequires:  ros-jazzy-geometry-msgs
BuildRequires:  ros-jazzy-rmw-cyclonedds-cpp
BuildRequires:  ros-jazzy-rmw-fastrtps-cpp
BuildRequires:  ros-jazzy-rmw-zenoh-cpp
BuildRequires:  ros-jazzy-sensor-msgs
BuildRequires:  ros-jazzy-std-msgs
BuildRequires:  ros-jazzy-test-msgs
%endif

%description
rqt_multiplot provides a GUI plugin for visualizing numeric values in multiple
2D plots using the Qwt plotting backend.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Thu Oct 15 2026 Samuel Bachmann <sbachmann@anybotics.com> - 0.1.0-2
- Autogenerated by Bloom

* Thu Oct 15 2026 Samuel Bachmann <sbachmann@anybotics.com> - 0.1.0-1
- Autogenerated by Bloom

