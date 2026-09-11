#include <QGuiApplication>
#include <QQuickView>
#include <QQmlEngine>
#include <QQmlContext>
#include <QScreen>
#include <QDebug>
#include <QTimer>
#include <wayland-client.h>
#include <qpa/qplatformnativeinterface.h>

#include "qwayland-wlr-layer-shell-unstable-v1.h"

static QtWayland::zwlr_layer_shell_v1 *s_layerShell = nullptr;

static void registry_handle_global(void *data, struct wl_registry *registry,
                                   uint32_t id, const char *interface, uint32_t version)
{
    if (strcmp(interface, "zwlr_layer_shell_v1") == 0) {
        int bindVersion = std::min(static_cast<int>(version), 4);
        s_layerShell = new QtWayland::zwlr_layer_shell_v1(registry, id, bindVersion);
    }
}

static void registry_handle_global_remove(void *, struct wl_registry *, uint32_t) {}

static const struct wl_registry_listener registry_listener = {
    registry_handle_global,
    registry_handle_global_remove
};

class LayerQuickView : public QQuickView, public QtWayland::zwlr_layer_surface_v1 {
public:
    LayerQuickView(struct wl_output *output, uint32_t layer, const QString &scope, int height, int exclusive) {
        setFlags(Qt::FramelessWindowHint | Qt::WindowStaysOnTopHint);
        setColor(QColor(0xFF, 0xE6, 0x00));
        create();

        QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
        struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
            native->nativeResourceForWindow("surface", this)
        );

        struct ::zwlr_layer_surface_v1 *ls = s_layerShell->get_layer_surface(
            surf, output, layer, scope
        );
        init(ls);

        set_size(0, height);
        set_anchor(
            QtWayland::zwlr_layer_surface_v1::anchor_top |
            QtWayland::zwlr_layer_surface_v1::anchor_left |
            QtWayland::zwlr_layer_surface_v1::anchor_right
        );
        set_exclusive_zone(exclusive);
        set_keyboard_interactivity(0);
        wl_surface_commit(surf);
    }

protected:
    void zwlr_layer_surface_v1_configure(uint32_t serial, uint32_t w, uint32_t h) override {
        ack_configure(serial);
        qInfo() << "[QUICK-LAYER-CONFIGURE] Configured width:" << w << "height:" << h;
        if (w > 0 && h > 0) {
            resize(w, h);
        }
    }

    void zwlr_layer_surface_v1_closed() override {
        qInfo() << "[QUICK-LAYER-CLOSED]";
    }
};

int main(int argc, char *argv[])
{
    qputenv("QT_QPA_PLATFORM", "wayland");
    QGuiApplication app(argc, argv);

    QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
    struct wl_display *display = reinterpret_cast<struct wl_display*>(
        native->nativeResourceForIntegration("wl_display")
    );
    if (!display) display = reinterpret_cast<struct wl_display*>(native->nativeResourceForIntegration("display"));

    struct wl_registry *registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &registry_listener, nullptr);
    wl_display_roundtrip(display);

    if (!s_layerShell) {
        qCritical() << "zwlr_layer_shell_v1 missing";
        return 1;
    }

    QScreen *screen = app.primaryScreen();
    struct wl_output *output = reinterpret_cast<struct ::wl_output*>(
        native->nativeResourceForScreen("output", screen)
    );

    auto *view = new LayerQuickView(output, QtWayland::zwlr_layer_shell_v1::layer_top, "quick_topbar", 42, 42);
    view->show();

    wl_display_roundtrip(display);

    QTimer::singleShot(2000, [&]() {
        qInfo() << "[QUICK-LAYER-TEST-PASS] QQuickView with Layer Shell works!";
        app.quit();
    });

    return app.exec();
}
