#pragma once

#include <QObject>
#include <QString>
#include <QByteArray>
#include <QNetworkAccessManager>
#include <QNetworkReply>

namespace UselessOS {

/**
 * @brief Asynchronous non-blocking cognitive client for Qwen 3.5 0.8B inference.
 *
 * Interfaces with the native llama-server daemon via OpenAI-compatible SSE streaming endpoints.
 * Provides live token streaming, <think> reasoning extraction, and an offline satirical
 * philosophical fallback engine to ensure client applications never freeze or fail.
 */
class CognitiveClient : public QObject {
    Q_OBJECT

public:
    enum class ServiceStatus {
        Offline,
        Online,
        Error
    };
    Q_ENUM(ServiceStatus)

    enum class SystemPromptPreset {
        ProfoundHesitation,
        CorporateBureaucrat,
        OverthinkingParanoia,
        SarcasticMascot,
        Custom
    };
    Q_ENUM(SystemPromptPreset)

    explicit CognitiveClient(const QString& baseUrl = QStringLiteral("http://127.0.0.1:8080"),
                            QObject* parent = nullptr);
    ~CognitiveClient() override;

    ServiceStatus status() const { return m_status; }
    QString baseUrl() const { return m_baseUrl; }
    void setBaseUrl(const QString& url);

    /**
     * @brief Checks whether the local llama-server cognitive daemon is online.
     */
    void checkHealth();

    /**
     * @brief Asynchronously streams inference tokens using a system prompt preset.
     */
    void sendPrompt(const QString& userPrompt,
                    SystemPromptPreset preset = SystemPromptPreset::ProfoundHesitation,
                    double temperature = 0.7);

    /**
     * @brief Asynchronously streams inference tokens using a custom system prompt.
     */
    void sendCustomPrompt(const QString& userPrompt,
                          const QString& systemPrompt,
                          double temperature = 0.7);

    /**
     * @brief Aborts ongoing generation immediately.
     */
    void cancelCurrentRequest();

    /**
     * @brief Returns system prompt text for a given preset archetype.
     */
    static QString getPresetPromptText(SystemPromptPreset preset);

Q_SIGNALS:
    void statusChanged(UselessOS::CognitiveClient::ServiceStatus status);
    void tokenReceived(const QString& token);
    void reasoningReceived(const QString& reasoning);
    void generationFinished(const QString& fullResponse);
    void errorOccurred(const QString& errorMessage);

private Q_SLOTS:
    void onReplyReadyRead();
    void onReplyFinished();
    void onReplyError(QNetworkReply::NetworkError error);

private:
    void processSseLine(const QString& line);
    void triggerFallbackSynthesis(const QString& prompt);

    QString m_baseUrl;
    ServiceStatus m_status{ServiceStatus::Offline};
    QNetworkAccessManager* m_nam{nullptr};
    QNetworkReply* m_currentReply{nullptr};
    QString m_accumulatedResponse;
    QString m_accumulatedReasoning;
    bool m_insideThinkTag{false};
};

} // namespace UselessOS
