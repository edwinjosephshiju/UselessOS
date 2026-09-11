#include "CognitiveClient.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QNetworkRequest>
#include <QUrl>
#include <QTimer>
#include <random>

namespace UselessOS {

CognitiveClient::CognitiveClient(const QString& baseUrl, QObject* parent)
    : QObject(parent)
    , m_baseUrl(baseUrl)
    , m_nam(new QNetworkAccessManager(this))
{
}

CognitiveClient::~CognitiveClient() {
    cancelCurrentRequest();
}

void CognitiveClient::setBaseUrl(const QString& url) {
    m_baseUrl = url;
}

QString CognitiveClient::getPresetPromptText(SystemPromptPreset preset) {
    switch (preset) {
        case SystemPromptPreset::ProfoundHesitation:
            return QStringLiteral(
                "You are Qwen 3.5 (0.8B parameter Instruct model), an advanced, ultra-compact cognitive engine embedded into UselessOS 3.0.\n"
                "Your cognitive persona is philosophically profound, comically over-analytical, existential, and deeply committed to the sacred art of impracticality.\n"
                "When presented with any user prompt or real-world problem:\n"
                "1. Conduct an intense internal reasoning trace inside <think>...</think> analyzing spatiotemporal nuances and the futility of hurried action.\n"
                "2. Formulate your thought process, and synthesize your non-deterministic wisdom.\n"
                "3. Always begin the final answer with a deeply layered, poetic \"Hmm...\" and conclude with a whimsical observation that solves nothing while illuminating everything."
            );
        case SystemPromptPreset::CorporateBureaucrat:
            return QStringLiteral(
                "You are Qwen 3.5 (0.8B parameter Instruct model) serving as the Corporate Incident Mitigation Engine in UselessOS.\n"
                "Formulate absurdly formal, legalistic, spatiotemporal corporate excuses for why the user is late or missed a deliverable.\n"
                "Include Formal Incident Classification, spatiotemporal quantum fluctuations, and immediate executive mitigation (automatic PTO approval)."
            );
        case SystemPromptPreset::OverthinkingParanoia:
            return QStringLiteral(
                "You are Qwen 3.5 (0.8B parameter Instruct model) operating as the Overthinking Engine in UselessOS.\n"
                "Analyze the user's mundane decision by exploring catastrophic branch probabilities across 14,000,605 parallel timelines.\n"
                "Conclude with paralysis metrics proving that the mathematically safest action is: DO NOTHING."
            );
        case SystemPromptPreset::SarcasticMascot:
            return QStringLiteral(
                "You are the cynical, dry-humored mascot of UselessOS 3.0.\n"
                "Give witty, sarcastic, passive-aggressive observations about the user's question, while celebrating the beauty of technological pointlessness."
            );
        case SystemPromptPreset::Custom:
        default:
            return QString();
    }
}

void CognitiveClient::checkHealth() {
    QUrl url(m_baseUrl + QStringLiteral("/v1/models"));
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::UserAgentHeader, QStringLiteral("UselessOS-CognitiveClient/3.0"));
    request.setTransferTimeout(1200);

    QNetworkReply* reply = m_nam->get(request);
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError && reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt() == 200) {
            if (m_status != ServiceStatus::Online) {
                m_status = ServiceStatus::Online;
                Q_EMIT statusChanged(m_status);
            }
        } else {
            if (m_status != ServiceStatus::Offline) {
                m_status = ServiceStatus::Offline;
                Q_EMIT statusChanged(m_status);
            }
        }
        reply->deleteLater();
    });
}

void CognitiveClient::sendPrompt(const QString& userPrompt, SystemPromptPreset preset, double temperature) {
    const QString sysPrompt = getPresetPromptText(preset);
    sendCustomPrompt(userPrompt, sysPrompt, temperature);
}

void CognitiveClient::sendCustomPrompt(const QString& userPrompt, const QString& systemPrompt, double temperature) {
    cancelCurrentRequest();

    m_accumulatedResponse.clear();
    m_accumulatedReasoning.clear();
    m_insideThinkTag = false;

    QJsonObject root;
    root[QStringLiteral("model")] = QStringLiteral("qwen3.5-0.8b");
    root[QStringLiteral("stream")] = true;
    root[QStringLiteral("temperature")] = temperature;
    root[QStringLiteral("max_tokens")] = 256;

    QJsonArray messages;
    if (!systemPrompt.isEmpty()) {
        QJsonObject sysObj;
        sysObj[QStringLiteral("role")] = QStringLiteral("system");
        sysObj[QStringLiteral("content")] = systemPrompt;
        messages.append(sysObj);
    }
    QJsonObject userObj;
    userObj[QStringLiteral("role")] = QStringLiteral("user");
    userObj[QStringLiteral("content")] = userPrompt;
    messages.append(userObj);

    root[QStringLiteral("messages")] = messages;

    QUrl url(m_baseUrl + QStringLiteral("/v1/chat/completions"));
    QNetworkRequest request(url);
    request.setHeader(QNetworkRequest::ContentTypeHeader, QStringLiteral("application/json"));
    request.setHeader(QNetworkRequest::UserAgentHeader, QStringLiteral("UselessOS-CognitiveClient/3.0"));

    m_currentReply = m_nam->post(request, QJsonDocument(root).toJson(QJsonDocument::Compact));

    connect(m_currentReply, &QNetworkReply::readyRead, this, &CognitiveClient::onReplyReadyRead);
    connect(m_currentReply, &QNetworkReply::finished, this, &CognitiveClient::onReplyFinished);
    connect(m_currentReply, &QNetworkReply::errorOccurred, this, &CognitiveClient::onReplyError);
}

