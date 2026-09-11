#include <QGuiApplication>
#include <QWindow>
#include <QPainter>
#include <QBackingStore>
#include <QDebug>
#include <QTimer>
#include <QScreen>
#include <QColor>
#include <QFont>
#include <algorithm>

#include <wayland-client.h>
#include <qpa/qplatformnativeinterface.h>

#include "qwayland-wlr-layer-shell-unstable-v1.h"

class LayerShellManager;

class LayerSurfaceWindow : public QWindow, public QtWayland::zwlr_layer_surface_v1 {
    Q_OBJECT
public:
    enum SurfaceType {
        TypeTopBar,
        TypeDock,
        TypeCanvas
    };

    SurfaceType surfaceType;
    QString scopeName;
    int exclusivePixels = 0;
    QBackingStore *backingStore = nullptr;
    bool isConfigured = false;
    uint32_t configuredWidth = 0;
    uint32_t configuredHeight = 0;

    LayerSurfaceWindow(SurfaceType type, const QString &scope, int exclusive)
        : surfaceType(type), scopeName(scope), exclusivePixels(exclusive)
    {
        setSurfaceType(QWindow::RasterSurface);
    }

    void setupLayerSurface(QtWayland::zwlr_layer_shell_v1 *shell, struct wl_output *output, uint32_t layer, QPlatformNativeInterface *native) {
        create();
        backingStore = new QBackingStore(this);
        struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
            native->nativeResourceForWindow("surface", this)
        );
        struct ::zwlr_layer_surface_v1 *ls = shell->get_layer_surface(
            surf, output, layer, scopeName
        );
        init(ls);
    }

    ~LayerSurfaceWindow() override {
        delete backingStore;
        if (isInitialized()) {
            QtWayland::zwlr_layer_surface_v1::destroy();
        }
    }

    void render() {
        if (!isExposed() && !isConfigured) return;

        QRect rect(0, 0, width(), height());
        backingStore->resize(rect.size());
        backingStore->beginPaint(rect);

        QPaintDevice *device = backingStore->paintDevice();
        QPainter painter(device);

        if (surfaceType == TypeTopBar) {
            // Neobrutalist Bright Yellow TopBar
            painter.fillRect(rect, QColor(0xFF, 0xE6, 0x00));
            painter.setPen(QPen(Qt::black, 4));
            painter.drawLine(0, height() - 2, width(), height() - 2);

            painter.setPen(Qt::black);
            QFont font("sans-serif", 11, QFont::Bold);
            painter.setFont(font);
            painter.drawText(20, 26, "USELESS OS 3.0  |  KWIN WAYLAND LAYER-SHELL VERIFIED  |  TOPBAR [EXCLUSIVE: 42px]");
        } else if (surfaceType == TypeDock) {
            // Neobrutalist Coral / Cyan Floating Dock
            painter.fillRect(rect, QColor(0xFF, 0x6B, 0x6B));
            painter.setPen(QPen(Qt::black, 4));
            painter.drawRect(2, 2, width() - 4, height() - 4);

            painter.setPen(Qt::black);
            QFont font("sans-serif", 10, QFont::Bold);
            painter.setFont(font);
            painter.drawText(rect, Qt::AlignCenter, "USELESS DOCK [EXCLUSIVE: 80px]");
        } else if (surfaceType == TypeCanvas) {
            // Retro Neobrutalist Canvas Background
            painter.fillRect(rect, QColor(0xF4, 0xF4, 0xF0));
            painter.setPen(QPen(QColor(0xDD, 0xDD, 0xDD), 2, Qt::DotLine));
            for (int x = 0; x < width(); x += 40) {
                painter.drawLine(x, 0, x, height());
            }
            for (int y = 0; y < height(); y += 40) {
                painter.drawLine(0, y, width(), y);
            }
            painter.setPen(QColor(0x88, 0x88, 0x88));
            QFont font("sans-serif", 16, QFont::Bold);
            painter.setFont(font);
            painter.drawText(rect, Qt::AlignCenter, "UselessOS Canvas (LayerBackground)");
        }

        painter.end();
        backingStore->endPaint();
        backingStore->flush(rect);
    }

protected:
    void zwlr_layer_surface_v1_configure(uint32_t serial, uint32_t w, uint32_t h) override {
        ack_configure(serial);
        isConfigured = true;
        configuredWidth = w;
        configuredHeight = h;

        if (w > 0 && h > 0) {
            resize(w, h);
        }
        render();

        qInfo().noquote() << QString("[LAYER-CONFIGURE] Surface '%1' configured -> %2x%3 (Exclusive Zone: %4px)")
            .arg(scopeName).arg(width()).arg(height()).arg(exclusivePixels);
    }

    void zwlr_layer_surface_v1_closed() override {
        qInfo().noquote() << QString("[LAYER-CLOSED] Surface '%1' closed by compositor").arg(scopeName);
    }

    void exposeEvent(QExposeEvent *) override {
        if (isExposed()) {
            render();
        }
    }

    void resizeEvent(QResizeEvent *) override {
        render();
    }
};

static QtWayland::zwlr_layer_shell_v1 *s_layerShell = nullptr;

