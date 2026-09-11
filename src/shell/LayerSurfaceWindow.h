#pragma once

#include <QWindow>
#include <QBackingStore>
#include <QPainter>
#include <QScreen>
#include <QString>
#include <wayland-client.h>

#include "qwayland-wlr-layer-shell-unstable-v1.h"

namespace UselessOS {

class LayerSurfaceWindow : public QWindow, public QtWayland::zwlr_layer_surface_v1 {
    Q_OBJECT
public:
    LayerSurfaceWindow(QScreen *targetScreen, const QString &scopeName);
    ~LayerSurfaceWindow() override;

    void setupLayerSurface(QtWayland::zwlr_layer_shell_v1 *shell,
                           uint32_t layer,
                           int width,
                           int height,
                           uint32_t anchorMask,
                           int exclusiveZone,
                           uint32_t keyboardInteractivity = 0);

    void requestRepaint();

protected:
    virtual void paint(QPainter &painter) = 0;
    virtual void onConfigured(uint32_t width, uint32_t height) { Q_UNUSED(width); Q_UNUSED(height); }

    // Wayland layer surface callbacks
    void zwlr_layer_surface_v1_configure(uint32_t serial, uint32_t w, uint32_t h) override;
    void zwlr_layer_surface_v1_closed() override;

    // QWindow event overrides
    void exposeEvent(QExposeEvent *ev) override;
    void resizeEvent(QResizeEvent *ev) override;

    QBackingStore *m_backingStore = nullptr;
    QString m_scopeName;
    int m_exclusiveZone = 0;
    bool m_isConfigured = false;
};

} // namespace UselessOS
