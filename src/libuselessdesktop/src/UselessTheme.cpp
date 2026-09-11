#include "UselessTheme.h"

#include <QFontDatabase>
#include <QFileInfo>
#include <QDir>
#include <QCoreApplication>
#include <QStyleFactory>
#include <iostream>

namespace UselessOS {

static bool s_fontsLoaded = false;

void UselessTheme::loadCustomFonts() {
    if (s_fontsLoaded) {
        return;
    }

    const QString appDir = QCoreApplication::applicationDirPath();
    const QStringList candidateDirs = {
        appDir + QStringLiteral("/fonts"),
        appDir + QStringLiteral("/../fonts"),
        appDir + QStringLiteral("/../apps/fonts"),
        appDir + QStringLiteral("/../../apps/fonts"),
        QStringLiteral("/opt/uselessos/fonts"),
        QStringLiteral("/opt/uselessos/apps/fonts")
    };

    for (const auto& dirPath : candidateDirs) {
        QDir dir(dirPath);
        if (dir.exists()) {
            const QStringList fontFiles = dir.entryList({QStringLiteral("*.otf"), QStringLiteral("*.ttf")}, QDir::Files);
            for (const auto& file : fontFiles) {
                const QString fullPath = dir.absoluteFilePath(file);
                QFontDatabase::addApplicationFont(fullPath);
            }
        }
    }

    s_fontsLoaded = true;
}

QString UselessTheme::getIconPath(const QString& filename) {
    if (filename.isEmpty()) {
        return QString();
    }

    const QString appDir = QCoreApplication::applicationDirPath();
    const QStringList candidates = {
        appDir + QStringLiteral("/assets/icons/") + filename,
        appDir + QStringLiteral("/assets/") + filename,
        appDir + QStringLiteral("/../assets/icons/") + filename,
        appDir + QStringLiteral("/../apps/assets/icons/") + filename,
        appDir + QStringLiteral("/../../apps/assets/icons/") + filename,
        QStringLiteral("/opt/uselessos/assets/icons/") + filename,
        QStringLiteral("/opt/uselessos/assets/") + filename
    };

    for (const auto& candidate : candidates) {
        if (QFileInfo::exists(candidate)) {
            return candidate;
        }
    }

    return QString();
}

QString UselessTheme::getAssetPath(const QString& filename) {
    if (filename.isEmpty()) {
        return QString();
    }

    const QString appDir = QCoreApplication::applicationDirPath();
    const QStringList candidates = {
        appDir + QStringLiteral("/assets/") + filename,
        appDir + QStringLiteral("/../assets/") + filename,
        appDir + QStringLiteral("/../apps/assets/") + filename,
        appDir + QStringLiteral("/../../apps/assets/") + filename,
        QStringLiteral("/opt/uselessos/assets/") + filename
    };

    for (const auto& candidate : candidates) {
        if (QFileInfo::exists(candidate)) {
            return candidate;
        }
    }

    return QString();
}

AppGuide UselessTheme::getAppGuide(const QString& appTitle) {
    static const QMap<QString, AppGuide> guides = {
        {
            QStringLiteral("Excuse Generator™"),
            {
                {
                    QStringLiteral("Select an excuse archetype (e.g. Spatiotemporal Anomalies, Sentient Infrastructure)."),
                    QStringLiteral("Pick the intended recipient (e.g. Direct Line Manager, Team Slack Channel)."),
                    QStringLiteral("Adjust the Absurdity Calibration slider to tune believability vs chaos."),
                    QStringLiteral("Click 'GENERATE BINDING CORPORATE EXCUSE' to produce a bullet-proof mitigation excuse.")
                },
                QStringLiteral("In hyper-productive corporate environments, honesty creates meetings. A sufficiently convoluted spatiotemporal anomaly creates profound silence and automatic PTO approval.")
            }
        },
        {
            QStringLiteral("Overthinking Engine™"),
            {
                {
                    QStringLiteral("Enter any mundane everyday decision (e.g. 'Should I reply to this email now?')."),
                    QStringLiteral("Click 'SIMULATE 14,000,605 SCENARIOS' to calculate catastrophic branch probabilities."),
                    QStringLiteral("Review the Catastrophe Confidence Index and paralysis telemetry.")
                },
                QStringLiteral("Why make a simple decision in 5 seconds when you can calculate 14 million catastrophic timelines for 4 hours and conclude that taking no action is safest?")
            }
        },
        {
            QStringLiteral("AI That Says Hmm™"),
            {
                {
                    QStringLiteral("Type any deep existential dilemma, moral question, or technical query into the input."),
                    QStringLiteral("Click 'Ask AI' or press Enter to invoke the Qwen 3.5 0.8B cognitive backend."),
                    QStringLiteral("Observe the token streaming and telemetry as it engages in profound deliberation.")
                },
                QStringLiteral("Modern LLMs hallucinate false certainty. Qwen 3.5 0.8B in UselessOS respects cosmic ambiguity: when faced with reality, the only truly honest answer is 'Hmm...'.")
            }
        },
        {
            QStringLiteral("Uselessness Analytics™"),
            {
                {
                    QStringLiteral("Observe live enterprise procrastination throughput and dopamine decay metrics."),
                    QStringLiteral("Review the Spatiotemporal Drift and Circular Logic coefficients."),
                    QStringLiteral("Click 'Run Audit' to re-certify that zero tangible value was created.")
                },
                QStringLiteral("Corporate dashboards measure output regardless of utility. Here, we measure lack of utility with enterprise rigor, proving that idleness is quantifiable science.")
            }
        },
        {
            QStringLiteral("Screen Time™"),
            {
                {
                    QStringLiteral("Monitor real-time consumption of glowing rectangle photons."),
                    QStringLiteral("Toggle between 'Existential Despair' and 'Digital Dissociation' telemetry."),
                    QStringLiteral("Click 'Log More Screen Time' to deepen your dedication to the void.")
                },
                QStringLiteral("Other screen time apps shame you into touching grass. Screen Time celebrates your loyal commitment to the phosphor glow of digital delusion.")
            }
        },
        {
            QStringLiteral("Existential Crisis Tracker™"),
            {
                {
                    QStringLiteral("Inspect telemetry: Sense of Purpose, Monday Motivation, Bloodstream Caffeine."),
                    QStringLiteral("Consult the System Recommendation (e.g. 'Have some water')."),
                    QStringLiteral("Increment the 'Why am I doing this?' counter whenever dread peaks.")
                },
                QStringLiteral("Awareness of one's cosmic insignificance is the first step toward enjoying a pointless cup of tea. We track the void so the void doesn't sneak up on you.")
            }
        },
        {
            QStringLiteral("Emotional Bin™"),
            {
                {
                    QStringLiteral("Type negative emotions, imposter syndrome, or annoying thoughts into the incinerator."),
                    QStringLiteral("Click 'DISCARD & SHRED' to watch them vanish forever into the digital incinerator.")
                },
                QStringLiteral("Closure is overrated and therapy takes time. Emotional Bin offers an unceremonious byte-level /dev/null deletion for all psychological baggage.")
            }
        },
        {
            QStringLiteral("Useless Alarm™"),
            {
                {
                    QStringLiteral("Select your desired wake-up hour (or sleep procrastination window)."),
                    QStringLiteral("Set the Snooze Permissiveness slider to maximum."),
                    QStringLiteral("Click 'Arm Alarm' — when it rings, it will politely suggest going back to sleep.")
                },
                QStringLiteral("Waking up early is a social construct. Useless Alarm believes in honoring your circadian rebellion by actively encouraging naps.")
            }
        },
        {
            QStringLiteral("System Settings"),
            {
                {
                    QStringLiteral("Navigate the macOS-style sidebar: General, Desktop, Display, Sound, Impracticality."),
                    QStringLiteral("Toggle placebos such as 'Hyper-Threading Coffee Machine' and 'Dark Mode Sarcasm'."),
                    QStringLiteral("Adjust sliders that change absolutely nothing with high precision.")
                },
                QStringLiteral("The illusion of control is the foundation of modern operating systems. Here, you have total control over settings that intentionally effect zero changes.")
            }
        },
        {
            QStringLiteral("Useless Terminal™"),
            {
                {
                    QStringLiteral("Type standard UNIX commands like 'help', 'status', 'why', 'overthink', 'sudo', or 'matrix'."),
                    QStringLiteral("Experience a terminal environment engineered to answer everything with philosophical absurdity.")
                },
                QStringLiteral("UNIX was designed for deterministic computing. Useless Terminal restores poetry to the shell prompt, proving that not all pipelines need an exit code of 0.")
            }
        }
    };

    for (auto it = guides.constBegin(); it != guides.constEnd(); ++it) {
        if (appTitle.contains(it.key(), Qt::CaseInsensitive) || it.key().contains(appTitle, Qt::CaseInsensitive)) {
            return it.value();
        }
    }

    return AppGuide{
        {
            QStringLiteral("Interact with the controls, buttons, and inputs on screen."),
            QStringLiteral("Enjoy the complete lack of measurable productivity."),
            QStringLiteral("Observe how peaceful idleness feels in an over-engineered world.")
        },
        QStringLiteral("Every application in UselessOS is an aesthetic celebration of digital futility, challenging the assumption that all software must generate shareholder value.")
    };
}

QString UselessTheme::getGlobalStylesheet() {
    return QStringLiteral(R"css(
    QWidget {
        color: #0e0e0d;
        font-family: "Helvetica", -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }
    QMainWindow, QDialog {
        background-color: #ffffff;
    }
    
    QToolTip {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 8px;
        padding: 6px 12px;
        font-family: "Helvetica", sans-serif;
        font-size: 9pt;
        font-weight: 800;
    }
    
    QGroupBox {
        border: 2px solid #0e0e0d;
        border-radius: 14px;
        margin-top: 20px;
        background-color: #ffffff;
        font-weight: 700;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 3px 14px;
        color: #0e0e0d;
        font-weight: 800;
        font-size: 10pt;
        background-color: #f5f4f0;
        border: 2px solid #0e0e0d;
        border-radius: 10px;
    }
    
    QPushButton {
        background-color: #0e0e0d;
        color: #ffffff;
        border: 2px solid #0e0e0d;
        border-radius: 20px;
        padding: 10px 22px;
        font-weight: 800;
        font-size: 10.5pt;
        font-family: "Helvetica";
    }
    QPushButton:hover {
        background-color: #ea34df;
        color: #ffffff;
        border: 2px solid #0e0e0d;
    }
    QPushButton:pressed {
        background-color: #c0326b;
    }
    QPushButton:disabled {
        background-color: #e5e5e0;
        color: #888880;
        border: 2px solid #b5b5b0;
    }
    
    QLineEdit, QTextEdit, QTimeEdit, QSpinBox {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 8px 12px;
        font-size: 10.5pt;
    }
    QComboBox {
        background-color: #ffffff;
        color: #0e0e0d;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 4px 10px;
        font-size: 10pt;
        font-weight: 700;
        min-height: 28px;
    }
    QLineEdit:focus, QTextEdit:focus, QComboBox:focus, QTimeEdit:focus, QSpinBox:focus {
        border: 2px solid #ea34df;
    }
    QComboBox::drop-down {
        border: none;
        width: 26px;
    }
    QComboBox QAbstractItemView {
        border: 2px solid #0e0e0d;
        border-radius: 8px;
        background-color: #ffffff;
        color: #0e0e0d;
        selection-background-color: #ea34df;
        selection-color: #ffffff;
        padding: 4px;
    }
    
    QSlider::groove:horizontal {
        border: 2px solid #0e0e0d;
        height: 10px;
        background: #f5f4f0;
        border-radius: 5px;
    }
    QSlider::sub-page:horizontal {
        background: #ea34df;
        border: 2px solid #0e0e0d;
        border-radius: 5px;
    }
    QSlider::handle:horizontal {
        background: #ffffff;
        border: 2px solid #0e0e0d;
        width: 22px;
        margin-top: -6px;
        margin-bottom: -6px;
        border-radius: 11px;
    }
    QSlider::handle:horizontal:hover {
        background: #0e0e0d;
    }
    
    QProgressBar {
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        text-align: center;
        background-color: #ffffff;
        color: #0e0e0d;
        font-weight: 800;
        height: 22px;
    }
    QProgressBar::chunk {
        background-color: #244638;
        border-radius: 8px;
        margin: 2px;
    }
    
    QListWidget {
        background-color: #ffffff;
        border: 2px solid #0e0e0d;
        border-radius: 12px;
        padding: 6px;
    }
    QListWidget::item {
        border-radius: 8px;
        padding: 6px 10px;
    }
    QListWidget::item:selected {
        background-color: #ea34df;
        color: #ffffff;
    }
    
    QScrollBar:vertical {
        border: 1.5px solid #0e0e0d;
        background: #f5f4f0;
        width: 10px;
        border-radius: 5px;
        margin: 4px 6px 6px 0px;
    }
    QScrollBar::handle:vertical {
        background: #0e0e0d;
        border-radius: 3px;
        min-height: 20px;
    }
    QScrollBar::handle:vertical:hover {
        background: #ea34df;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }
    QScrollBar:horizontal {
        height: 0px;
    }
    )css");
}

void UselessTheme::applyCorporateStyle(QApplication* app) {
    if (!app) {
        return;
    }

    loadCustomFonts();

    app->setStyle(QStyleFactory::create(QStringLiteral("Fusion")));

    QFont defaultFont(QStringLiteral("Helvetica"), 11);
    defaultFont.setStyleHint(QFont::SansSerif);
    app->setFont(defaultFont);

    app->setStyleSheet(getGlobalStylesheet());
}

} // namespace UselessOS
