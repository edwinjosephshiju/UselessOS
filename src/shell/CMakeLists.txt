find_program(WAYLAND_SCANNER_BIN wayland-scanner REQUIRED)

# Generate C protocol implementations
add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
    COMMAND ${WAYLAND_SCANNER_BIN} public-code /usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
    DEPENDS /usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml
    VERBATIM
)
set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c PROPERTIES GENERATED TRUE)

set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-plasma-window-management-protocol.c PROPERTIES GENERATED TRUE)
set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-wlr-layer-shell-unstable-v1-protocol.c PROPERTIES GENERATED TRUE)

add_executable(uselessos-shell
    main.cpp
    WindowTracker.h
    WindowTracker.cpp
    LayerSurfaceWindow.h
    LayerSurfaceWindow.cpp
    TopBarWindow.h
    TopBarWindow.cpp
    DockWindow.h
    DockWindow.cpp
    BackgroundCanvasWindow.h
    BackgroundCanvasWindow.cpp
    ${CMAKE_CURRENT_BINARY_DIR}/wayland-plasma-window-management-protocol.c
    ${CMAKE_CURRENT_BINARY_DIR}/wayland-wlr-layer-shell-unstable-v1-protocol.c
    ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
)

qt6_generate_wayland_protocol_client_sources(uselessos-shell
    FILES
        ${CMAKE_SOURCE_DIR}/src/protocols/plasma-window-management.xml
        ${CMAKE_SOURCE_DIR}/src/protocols/wlr-layer-shell-unstable-v1.xml
)

target_link_libraries(uselessos-shell
    PRIVATE
        UselessOS::Desktop
        Qt${QT_VERSION_MAJOR}::Core
        Qt${QT_VERSION_MAJOR}::Gui
        Qt${QT_VERSION_MAJOR}::GuiPrivate
        Qt${QT_VERSION_MAJOR}::WaylandClient
        PkgConfig::WAYLAND_CLIENT
)

target_include_directories(uselessos-shell
    PRIVATE
        ${CMAKE_CURRENT_BINARY_DIR}
        ${CMAKE_CURRENT_SOURCE_DIR}
        /usr/include
)

target_set_warnings(uselessos-shell)

install(TARGETS uselessos-shell DESTINATION /usr/local/bin)
install(FILES uselessos-shell.desktop DESTINATION /usr/share/applications)
