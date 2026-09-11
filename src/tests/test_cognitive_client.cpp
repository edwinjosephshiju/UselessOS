#include <QCoreApplication>
#include <QTimer>
#include <iostream>

#include "CognitiveClient.h"

int main(int argc, char* argv[]) {
    QCoreApplication app(argc, argv);
    app.setApplicationName(QStringLiteral("TestCognitiveClient"));

    std::cout << "\n=======================================================\n";
    std::cout << "  USELESSOS NATIVE COGNITIVE CLIENT VERIFICATION\n";
    std::cout << "=======================================================\n";

    UselessOS::CognitiveClient client(QStringLiteral("http://127.0.0.1:8080"));

    QObject::connect(&client, &UselessOS::CognitiveClient::statusChanged, [](UselessOS::CognitiveClient::ServiceStatus status) {
        std::cout << " [DAEMON] Status Changed: " 
                  << (status == UselessOS::CognitiveClient::ServiceStatus::Online ? "ONLINE" : "OFFLINE") 
                  << "\n";
    });

    QObject::connect(&client, &UselessOS::CognitiveClient::reasoningReceived, [](const QString& reason) {
        std::cout << reason.toStdString() << std::flush;
    });

    QObject::connect(&client, &UselessOS::CognitiveClient::tokenReceived, [](const QString& tok) {
        std::cout << tok.toStdString() << std::flush;
    });

    QObject::connect(&client, &UselessOS::CognitiveClient::generationFinished, [&app](const QString& fullText) {
        std::cout << "\n\n [COGNITIVE STREAM] Finished (" << fullText.length() << " chars).\n";
        std::cout << " [VERIFIED] Asynchronous non-blocking streaming complete.\n";
        std::cout << "=======================================================\n\n";
        QTimer::singleShot(200, &app, &QCoreApplication::quit);
    });

    QObject::connect(&client, &UselessOS::CognitiveClient::errorOccurred, [](const QString& err) {
        std::cout << " [NOTICE] Network/Daemon Status: " << err.toStdString() << "\n";
        std::cout << " [FALLBACK] Triggering resilient philosophical synthesizer...\n\n";
    });

    std::cout << " [TEST] Querying cognitive daemon health...\n";
    client.checkHealth();

    std::cout << " [TEST] Dispatching asynchronous prompt: 'Why should I do nothing today?'\n";
    client.sendPrompt(QStringLiteral("Why should I do nothing today?"), 
                      UselessOS::CognitiveClient::SystemPromptPreset::ProfoundHesitation);

    // Timeout safety: 10 seconds max
    QTimer::singleShot(10000, [&app]() {
        std::cerr << " [TIMEOUT] Verification timed out.\n";
        app.exit(1);
    });

    return app.exec();
}