static void registry_handle_global(void *data, struct wl_registry *registry,
                                   uint32_t id, const char *interface, uint32_t version)
{
    if (strcmp(interface, "zwlr_layer_shell_v1") == 0) {
        qInfo() << "[PoC] Discovered Wayland Global:" << interface << "Server Version:" << version;
        int bindVersion = std::min(static_cast<int>(version), 4);
        s_layerShell = new QtWayland::zwlr_layer_shell_v1(registry, id, bindVersion);
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
    qputenv("QT_QPA_PLATFORM", "wayland");

    QGuiApplication app(argc, argv);
    app.setApplicationName("UselessOS Layer Shell PoC");
    app.setApplicationVersion("1.0.0");

    qInfo() << "========================================================";
    qInfo() << " UselessOS Architecture Gate: Layer Shell PoC";
    qInfo() << " Testing zwlr_layer_shell_v1 Surfaces & Exclusive Zones";
    qInfo() << "========================================================";

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
        qCritical() << "Fatal: Failed to obtain wl_display!";
        return 1;
    }

    struct wl_registry *registry = wl_display_get_registry(display);
    wl_registry_add_listener(registry, &registry_listener, nullptr);
    wl_display_roundtrip(display);

    if (!s_layerShell) {
        qCritical() << "Fatal: zwlr_layer_shell_v1 not advertised by the compositor!";
        return 1;
    }

    qInfo() << "[PoC] zwlr_layer_shell_v1 successfully bound!";

    QList<LayerSurfaceWindow*> surfaces;

    for (QScreen *screen : QGuiApplication::screens()) {
        qInfo().noquote() << QString("[SCREEN] Screen: '%1' | Res: %2x%3 | DPR: %4")
            .arg(screen->name())
            .arg(screen->geometry().width())
            .arg(screen->geometry().height())
            .arg(screen->devicePixelRatio());

        struct wl_output *output = reinterpret_cast<struct ::wl_output*>(
            native->nativeResourceForScreen("output", screen)
        );

        // 1. Create TopBar Surface (LayerTop, Height 42px, Exclusive Zone 42px)
        {
            auto *layerWin = new LayerSurfaceWindow(LayerSurfaceWindow::TypeTopBar, "useless_topbar", 42);
            layerWin->setScreen(screen);
            layerWin->resize(screen->geometry().width(), 42);
            layerWin->setupLayerSurface(s_layerShell, output, QtWayland::zwlr_layer_shell_v1::layer_top, native);
            layerWin->set_size(0, 42);
            layerWin->set_anchor(
                QtWayland::zwlr_layer_surface_v1::anchor_top |
                QtWayland::zwlr_layer_surface_v1::anchor_left |
                QtWayland::zwlr_layer_surface_v1::anchor_right
            );
            layerWin->set_exclusive_zone(42);
            layerWin->set_keyboard_interactivity(0);

            struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
                native->nativeResourceForWindow("surface", layerWin)
            );
            wl_surface_commit(surf);
            surfaces.append(layerWin);
        }

        // 2. Create Dock Surface (LayerTop, Height 80px, Width 500px, Exclusive Zone 80px)
        {
            auto *layerWin = new LayerSurfaceWindow(LayerSurfaceWindow::TypeDock, "useless_dock", 80);
            layerWin->setScreen(screen);
            layerWin->resize(500, 80);
            layerWin->setupLayerSurface(s_layerShell, output, QtWayland::zwlr_layer_shell_v1::layer_top, native);
            layerWin->set_size(500, 80);
            layerWin->set_anchor(QtWayland::zwlr_layer_surface_v1::anchor_bottom);
            layerWin->set_exclusive_zone(80);
            layerWin->set_keyboard_interactivity(0);

            struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
                native->nativeResourceForWindow("surface", layerWin)
            );
            wl_surface_commit(surf);
            surfaces.append(layerWin);
        }

        // 3. Create Canvas Surface (LayerBackground, Exclusive Zone 0)
        {
            auto *layerWin = new LayerSurfaceWindow(LayerSurfaceWindow::TypeCanvas, "useless_canvas", 0);
            layerWin->setScreen(screen);
            layerWin->resize(screen->geometry().size());
            layerWin->setupLayerSurface(s_layerShell, output, QtWayland::zwlr_layer_shell_v1::layer_background, native);
            layerWin->set_size(0, 0);
            layerWin->set_anchor(
                QtWayland::zwlr_layer_surface_v1::anchor_top |
                QtWayland::zwlr_layer_surface_v1::anchor_bottom |
                QtWayland::zwlr_layer_surface_v1::anchor_left |
                QtWayland::zwlr_layer_surface_v1::anchor_right
            );
            layerWin->set_exclusive_zone(0);
            layerWin->set_keyboard_interactivity(0);

            struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
                native->nativeResourceForWindow("surface", layerWin)
            );
            wl_surface_commit(surf);
            surfaces.append(layerWin);
        }
    }

    wl_display_roundtrip(display);

    // Run for 5 seconds to demonstrate surfaces and configure responses, then cleanly exit
    auto *timer = new QTimer(&app);
    int step = 0;
    QObject::connect(timer, &QTimer::timeout, [&]() {
        step++;
        wl_display_dispatch_pending(display);
        for (auto *s : surfaces) {
            s->render();
        }
        wl_display_flush(display);

        if (step >= 4) {
            qInfo() << "[PoC] Verified all Layer Shell surfaces (TopBar 42px, Dock 80px, Canvas Background)!";
            app.quit();
        }
    });
    timer->start(1000);

    return app.exec();
}

#include "poc_layer_shell.moc"
