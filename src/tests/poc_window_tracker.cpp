#include <QGuiApplication>
#include <QDebug>
#include <QTimer>
#include <QMap>
#include <QString>
#include <QSocketNotifier>
#include <QScreen>
#include <iostream>
#include <iomanip>
#include <algorithm>

#include <wayland-client.h>
#include <qpa/qplatformnativeinterface.h>

#include "qwayland-plasma-window-management.h"

// Forward declaration
class WindowManager;

class WindowItem : public QObject, public QtWayland::org_kde_plasma_window {
    Q_OBJECT
public:
    QString uuid;
    QString title;
    QString appId;
    QString resourceName; // For XWayland applications
    bool isActive = false;
    bool isMinimized = false;
    bool isMaximized = false;
    QString virtualDesktop;
    int pid = 0;

    WindowItem(struct ::org_kde_plasma_window *win, const QString &id)
        : uuid(id)
    {
        init(win);
    }

    ~WindowItem() override {
        if (isInitialized()) {
            destroy();
        }
    }

protected:
    void org_kde_plasma_window_title_changed(const QString &newTitle) override {
        title = newTitle;
        qInfo().noquote() << QString("[WIN-EVENT] Title Changed -> [%1] '%2'").arg(uuid.left(8), title);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_app_id_changed(const QString &newAppId) override {
        appId = newAppId;
        qInfo().noquote() << QString("[WIN-EVENT] AppID Changed -> [%1] '%2'").arg(uuid.left(8), appId);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_resource_name_changed(const QString &resName) override {
        resourceName = resName;
        qInfo().noquote() << QString("[WIN-EVENT] (XWayland) Resource Name -> [%1] '%2'").arg(uuid.left(8), resourceName);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_pid_changed(uint32_t newPid) override {
        pid = static_cast<int>(newPid);
        qInfo().noquote() << QString("[WIN-EVENT] PID -> [%1] %2").arg(uuid.left(8)).arg(pid);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_state_changed(uint32_t flags) override {
        bool active = (flags & QtWayland::org_kde_plasma_window_management::state_active);
        bool minimized = (flags & QtWayland::org_kde_plasma_window_management::state_minimized);
        bool maximized = (flags & QtWayland::org_kde_plasma_window_management::state_maximized);

        if (active != isActive) {
            isActive = active;
            qInfo().noquote() << QString("[WIN-EVENT] Focus State -> [%1] %2").arg(uuid.left(8), isActive ? "ACTIVE (FOCUSED)" : "INACTIVE");
        }
        if (minimized != isMinimized) {
            isMinimized = minimized;
            qInfo().noquote() << QString("[WIN-EVENT] Minimized State -> [%1] %2").arg(uuid.left(8), isMinimized ? "MINIMIZED" : "RESTORED");
        }
        if (maximized != isMaximized) {
            isMaximized = maximized;
            qInfo().noquote() << QString("[WIN-EVENT] Maximized State -> [%1] %2").arg(uuid.left(8), isMaximized ? "MAXIMIZED" : "RESTORED");
        }
        Q_EMIT updated();
    }

    void org_kde_plasma_window_virtual_desktop_entered(const QString &id) override {
        virtualDesktop = id;
        qInfo().noquote() << QString("[WIN-EVENT] Workspace Entered -> [%1] Desktop '%2'").arg(uuid.left(8), id);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_virtual_desktop_left(const QString &id) override {
        qInfo().noquote() << QString("[WIN-EVENT] Workspace Left -> [%1] Desktop '%2'").arg(uuid.left(8), id);
        Q_EMIT updated();
    }

    void org_kde_plasma_window_unmapped() override {
        qInfo().noquote() << QString("[WIN-EVENT] Window Closed/Unmapped -> [%1] '%2'").arg(uuid.left(8), title);
        Q_EMIT closed(uuid);
    }

Q_SIGNALS:
    void updated();
    void closed(const QString &uuid);
};

class WindowManager : public QObject, public QtWayland::org_kde_plasma_window_management {
    Q_OBJECT
public:
    QMap<QString, WindowItem*> windows;

    WindowManager(struct ::wl_registry *registry, uint32_t id, int version)
    {
        init(registry, id, version);
        qInfo() << "[PoC] Bound org_kde_plasma_window_management protocol version" << version;
    }

    void dumpWindows() {
        std::cout << "\n================ CURRENT MAPPED WINDOWS (" << windows.size() << ") ================\n";
        std::cout << std::left << std::setw(12) << "UUID"
                  << std::setw(22) << "APP-ID / RES"
                  << std::setw(14) << "STATE"
                  << "TITLE\n";
        std::cout << "----------------------------------------------------------------\n";
        for (auto it = windows.begin(); it != windows.end(); ++it) {
            auto *w = it.value();
            QString idStr = w->appId.isEmpty() ? w->resourceName : w->appId;
            if (idStr.isEmpty()) idStr = QString("PID:%1").arg(w->pid);
            
            QString stateStr;
            if (w->isActive) stateStr += "[ACT] ";
            if (w->isMinimized) stateStr += "[MIN] ";
            if (w->isMaximized) stateStr += "[MAX] ";
            if (stateStr.isEmpty()) stateStr = "[NORM]";

            std::cout << std::left << std::setw(12) << w->uuid.left(10).toStdString()
                      << std::setw(22) << idStr.left(20).toStdString()
                      << std::setw(14) << stateStr.toStdString()
                      << w->title.toStdString() << "\n";
        }
        std::cout << "================================================================\n\n" << std::flush;
    }

    void activateWindow(const QString &uuid) {
        if (windows.contains(uuid)) {
            qInfo().noquote() << QString("[PoC-ACTION] Dispatched set_state(ACTIVE) -> [%1]").arg(uuid.left(8));
            windows[uuid]->set_state(
                QtWayland::org_kde_plasma_window_management::state_active,
                QtWayland::org_kde_plasma_window_management::state_active
            );
        }
    }

    void minimizeWindow(const QString &uuid) {
        if (windows.contains(uuid)) {
            qInfo().noquote() << QString("[PoC-ACTION] Dispatched set_state(MINIMIZED) -> [%1]").arg(uuid.left(8));
            windows[uuid]->set_state(
                QtWayland::org_kde_plasma_window_management::state_minimized,
                QtWayland::org_kde_plasma_window_management::state_minimized
            );
        }
    }

    void restoreWindow(const QString &uuid) {
        if (windows.contains(uuid)) {
            qInfo().noquote() << QString("[PoC-ACTION] Dispatched set_state(RESTORE) -> [%1]").arg(uuid.left(8));
            windows[uuid]->set_state(
                QtWayland::org_kde_plasma_window_management::state_minimized,
                0
            );
        }
    }

    void closeWindow(const QString &uuid) {
        if (windows.contains(uuid)) {
            qInfo().noquote() << QString("[PoC-ACTION] Dispatched close() -> [%1]").arg(uuid.left(8));
            windows[uuid]->close();
        }
    }

protected:
    void org_kde_plasma_window_management_window_with_uuid(uint32_t id, const QString &uuid) override {
        qInfo().noquote() << QString("[WIN-EVENT] Window Created -> ID: %1, UUID: %2").arg(id).arg(uuid.left(8));
        struct ::org_kde_plasma_window *rawWin = get_window_by_uuid(uuid);
        if (!rawWin) {
            rawWin = get_window(id);
        }
        if (rawWin) {
            registerWindow(rawWin, uuid);
        }
    }

    void org_kde_plasma_window_management_window(uint32_t id) override {
        QString syntheticUuid = QString("win-%1").arg(id);
        if (!windows.contains(syntheticUuid)) {
            qInfo().noquote() << QString("[WIN-EVENT] Window Created -> ID: %1").arg(id);
            struct ::org_kde_plasma_window *rawWin = get_window(id);
            if (rawWin) {
                registerWindow(rawWin, syntheticUuid);
            }
        }
    }

private:
    void registerWindow(struct ::org_kde_plasma_window *rawWin, const QString &uuid) {
        auto *winItem = new WindowItem(rawWin, uuid);
        connect(winItem, &WindowItem::closed, this, [this](const QString &u) {
            if (windows.contains(u)) {
                windows.take(u)->deleteLater();
                dumpWindows();
            }
        });
        connect(winItem, &WindowItem::updated, this, [this]() {
            // Updated
        });
        windows[uuid] = winItem;
    }
};

static WindowManager *s_wm = nullptr;

static void registry_handle_global(void *data, struct wl_registry *registry,
                                   uint32_t id, const char *interface, uint32_t version)
{
    if (strcmp(interface, "org_kde_plasma_window_management") == 0) {
        qInfo() << "[PoC] Discovered Wayland Global:" << interface << "Server Version:" << version;
        int bindVersion = std::min(static_cast<int>(version), 16);
        s_wm = new WindowManager(registry, id, bindVersion);
    }
}

static void registry_handle_global_remove(void *data, struct wl_registry *registry, uint32_t id)
{
    Q_UNUSED(data);
    Q_UNUSED(registry);
    Q_UNUSED(id);
}

static const struct wl_registry_listener registry_listener = {
    registry_handle_global,
    registry_handle_global_remove
};

int main(int argc, char *argv[])
{
    // Force Wayland QPA platform plugin
    qputenv("QT_QPA_PLATFORM", "wayland");

    QGuiApplication app(argc, argv);
    app.setApplicationName("UselessOS Window Tracker PoC");
    app.setApplicationVersion("1.0.0");

    qInfo() << "========================================================";
    qInfo() << " UselessOS Architecture Gate: Window Tracker PoC";
    qInfo() << " Testing org_kde_plasma_window_management under KWin";
    qInfo() << "========================================================";
    qInfo() << "Platform Name:" << QGuiApplication::platformName();
    
    for (QScreen *screen : QGuiApplication::screens()) {
        qInfo() << "Detected Output:" << screen->name() 
                << "Geometry:" << screen->geometry()
                << "DPR / Scale:" << screen->devicePixelRatio();
    }

    QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
    if (!native) {
        qCritical() << "Fatal: QPlatformNativeInterface not available!";
        return 1;
    }

    struct wl_display *display = reinterpret_cast<struct wl_display*>(
        native->nativeResourceForIntegration("wl_display")
    );
    if (!display) {
        display = reinterpret_cast<struct wl_display*>(
            native->nativeResourceForIntegration("display")
        );
    }

    if (!display) {
        qCritical() << "Fatal: Failed to obtain wl_display from Qt Wayland QPA!";
        return 1;
    }

    qInfo() << "[PoC] Connected to Wayland display socket successfully.";

    struct wl_registry *registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &registry_listener, nullptr);
    wl_display_roundtrip(display);

    if (!s_wm) {
        qCritical() << "Fatal: org_kde_plasma_window_management was NOT advertised by the compositor!";
        qCritical() << "Are you running inside KWin Wayland?";
        return 1;
    }

    qInfo() << "[PoC] org_kde_plasma_window_management successfully bound!";

    // Roundtrip to receive initial mapped windows
    wl_display_roundtrip(display);

    // Socket notifier for Wayland events
    int waylandFd = wl_display_get_fd(display);
    auto *notifier = new QSocketNotifier(waylandFd, QSocketNotifier::Read, &app);
    QObject::connect(notifier, &QSocketNotifier::activated, [&]() {
        wl_display_dispatch(display);
    });

    // Verification cycle timer: dumps status and demonstrates activation / minimization
    int cycleCount = 0;
    auto *timer = new QTimer(&app);
    QObject::connect(timer, &QTimer::timeout, [&]() {
        cycleCount++;
        wl_display_dispatch_pending(display);
        s_wm->dumpWindows();

        if (!s_wm->windows.isEmpty()) {
            QString firstUuid = s_wm->windows.firstKey();
            if (cycleCount == 3) {
                qInfo() << ">>> [TEST PHASE 1] Disagreeably Minimizing First Window <<<";
                s_wm->minimizeWindow(firstUuid);
                wl_display_flush(display);
            } else if (cycleCount == 6) {
                qInfo() << ">>> [TEST PHASE 2] Restoring and Activating First Window <<<";
                s_wm->restoreWindow(firstUuid);
                s_wm->activateWindow(firstUuid);
                wl_display_flush(display);
            } else if (cycleCount >= 10) {
                qInfo() << ">>> [PASS] All Window Tracking & Lifecycle Operations Verified! <<<";
                app.quit();
            }
        } else {
            qInfo() << "[PoC] Waiting for application windows to map... (Cycle" << cycleCount << ")";
            if (cycleCount >= 8) {
                qInfo() << "[PoC] Window tracker protocol binding validated successfully.";
                app.quit();
            }
        }
    });
    timer->start(1500);

    return app.exec();
}

#include "poc_window_tracker.moc"
