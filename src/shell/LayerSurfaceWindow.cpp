#include "LayerSurfaceWindow.h"
#include <QGuiApplication>
#include <QDebug>
#include <qpa/qplatformnativeinterface.h>

namespace UselessOS {

LayerSurfaceWindow::LayerSurfaceWindow(QScreen *targetScreen, const QString &scopeName)
    : m_scopeName(scopeName)
{
    setSurfaceType(QWindow::RasterSurface);
    if (targetScreen) {
        setScreen(targetScreen);
    }
}

LayerSurfaceWindow::~LayerSurfaceWindow()
{
    delete m_backingStore;
    if (isInitialized()) {
        QtWayland::zwlr_layer_surface_v1::destroy();
    }
}

void LayerSurfaceWindow::setupLayerSurface(QtWayland::zwlr_layer_shell_v1 *shell,
                                           uint32_t layer,
                                           int width,
                                           int height,
                                           uint32_t anchorMask,
                                           int exclusiveZone,
                                           uint32_t keyboardInteractivity)
{
    m_exclusiveZone = exclusiveZone;

    create();
    m_backingStore = new QBackingStore(this);

    QPlatformNativeInterface *native = QGuiApplication::platformNativeInterface();
    if (!native) {
        qWarning() << "[LayerSurfaceWindow] QPlatformNativeInterface unavailable!";
        return;
    }

    struct wl_surface *surf = reinterpret_cast<struct wl_surface*>(
        native->nativeResourceForWindow("surface", this)
    );
    if (!surf) {
        qWarning() << "[LayerSurfaceWindow] Failed to get wl_surface for" << m_scopeName;
        return;
    }

    struct wl_output *output = nullptr;
    if (screen()) {
        output = reinterpret_cast<struct wl_output*>(
            native->nativeResourceForScreen("output", screen())
        );
    }

    struct ::zwlr_layer_surface_v1 *ls = shell->get_layer_surface(
        surf, output, layer, m_scopeName
    );
    init(ls);

    set_size(static_cast<uint32_t>(std::max(0, width)), static_cast<uint32_t>(std::max(0, height)));
    set_anchor(anchorMask);
    set_exclusive_zone(exclusiveZone);
    set_keyboard_interactivity(keyboardInteractivity);

    wl_surface_commit(surf);
}

void LayerSurfaceWindow::zwlr_layer_surface_v1_configure(uint32_t serial, uint32_t w, uint32_t h)
{
    ack_configure(serial);
    m_isConfigured = true;

    if (w > 0 && h > 0 && (w != static_cast<uint32_t>(width()) || h != static_cast<uint32_t>(height()))) {
        resize(w, h);
    }

    onConfigured(width(), height());
    requestRepaint();
}

void LayerSurfaceWindow::zwlr_layer_surface_v1_closed()
{
    qInfo() << "[LayerSurfaceWindow] Surface closed by compositor:" << m_scopeName;
}

void LayerSurfaceWindow::exposeEvent(QExposeEvent *)
{
    if (isExposed()) {
        requestRepaint();
    }
}

void LayerSurfaceWindow::resizeEvent(QResizeEvent *)
{
    requestRepaint();
}

void LayerSurfaceWindow::requestRepaint()
{
    if (!m_backingStore || !m_isConfigured) return;

    QRect rect(0, 0, width(), height());
    m_backingStore->resize(rect.size());
    m_backingStore->beginPaint(rect);

    QPaintDevice *device = m_backingStore->paintDevice();
    if (device) {
        QPainter painter(device);
        paint(painter);
        painter.end();
    }

    m_backingStore->endPaint();
    m_backingStore->flush(rect);
}

} // namespace UselessOS
