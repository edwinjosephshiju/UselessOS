# Shared Core Desktop Library: libuselessdesktop
add_library(uselessdesktop SHARED
    include/UselessTheme.h
    include/CustomTitleBar.h
    include/UselessInstructionsDialog.h
    include/UselessWindow.h
    include/CognitiveClient.h
    src/UselessTheme.cpp
    src/CustomTitleBar.cpp
    src/UselessInstructionsDialog.cpp
    src/UselessWindow.cpp
    src/CognitiveClient.cpp
)

add_library(UselessOS::Desktop ALIAS uselessdesktop)

target_include_directories(uselessdesktop
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

target_link_libraries(uselessdesktop
    PUBLIC
        Qt${QT_VERSION_MAJOR}::Core
        Qt${QT_VERSION_MAJOR}::Gui
        Qt${QT_VERSION_MAJOR}::Widgets
        Qt${QT_VERSION_MAJOR}::Network
)

if(TARGET Qt${QT_VERSION_MAJOR}::Svg)
    target_link_libraries(uselessdesktop PUBLIC Qt${QT_VERSION_MAJOR}::Svg)
endif()

if(TARGET KF${QT_VERSION_MAJOR}::WindowSystem)
    target_link_libraries(uselessdesktop PUBLIC KF${QT_VERSION_MAJOR}::WindowSystem)
    target_compile_definitions(uselessdesktop PUBLIC USELESS_HAS_KWINDOWSYSTEM=1)
endif()

target_set_warnings(uselessdesktop)

set_target_properties(uselessdesktop PROPERTIES
    VERSION ${PROJECT_VERSION}
    SOVERSION 3
    CXX_VISIBILITY_PRESET default
    VISIBILITY_INLINES_HIDDEN 0
)
