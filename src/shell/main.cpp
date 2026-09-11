#include <QGuiApplication>
#include <QScreen>
#include <QDebug>
#include <QList>
#include <csignal>
#include <algorithm>

#include <wayland-client.h>
#include <qpa/qplatformnativeinterface.h>

#include "WindowTracker.h"
#include "TopBarWindow.h"
#include "DockWindow.h"
#include "BackgroundCanvasWindow.h"

namespace {

static QtWayland::zwlr_layer_shell_v1 *s_layerShell = nullptr;
static struct wl_registry *s_registry = nullptr;
static uint32_t s_windowManagementId = 0;
static uint32_t s_windowManagementVersion = 0;
static uint32_t s_layerShellId = 0;
static uint32_t s_layerShellVersion = 0;

void registry_handle_global(void *, struct wl_registry *registry,
                            uint32_t id, const char *interface, uint32_t version)
{
    if (strcmp(interface, "zwlr_layer_shell_v1") == 0) {
        s_layerShellId = id;
        s_layerShellVersion = std::min(version, 4u);
        s_layerShell = new QtWayland::zwlr_layer_shell_v1(registry, id, s_layerShellVersion);
        qInfo() << "[UselessShell] Discovered zwlr_layer_shell_v1 v" << version;
    } else if (strcmp(interface, "org_kde_plasma_window_management") == 0) {
        s_windowManagementId = id;
        s_windowManagementVersion = std::min(version, 16u);
        qInfo() << "[UselessShell] Discovered org_kde_plasma_window_management v" << version;
    }
}

void registry_handle_global_remove(void *, struct wl_registry *, uint32_t) {}

static const struct wl_registry_listener registry_listener = {
    registry_handle_global,
    registry_handle_global_remove
};

} // namespace

int main(int argc, char *argv[])
{
    // Ensure Wayland platform plugin is prioritized
    if (!qEnvironmentVariableIsSet("QT_QPA_PLATFORM")) {
        qputenv("QT_QPA_PLATFORM", "wayland");
    }

    QGuiApplication app(argc, argv);
    app.setApplicationName("UselessOS Shell");
    app.setApplicationVersion("3.0.0");
    app.setOrganizationName("UselessOS");

    qInfo() << "========================================================";
    qInfo() << " UselessOS 3.0 Native Linux Desktop Shell";
    qInfo() << " Runtime: Wayland | KWin Compositor | C++20 / Qt 6";
    qInfo() << "========================================================";

    QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
    if (!native) {
        qCritical() << "[Fatal] QPlatformNativeInterface unavailable!";
        return 1;
    }

    struct wl_display *display = reinterpret_cast<struct wl_display*>(
        native->nativeResourceForIntegration("wl_display")
    );
    if (!display) {
        display = reinterpret_cast<struct wl_display*>(native->nativeResourceForIntegration("display"));
    }

    if (!display) {
        qCritical() << "[Fatal] Failed to acquire wl_display connection!";
        return 1;
    }

    s_registry = wl_display_get_registry(display);
    wl_registry_add_listener(s_registry, &registry_listener, nullptr);
    wl_display_roundtrip(display);

    if (!s_layerShell) {
        qCritical() << "[Fatal] zwlr_layer_shell_v1 protocol was not advertised by compositor!";
        return 1;
    }

    UselessOS::WindowTracker *tracker = nullptr;
    if (s_windowManagementId > 0) {
        tracker = new UselessOS::WindowTracker(display, s_registry, s_windowManagementId, s_windowManagementVersion, &app);
    } else {
        qWarning() << "[Warning] org_kde_plasma_window_management not available; running in standalone mode.";
    }

    struct ScreenSurfaces {
        UselessOS::TopBarWindow *topBar = nullptr;
        UselessOS::DockWindow *dock = nullptr;
        UselessOS::BackgroundCanvasWindow *canvas = nullptr;
    };
    QMap<QScreen*, ScreenSurfaces> activeScreens;

    auto setupScreen = [&](QScreen *scr) {
        if (!scr || activeScreens.contains(scr)) return;
        qInfo() << "[UselessShell] Configuring layer surfaces for screen:" << scr->name() << scr->geometry();

        ScreenSurfaces surfaces;
        surfaces.canvas = new UselessOS::BackgroundCanvasWindow(scr, s_layerShell);
        surfaces.topBar = new UselessOS::TopBarWindow(scr, tracker, s_layerShell);
        surfaces.dock = new UselessOS::DockWindow(scr, tracker, s_layerShell);

        activeScreens.insert(scr, surfaces);
    };

    auto removeScreen = [&](QScreen *scr) {
        if (activeScreens.contains(scr)) {
            auto s = activeScreens.take(scr);
            delete s.topBar;
            delete s.dock;
            delete s.canvas;
        }
    };

    // Initialize all existing connected outputs
    for (QScreen *scr : app.screens()) {
        setupScreen(scr);
    }

    // Connect display hot-plugging signals
    QObject::connect(&app, &QGuiApplication::screenAdded, [&](QScreen *scr) {
        qInfo() << "[UselessShell] Screen Connected:" << scr->name();
        setupScreen(scr);
    });
    QObject::connect(&app, &QGuiApplication::screenRemoved, [&](QScreen *scr) {
        qInfo() << "[UselessShell] Screen Disconnected:" << scr->name();
        removeScreen(scr);
    });

    wl_display_roundtrip(display);

    // Handle OS termination signals cleanly
    std::signal(SIGINT, [](int) { QGuiApplication::quit(); });
    std::signal(SIGTERM, [](int) { QGuiApplication::quit(); });

    qInfo() << "[UselessShell] Shell running. Exclusive zones active (TopBar: 42px, Dock: 80px).";
    return app.exec();
}
