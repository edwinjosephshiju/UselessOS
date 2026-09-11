#pragma once

#include <QString>
#include <QStringList>
#include <QColor>
#include <QMap>
#include <QFont>
#include <QApplication>

namespace UselessOS {

/**
 * @brief Neobrutalist design tokens and global palette constants for UselessOS.
 */
namespace Colors {
    inline const QString InkBlack        = QStringLiteral("#0e0e0d");
    inline const QString BrutalistPink   = QStringLiteral("#ea34df");
    inline const QString NeonCyan        = QStringLiteral("#00c2cb");
    inline const QString BackgroundLight = QStringLiteral("#f5f4f0");
    inline const QString CardWhite       = QStringLiteral("#ffffff");
    inline const QString CorporateGreen  = QStringLiteral("#244638");
    inline const QString AccentRed       = QStringLiteral("#e82803");

    // macOS traffic light buttons
    inline const QString TrafficCloseBg   = QStringLiteral("#ff5f56");
    inline const QString TrafficCloseHov  = QStringLiteral("#5c0000");
    inline const QString TrafficMinBg     = QStringLiteral("#ffbd2e");
    inline const QString TrafficMinHov    = QStringLiteral("#5c3b00");
    inline const QString TrafficMaxBg     = QStringLiteral("#27c93f");
    inline const QString TrafficMaxHov    = QStringLiteral("#004d10");
}

/**
 * @brief Philosophical and instructional documentation metadata for applications.
 */
struct AppGuide {
    QStringList howToUse;
    QString philosophy;
};

class UselessTheme {
public:
    /**
     * @brief Loads custom typography (NanumPenScript, Helvetica, Drowner) into QFontDatabase.
     */
    static void loadCustomFonts();

    /**
     * @brief Resolves full absolute path to an icon asset.
     */
    static QString getIconPath(const QString& filename);

    /**
     * @brief Resolves full absolute path to a general asset (SVG, PNG).
     */
    static QString getAssetPath(const QString& filename);

    /**
     * @brief Retrieves the application instruction guide and philosophical manifesto.
     */
    static AppGuide getAppGuide(const QString& appTitle);

    /**
     * @brief Applies global fusion theme, brutalist stylesheet, and high-DPI attributes.
     */
    static void applyCorporateStyle(QApplication* app);

    /**
     * @brief Returns global Neobrutalist QSS stylesheet string.
     */
    static QString getGlobalStylesheet();
};

} // namespace UselessOS
