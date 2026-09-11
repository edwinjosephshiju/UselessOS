# Native Window Verification & Benchmark Harness
add_executable(test_native_window
    test_native_window.cpp
)

target_link_libraries(test_native_window
    PRIVATE
        UselessOS::Desktop
        Qt${QT_VERSION_MAJOR}::Widgets
)

target_set_warnings(test_native_window)

# Cognitive Client Async Streaming Verification Harness
add_executable(test_cognitive_client
    test_cognitive_client.cpp
)

target_link_libraries(test_cognitive_client
    PRIVATE
        UselessOS::Desktop
        Qt${QT_VERSION_MAJOR}::Core
        Qt${QT_VERSION_MAJOR}::Network
)

target_set_warnings(test_cognitive_client)

# ==============================================================================
# Architecture Gate Proofs of Concept (PoCs)
# ==============================================================================
if(TARGET Qt${QT_VERSION_MAJOR}::WaylandClient)
    # PoC 1: Window Tracking under KWin Wayland
    set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-plasma-window-management-protocol.c PROPERTIES GENERATED TRUE)
    add_executable(poc_window_tracker
        poc_window_tracker.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-plasma-window-management-protocol.c
    )
    qt6_generate_wayland_protocol_client_sources(poc_window_tracker
        FILES
            ${CMAKE_SOURCE_DIR}/src/protocols/plasma-window-management.xml
    )
    target_link_libraries(poc_window_tracker
        PRIVATE
            Qt${QT_VERSION_MAJOR}::Core
            Qt${QT_VERSION_MAJOR}::Gui
            Qt${QT_VERSION_MAJOR}::GuiPrivate
            Qt${QT_VERSION_MAJOR}::WaylandClient
            PkgConfig::WAYLAND_CLIENT
    )
    target_include_directories(poc_window_tracker
        PRIVATE
            ${CMAKE_CURRENT_BINARY_DIR}
            /usr/include
    )

    # PoC 2: Layer Shell Multi-Surface under KWin Wayland
    find_program(WAYLAND_SCANNER_BIN wayland-scanner REQUIRED)
    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
        COMMAND ${WAYLAND_SCANNER_BIN} public-code /usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
        DEPENDS /usr/share/wayland-protocols/stable/xdg-shell/xdg-shell.xml
        VERBATIM
    )
    set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c PROPERTIES GENERATED TRUE)
    set_source_files_properties(${CMAKE_CURRENT_BINARY_DIR}/wayland-wlr-layer-shell-unstable-v1-protocol.c PROPERTIES GENERATED TRUE)

    add_executable(poc_layer_shell
        poc_layer_shell.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-wlr-layer-shell-unstable-v1-protocol.c
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
    )
    qt6_generate_wayland_protocol_client_sources(poc_layer_shell
        FILES
            ${CMAKE_SOURCE_DIR}/src/protocols/wlr-layer-shell-unstable-v1.xml
    )
    target_link_libraries(poc_layer_shell
        PRIVATE
            Qt${QT_VERSION_MAJOR}::Core
            Qt${QT_VERSION_MAJOR}::Gui
            Qt${QT_VERSION_MAJOR}::GuiPrivate
            Qt${QT_VERSION_MAJOR}::WaylandClient
            PkgConfig::WAYLAND_CLIENT
    )
    target_include_directories(poc_layer_shell
        PRIVATE
            ${CMAKE_CURRENT_BINARY_DIR}
            /usr/include
    )

    add_executable(test_layer_events
        test_layer_events.cpp
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-wlr-layer-shell-unstable-v1-protocol.c
        ${CMAKE_CURRENT_BINARY_DIR}/wayland-xdg-shell-protocol.c
        ${CMAKE_CURRENT_BINARY_DIR}/qwayland-wlr-layer-shell-unstable-v1.cpp
    )
    target_link_libraries(test_layer_events
        PRIVATE
            Qt${QT_VERSION_MAJOR}::Core
            Qt${QT_VERSION_MAJOR}::Gui
            Qt${QT_VERSION_MAJOR}::GuiPrivate
            Qt${QT_VERSION_MAJOR}::WaylandClient
            PkgConfig::WAYLAND_CLIENT
    )
    target_include_directories(test_layer_events
        PRIVATE
            ${CMAKE_CURRENT_BINARY_DIR}
            /usr/include
    )
endif()
