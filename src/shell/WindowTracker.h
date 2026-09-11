#pragma once

#include <QAbstractListModel>
#include <QString>
#include <QMap>
#include <QVector>
#include <QObject>
#include <QSocketNotifier>
#include <wayland-client.h>

#include "qwayland-plasma-window-management.h"

namespace UselessOS {

struct WindowEntry {
    QString uuid;
    uint32_t internalId = 0;
    QString title;
    QString appId;
    QString resourceName;
    int pid = 0;
    bool isActive = false;
    bool isMinimized = false;
    bool isMaximized = false;
    QString virtualDesktop;
};

class WindowItem;

class WindowTracker : public QAbstractListModel, public QtWayland::org_kde_plasma_window_management {
    Q_OBJECT
    Q_PROPERTY(QString activeWindowUuid READ activeWindowUuid NOTIFY activeWindowChanged)
    Q_PROPERTY(QString activeWindowTitle READ activeWindowTitle NOTIFY activeWindowChanged)
    Q_PROPERTY(QString activeWindowAppId READ activeWindowAppId NOTIFY activeWindowChanged)
    Q_PROPERTY(int windowCount READ windowCount NOTIFY countChanged)

public:
    enum WindowRoles {
        UuidRole = Qt::UserRole + 1,
        InternalIdRole,
        TitleRole,
        AppIdRole,
        ResourceNameRole,
        PidRole,
        IsActiveRole,
        IsMinimizedRole,
        IsMaximizedRole,
        VirtualDesktopRole
    };
    Q_ENUM(WindowRoles)

    explicit WindowTracker(struct wl_display *display, struct wl_registry *registry, uint32_t id, int version, QObject *parent = nullptr);
    ~WindowTracker() override;

    // QAbstractListModel interface
    int rowCount(const QModelIndex &parent = QModelIndex()) const override;
    QVariant data(const QModelIndex &index, int role = Qt::DisplayRole) const override;
    QHash<int, QByteArray> roleNames() const override;

    // Properties
    QString activeWindowUuid() const;
    QString activeWindowTitle() const;
    QString activeWindowAppId() const;
    int windowCount() const;

    const QVector<WindowEntry>& windows() const { return m_windows; }
    const WindowEntry* findWindow(const QString &uuid) const;

    // Window Management Operations (invokable from UI and QML)
    Q_INVOKABLE void activateWindow(const QString &uuid);
    Q_INVOKABLE void minimizeWindow(const QString &uuid);
    Q_INVOKABLE void restoreWindow(const QString &uuid);
    Q_INVOKABLE void toggleMinimize(const QString &uuid);
    Q_INVOKABLE void closeWindow(const QString &uuid);

Q_SIGNALS:
    void activeWindowChanged(const QString &uuid, const QString &title);
    void windowAdded(const QString &uuid, const QString &title);
    void windowRemoved(const QString &uuid);
    void windowUpdated(const QString &uuid);
    void countChanged(int count);

protected:
    void org_kde_plasma_window_management_window_with_uuid(uint32_t id, const QString &uuid) override;
    void org_kde_plasma_window_management_window(uint32_t id) override;

private:
    void registerWindow(struct ::org_kde_plasma_window *rawWin, const QString &uuid, uint32_t internalId);
    void handleWindowUpdated(const QString &uuid);
    void handleWindowClosed(const QString &uuid);
    int indexOfUuid(const QString &uuid) const;

    struct wl_display *m_display = nullptr;
    QSocketNotifier *m_notifier = nullptr;
    QVector<WindowEntry> m_windows;
    QMap<QString, WindowItem*> m_windowItems;
    QString m_activeUuid;
};

class WindowItem : public QObject, public QtWayland::org_kde_plasma_window {
    Q_OBJECT
public:
    QString uuid;
    uint32_t internalId = 0;
    QString title;
    QString appId;
    QString resourceName;
    int pid = 0;
    bool isActive = false;
    bool isMinimized = false;
    bool isMaximized = false;
    QString virtualDesktop;

    WindowItem(struct ::org_kde_plasma_window *win, const QString &id, uint32_t rawId, QObject *parent = nullptr);
    ~WindowItem() override;

Q_SIGNALS:
    void updated(const QString &uuid);
    void closed(const QString &uuid);

protected:
    void org_kde_plasma_window_title_changed(const QString &newTitle) override;
    void org_kde_plasma_window_app_id_changed(const QString &newAppId) override;
    void org_kde_plasma_window_resource_name_changed(const QString &resName) override;
    void org_kde_plasma_window_pid_changed(uint32_t newPid) override;
    void org_kde_plasma_window_state_changed(uint32_t flags) override;
    void org_kde_plasma_window_virtual_desktop_entered(const QString &id) override;
    void org_kde_plasma_window_virtual_desktop_left(const QString &id) override;
    void org_kde_plasma_window_unmapped() override;
};

} // namespace UselessOS