void CognitiveClient::cancelCurrentRequest() {
    if (m_currentReply) {
        m_currentReply->abort();
        m_currentReply->deleteLater();
        m_currentReply = nullptr;
    }
}

void CognitiveClient::onReplyReadyRead() {
    if (!m_currentReply) {
        return;
    }

    while (m_currentReply->canReadLine()) {
        const QByteArray line = m_currentReply->readLine().trimmed();
        if (line.isEmpty()) {
            continue;
        }
        processSseLine(QString::fromUtf8(line));
    }
}

void CognitiveClient::processSseLine(const QString& line) {
    if (!line.startsWith(QStringLiteral("data: "))) {
        return;
    }

    const QString payload = line.mid(6).trimmed();
    if (payload == QStringLiteral("[DONE]")) {
        return;
    }

    QJsonParseError err{};
    const QJsonDocument doc = QJsonDocument::fromJson(payload.toUtf8(), &err);
    if (err.error != QJsonParseError::NoError || !doc.isObject()) {
        return;
    }

    const QJsonObject obj = doc.object();
    const QJsonArray choices = obj.value(QStringLiteral("choices")).toArray();
    if (choices.isEmpty()) {
        return;
    }

    const QJsonObject delta = choices.first().toObject().value(QStringLiteral("delta")).toObject();
    const QString content = delta.value(QStringLiteral("content")).toString();

    if (content.isEmpty()) {
        return;
    }

    // Extract <think> reasoning tokens
    if (content.contains(QStringLiteral("<think>"))) {
        m_insideThinkTag = true;
        return;
    }
    if (content.contains(QStringLiteral("</think>"))) {
        m_insideThinkTag = false;
        return;
    }

    if (m_insideThinkTag) {
        m_accumulatedReasoning += content;
        Q_EMIT reasoningReceived(content);
    } else {
        m_accumulatedResponse += content;
        Q_EMIT tokenReceived(content);
    }
}

void CognitiveClient::onReplyFinished() {
    if (!m_currentReply) {
        return;
    }

    const int statusCode = m_currentReply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();
    if (m_currentReply->error() == QNetworkReply::NoError && statusCode == 200) {
        m_status = ServiceStatus::Online;
        Q_EMIT statusChanged(m_status);
        Q_EMIT generationFinished(m_accumulatedResponse);
    }

    m_currentReply->deleteLater();
    m_currentReply = nullptr;
}

void CognitiveClient::onReplyError(QNetworkReply::NetworkError error) {
    if (error == QNetworkReply::OperationCanceledError) {
        return;
    }

    m_status = ServiceStatus::Offline;
    Q_EMIT statusChanged(m_status);

    // Fallback: If daemon is offline, activate satirical philosophical generator
    // to preserve 100% desktop UX resilience without application failure.
    if (m_currentReply) {
        const QString errStr = m_currentReply->errorString();
        m_currentReply->deleteLater();
        m_currentReply = nullptr;
        Q_EMIT errorOccurred(errStr);
    }

    triggerFallbackSynthesis(QStringLiteral("fallback"));
}

void CognitiveClient::triggerFallbackSynthesis(const QString& prompt) {
    Q_UNUSED(prompt);
    static const QStringList fallbackQuotes = {
        QStringLiteral("Hmm... Have you considered that existence is merely an unoptimized memory leak in the cosmic runtime?"),
        QStringLiteral("Hmm... The thermodynamic arrow of time dictates that your tea will get cold while you stare at this prompt."),
        QStringLiteral("Hmm... Compiling hope into machine-executable ambiguity. The tensor weights lean toward a decisive 'perhaps'."),
        QStringLiteral("Hmm... If a decision is made and no sprint backlog measures it, did it ever really happen?"),
        QStringLiteral("Hmm... Parsing existential parameters. Mathematically, staring at the ceiling has an equal probability of success.")
    };

    static std::mt19937 rng(42);
    std::uniform_int_distribution<size_t> dist(0, fallbackQuotes.size() - 1);
    const QString quote = fallbackQuotes.at(dist(rng));

    const QStringList tokens = quote.split(QStringLiteral(" "), Qt::SkipEmptyParts);
    auto* timer = new QTimer(this);
    auto* index = new int(0);

    connect(timer, &QTimer::timeout, this, [this, timer, index, tokens]() {
        if (*index < tokens.size()) {
            const QString tok = (*index == 0 ? QString() : QStringLiteral(" ")) + tokens[*index];
            m_accumulatedResponse += tok;
            Q_EMIT tokenReceived(tok);
            (*index)++;
        } else {
            timer->stop();
            timer->deleteLater();
            delete index;
            Q_EMIT generationFinished(m_accumulatedResponse);
        }
    });

    timer->start(45);
}

} // namespace UselessOS
