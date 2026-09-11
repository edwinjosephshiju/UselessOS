#include <QGuiApplication>
#include <QWindow>
#include <QPainter>
#include <QBackingStore>
#include <QMouseEvent>
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

class TestEventWindow : public QWindow, public QtWayland::zwlr_layer_surface_v1 {
public:
    QBackingStore *backingStore = nullptr;
    bool clicked = false;

    TestEventWindow(struct wl_output *output) {
        setSurfaceType(QWindow::RasterSurface);
        create();
        backingStore = new QBackingStore(this);

        QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
        struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
            native->nativeResourceForWindow("surface", this)
        );

        struct ::zwlr_layer_surface_v1 *ls = s_layerShell->get_layer_surface(
            surf, output, QtWayland::zwlr_layer_shell_v1::layer_top, "event_test"
        );
        init(ls);

        set_size(400, 80);
        set_anchor(QtWayland::zwlr_layer_surface_v1::anchor_bottom);
        set_exclusive_zone(80);
        set_keyboard_interactivity(0);
        wl_surface_commit(surf);
    }

    void render() {
        QRect rect(0, 0, width(), height());
        backingStore->resize(rect.size());
        backingStore->beginPaint(rect);
        QPainter p(backingStore->paintDevice());
        p.fillRect(rect, clicked ? Qt::green : Qt::yellow);
        p.setPen(QPen(Qt::black, 3));
        p.drawRect(2, 2, width() - 4, height() - 4);
        p.drawText(rect, Qt::AlignCenter, clicked ? "CLICKED!" : "Click Me (Dock Test)");
        p.end();
        backingStore->endPaint();
        backingStore->flush(rect);
    }

protected:
    void zwlr_layer_surface_v1_configure(uint32_t serial, uint32_t w, uint32_t h) override {
        ack_configure(serial);
        if (w > 0 && h > 0) resize(w, h);
        render();
        qInfo() << "[EVENT-WIN-CONFIGURE] Size:" << width() << "x" << height();
    }

    void mousePressEvent(QMouseEvent *ev) override {
        clicked = true;
        render();
        qInfo() << "[EVENT-WIN-MOUSE] Mouse Clicked at:" << ev->pos();
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

    QScreen *screen = app.primaryScreen();
    struct wl_output *output = reinterpret_cast<struct ::wl_output*>(
        native->nativeResourceForScreen("output", screen)
    );

    auto *win = new TestEventWindow(output);
    wl_display_roundtrip(display);

    QTimer::singleShot(2500, [&]() {
        qInfo() << "[PASS] Layer Surface window event loop active and responsive.";
        app.quit();
    });

    return app.exec();
}
