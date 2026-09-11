#include "WindowTracker.h"
#include <QDebug>
#include <algorithm>

namespace UselessOS {

WindowItem::WindowItem(struct ::org_kde_plasma_window *win, const QString &id, uint32_t rawId, QObject *parent)
    : QObject(parent)
    , uuid(id)
    , internalId(rawId)
{
    init(win);
}

WindowItem::~WindowItem()
{
    if (isInitialized()) {
        destroy();
    }
}

void WindowItem::org_kde_plasma_window_title_changed(const QString &newTitle)
{
    title = newTitle;
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_app_id_changed(const QString &newAppId)
{
    appId = newAppId;
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_resource_name_changed(const QString &resName)
{
    resourceName = resName;
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_pid_changed(uint32_t newPid)
{
    pid = static_cast<int>(newPid);
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_state_changed(uint32_t flags)
{
    isActive = (flags & QtWayland::org_kde_plasma_window_management::state_active);
    isMinimized = (flags & QtWayland::org_kde_plasma_window_management::state_minimized);
    isMaximized = (flags & QtWayland::org_kde_plasma_window_management::state_maximized);
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_virtual_desktop_entered(const QString &id)
{
    virtualDesktop = id;
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_virtual_desktop_left(const QString &)
{
    virtualDesktop.clear();
    Q_EMIT updated(uuid);
}

void WindowItem::org_kde_plasma_window_unmapped()
{
    Q_EMIT closed(uuid);
}

// ==============================================================================
// WindowTracker Implementation
// ==============================================================================

WindowTracker::WindowTracker(struct wl_display *display, struct wl_registry *registry, uint32_t id, int version, QObject *parent)
    : QAbstractListModel(parent)
    , m_display(display)
{
    init(registry, id, version);

    // Establish asynchronous Wayland dispatching via QSocketNotifier
    if (m_display) {
        int waylandFd = wl_display_get_fd(m_display);
        m_notifier = new QSocketNotifier(waylandFd, QSocketNotifier::Read, this);
        connect(m_notifier, &QSocketNotifier::activated, this, [this]() {
            wl_display_dispatch(m_display);
        });
    }

    qInfo() << "[WindowTracker] Initialized native org_kde_plasma_window_management v" << version;
}

WindowTracker::~WindowTracker()
{
    qDeleteAll(m_windowItems);
    m_windowItems.clear();
}

int WindowTracker::rowCount(const QModelIndex &parent) const
{
    if (parent.isValid()) return 0;
    return m_windows.size();
}

QVariant WindowTracker::data(const QModelIndex &index, int role) const
{
    if (!index.isValid() || index.row() < 0 || index.row() >= m_windows.size()) {
        return QVariant();
    }

    const auto &win = m_windows.at(index.row());
    switch (role) {
    case UuidRole: return win.uuid;
    case InternalIdRole: return win.internalId;
    case TitleRole: return win.title;
    case AppIdRole: return win.appId;
    case ResourceNameRole: return win.resourceName;
    case PidRole: return win.pid;
    case IsActiveRole: return win.isActive;
    case IsMinimizedRole: return win.isMinimized;
    case IsMaximizedRole: return win.isMaximized;
    case VirtualDesktopRole: return win.virtualDesktop;
    default: break;
    }
    return QVariant();
}

QHash<int, QByteArray> WindowTracker::roleNames() const
{
    QHash<int, QByteArray> roles;
    roles[UuidRole] = "uuid";
    roles[InternalIdRole] = "internalId";
    roles[TitleRole] = "title";
    roles[AppIdRole] = "appId";
    roles[ResourceNameRole] = "resourceName";
    roles[PidRole] = "pid";
    roles[IsActiveRole] = "isActive";
    roles[IsMinimizedRole] = "isMinimized";
    roles[IsMaximizedRole] = "isMaximized";
    roles[VirtualDesktopRole] = "virtualDesktop";
    return roles;
}

QString WindowTracker::activeWindowUuid() const
{
    return m_activeUuid;
}

QString WindowTracker::activeWindowTitle() const
{
    const WindowEntry *win = findWindow(m_activeUuid);
    return win ? win->title : QString();
}

QString WindowTracker::activeWindowAppId() const
{
    const WindowEntry *win = findWindow(m_activeUuid);
    return win ? win->appId : QString();
}

int WindowTracker::windowCount() const
{
    return m_windows.size();
}

const WindowEntry* WindowTracker::findWindow(const QString &uuid) const
{
    for (const auto &win : m_windows) {
        if (win.uuid == uuid) return &win;
    }
    return nullptr;
}

int WindowTracker::indexOfUuid(const QString &uuid) const
{
    for (int i = 0; i < m_windows.size(); ++i) {
        if (m_windows.at(i).uuid == uuid) return i;
    }
    return -1;
}

void WindowTracker::activateWindow(const QString &uuid)
{
    if (m_windowItems.contains(uuid)) {
        m_windowItems[uuid]->set_state(
            QtWayland::org_kde_plasma_window_management::state_active,
            QtWayland::org_kde_plasma_window_management::state_active
        );
        if (m_display) wl_display_flush(m_display);
    }
}

void WindowTracker::minimizeWindow(const QString &uuid)
{
    if (m_windowItems.contains(uuid)) {
        m_windowItems[uuid]->set_state(
            QtWayland::org_kde_plasma_window_management::state_minimized,
            QtWayland::org_kde_plasma_window_management::state_minimized
        );
        if (m_display) wl_display_flush(m_display);
    }
}

void WindowTracker::restoreWindow(const QString &uuid)
{
    if (m_windowItems.contains(uuid)) {
        m_windowItems[uuid]->set_state(
            QtWayland::org_kde_plasma_window_management::state_minimized,
            0
        );
        if (m_display) wl_display_flush(m_display);
    }
}

void WindowTracker::toggleMinimize(const QString &uuid)
{
    const WindowEntry *entry = findWindow(uuid);
    if (!entry) return;

    if (entry->isActive && !entry->isMinimized) {
        minimizeWindow(uuid);
    } else if (entry->isMinimized) {
        restoreWindow(uuid);
        activateWindow(uuid);
    } else {
        activateWindow(uuid);
    }
}

void WindowTracker::closeWindow(const QString &uuid)
{
    if (m_windowItems.contains(uuid)) {
        m_windowItems[uuid]->close();
        if (m_display) wl_display_flush(m_display);
    }
}

void WindowTracker::org_kde_plasma_window_management_window_with_uuid(uint32_t id, const QString &uuid)
{
    struct ::org_kde_plasma_window *rawWin = get_window_by_uuid(uuid);
    if (!rawWin) {
        rawWin = get_window(id);
    }
    if (rawWin) {
        registerWindow(rawWin, uuid, id);
    }
}

void WindowTracker::org_kde_plasma_window_management_window(uint32_t id)
{
    QString synthUuid = QString("win-%1").arg(id);
    if (!m_windowItems.contains(synthUuid)) {
        struct ::org_kde_plasma_window *rawWin = get_window(id);
        if (rawWin) {
            registerWindow(rawWin, synthUuid, id);
        }
    }
}

void WindowTracker::registerWindow(struct ::org_kde_plasma_window *rawWin, const QString &uuid, uint32_t internalId)
{
    if (m_windowItems.contains(uuid)) return;

    auto *item = new WindowItem(rawWin, uuid, internalId, this);
    m_windowItems.insert(uuid, item);

    WindowEntry entry;
    entry.uuid = uuid;
    entry.internalId = internalId;

    int newRow = m_windows.size();
    beginInsertRows(QModelIndex(), newRow, newRow);
    m_windows.append(entry);
    endInsertRows();

    connect(item, &WindowItem::updated, this, &WindowTracker::handleWindowUpdated);
    connect(item, &WindowItem::closed, this, &WindowTracker::handleWindowClosed);

    Q_EMIT countChanged(m_windows.size());
    Q_EMIT windowAdded(uuid, entry.title);
}

void WindowTracker::handleWindowUpdated(const QString &uuid)
{
    int row = indexOfUuid(uuid);
    if (row < 0 || !m_windowItems.contains(uuid)) return;

    auto *item = m_windowItems[uuid];
    auto &entry = m_windows[row];

    entry.title = item->title;
    entry.appId = item->appId;
    entry.resourceName = item->resourceName;
    entry.pid = item->pid;
    entry.isActive = item->isActive;
    entry.isMinimized = item->isMinimized;
    entry.isMaximized = item->isMaximized;
    entry.virtualDesktop = item->virtualDesktop;

    QModelIndex idx = index(row);
    Q_EMIT dataChanged(idx, idx);
    Q_EMIT windowUpdated(uuid);

    if (entry.isActive && m_activeUuid != uuid) {
        m_activeUuid = uuid;
        Q_EMIT activeWindowChanged(m_activeUuid, entry.title);
    } else if (!entry.isActive && m_activeUuid == uuid) {
        m_activeUuid.clear();
        Q_EMIT activeWindowChanged(QString(), QString());
    }
}

void WindowTracker::handleWindowClosed(const QString &uuid)
{
    int row = indexOfUuid(uuid);
    if (row >= 0) {
        beginRemoveRows(QModelIndex(), row, row);
        m_windows.removeAt(row);
        endRemoveRows();
    }

    if (m_windowItems.contains(uuid)) {
        m_windowItems.take(uuid)->deleteLater();
    }

    if (m_activeUuid == uuid) {
        m_activeUuid.clear();
        Q_EMIT activeWindowChanged(QString(), QString());
    }

    Q_EMIT countChanged(m_windows.size());
    Q_EMIT windowRemoved(uuid);
}

} // namespace UselessOS
