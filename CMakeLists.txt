cmake_minimum_required(VERSION 3.22)
project(UselessOS
    VERSION 3.0.0
    DESCRIPTION "Native Neobrutalist Desktop Environment and Application Suite"
    LANGUAGES C CXX
)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Enable standard Qt meta-object and resource compilation
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

# Export compile commands for language servers and IDE tooling
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Custom CMake modules
list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
list(APPEND CMAKE_MODULE_PATH "/usr/lib/x86_64-linux-gnu/cmake/Qt6/3rdparty/extra-cmake-modules/find-modules")
include(CompilerWarnings)

# Resolve Qt 6 (primary target), with seamless Qt 5 fallback for Debian 12 compatibility
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Gui Widgets Network)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Gui Widgets Network)

# Wayland native library & scanner integration
find_package(WaylandScanner REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(WAYLAND_CLIENT REQUIRED IMPORTED_TARGET wayland-client)

# Bypass Debian 12 packaging bug for Qt6WaylandClient plugins
set(QT_SKIP_AUTO_PLUGIN_INCLUSION ON)
find_package(Qt${QT_VERSION_MAJOR} OPTIONAL_COMPONENTS Quick Qml Svg WaylandClient)

# Resolve KDE Frameworks (KF6 or KF5) where available for native Linux window/hardware integration
find_package(KF${QT_VERSION_MAJOR} OPTIONAL_COMPONENTS WindowSystem NetworkManagerQt BluezQt Solid IdleTime)

message(STATUS "--------------------------------------------------------")
message(STATUS "Configuring UselessOS Modernization Suite v${PROJECT_VERSION}")
message(STATUS "Target Qt Version: Qt ${QT_VERSION_MAJOR} (${Qt${QT_VERSION_MAJOR}_VERSION})")
message(STATUS "C++ Standard: C++${CMAKE_CXX_STANDARD}")
if(TARGET KF${QT_VERSION_MAJOR}::WindowSystem)
    message(STATUS "KDE Frameworks WindowSystem: ENABLED (Native Wayland/X11 D-Bus)")
else()
    message(STATUS "KDE Frameworks WindowSystem: DISABLED (Fallback mode)")
endif()
message(STATUS "--------------------------------------------------------")

# Subdirectories
add_subdirectory(src)
