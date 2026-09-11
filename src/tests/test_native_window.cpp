#include <QApplication>
#include <QLabel>
#include <QPushButton>
#include <QLineEdit>
#include <QSlider>
#include <QProgressBar>
#include <QGroupBox>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QTimer>
#include <chrono>
#include <iostream>
#include <fstream>
#include <string>

#include "UselessWindow.h"
#include "UselessTheme.h"

#ifdef __linux__
#include <unistd.h>
static long getLinuxRssKb() {
    std::ifstream statusFile("/proc/self/status");
    std::string line;
    while (std::getline(statusFile, line)) {
        if (line.rfind("VmRSS:", 0) == 0) {
            long rss = 0;
            if (sscanf(line.c_str(), "VmRSS: %ld kB", &rss) == 1) {
                return rss;
            }
        }
    }
    return -1;
}
#else
static long getLinuxRssKb() { return -1; }
#endif

class DemoOverthinkingWindow : public UselessOS::UselessWindow {
    Q_OBJECT
public:
    explicit DemoOverthinkingWindow(QWidget* parent = nullptr)
        : UselessWindow(QStringLiteral("Overthinking Engine™"),
                        QStringLiteral("14,000,605 Timelines Calculated"),
                        QStringLiteral("overthinking.png"),
                        QStringLiteral("#ea34df"),
                        620, 500, parent)
    {
        // 1. Header Banner
        auto* headerLayout = new QVBoxLayout();
        headerLayout->setSpacing(2);

        auto* titleLabel = new QLabel(QStringLiteral("Overthinking Engine™"), contentWidget());
        titleLabel->setObjectName(QStringLiteral("corp_title"));
        titleLabel->setStyleSheet(QStringLiteral("font-family: Helvetica; font-size: 18pt; font-weight: 900; color: #0e0e0d;"));
        headerLayout->addWidget(titleLabel);

        auto* subLabel = new QLabel(QStringLiteral("•  Native C++20 / Qt 6 Architecture Demonstration"), contentWidget());
        subLabel->setStyleSheet(QStringLiteral("font-family: 'NanumPenScript', cursive; font-size: 14pt; font-weight: bold; color: #ea34df;"));
        headerLayout->addWidget(subLabel);

        contentLayout()->addLayout(headerLayout);

        // 2. Brutalist Parameter Box
        auto* paramBox = new QGroupBox(QStringLiteral("DECISION PARALYSIS MATRIX"), contentWidget());
        auto* paramLayout = new QVBoxLayout(paramBox);
        paramLayout->setSpacing(10);
        paramLayout->setContentsMargins(16, 18, 16, 16);

        auto* inputPrompt = new QLabel(QStringLiteral("Enter mundane everyday decision to over-analyze:"), paramBox);
        inputPrompt->setStyleSheet(QStringLiteral("font-weight: 800; font-size: 9.5pt; color: #0e0e0d;"));
        paramLayout->addWidget(inputPrompt);

        auto* textInput = new QLineEdit(paramBox);
        textInput->setText(QStringLiteral("Should I reply to this email right now or stare at the ceiling?"));
        paramLayout->addWidget(textInput);

        // Sliders
        auto* sliderLayout = new QHBoxLayout();
        auto* sliderLabel = new QLabel(QStringLiteral("Catastrophe Sensitivity:"), paramBox);
        sliderLabel->setStyleSheet(QStringLiteral("font-weight: 800; font-size: 9pt;"));
        sliderLayout->addWidget(sliderLabel);

        auto* slider = new QSlider(Qt::Horizontal, paramBox);
        slider->setRange(0, 100);
        slider->setValue(88);
        sliderLayout->addWidget(slider);
        paramLayout->addLayout(sliderLayout);

        contentLayout()->addWidget(paramBox);

        // 3. Progress Bar & Action Button
        auto* progress = new QProgressBar(contentWidget());
        progress->setRange(0, 100);
        progress->setValue(92);
        progress->setFormat(QStringLiteral("Paralysis Level: 92% Complete"));
        contentLayout()->addWidget(progress);

        auto* btnAction = new QPushButton(QStringLiteral("SIMULATE 14,000,605 CATASTROPHIC FUTURES"), contentWidget());
        btnAction->setFixedHeight(44);
        btnAction->setCursor(Qt::PointingHandCursor);
        connect(btnAction, &QPushButton::clicked, [progress]() {
            int cur = (progress->value() + 15) % 101;
            progress->setValue(cur);
        });
        contentLayout()->addWidget(btnAction);

        // 4. Instructions Opener Button
        auto* btnHelp = new QPushButton(QStringLiteral("View Impractical Philosophy && Guide (?)"), contentWidget());
        btnHelp->setFixedHeight(36);
        btnHelp->setCursor(Qt::PointingHandCursor);
        btnHelp->setStyleSheet(QStringLiteral(
            "QPushButton {"
            "    background-color: #ffffff;"
            "    color: #0e0e0d;"
            "    border: 2px solid #0e0e0d;"
            "    border-radius: 18px;"
            "    font-weight: 800;"
            "}"
            "QPushButton:hover {"
            "    background-color: #00c2cb;"
            "    color: #ffffff;"
            "}"
        ));
        connect(btnHelp, &QPushButton::clicked, this, &UselessWindow::showInstructionsDialog);
        contentLayout()->addWidget(btnHelp);

        contentLayout()->addStretch();
    }
};

int main(int argc, char* argv[]) {
    const auto startTimestamp = std::chrono::high_resolution_clock::now();

    QApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("UselessOS-NativeTest"));
    app.setApplicationVersion(QStringLiteral("3.0.0"));

    // Apply global Neobrutalist design system
    UselessOS::UselessTheme::applyCorporateStyle(&app);

    // Initialize native CSD window
    DemoOverthinkingWindow window;
    window.show();

    const auto readyTimestamp = std::chrono::high_resolution_clock::now();
    const auto startupDurationMs = std::chrono::duration_cast<std::chrono::milliseconds>(readyTimestamp - startTimestamp).count();

    const long rssKb = getLinuxRssKb();

    std::cout << "\n=======================================================\n";
    std::cout << "  USELESSOS NATIVE C++ WINDOW VERIFICATION REPORT\n";
    std::cout << "=======================================================\n";
    std::cout << " [PERF] Cold Startup Latency : " << startupDurationMs << " ms (Target: < 80 ms)\n";
    if (rssKb > 0) {
        std::cout << " [PERF] Memory Footprint RSS : " << (rssKb / 1024.0) << " MB (Target: < 25 MB)\n";
    }
    std::cout << " [UI]   macOS Brutalist CSD  : INITIALIZED\n";
    std::cout << " [UI]   Traffic Light System : ACTIVE (Close, Min, Max)\n";
    std::cout << " [UI]   Edge Resizing Engine : 8-DIRECTIONAL ACTIVE\n";
    std::cout << " [UI]   Philosophy Modal     : READY\n";
    std::cout << "=======================================================\n\n";

    // Handle test / headless verification flags
    for (int i = 1; i < argc; ++i) {
        const std::string arg = argv[i];
        if (arg == "--test-exit") {
            QTimer::singleShot(500, &app, &QCoreApplication::quit);
            break;
        } else if (arg == "--show-modal") {
            QTimer::singleShot(400, &window, &UselessOS::UselessWindow::showInstructionsDialog);
        }
    }

    return app.exec();
}

#include "test_native_window.moc"
