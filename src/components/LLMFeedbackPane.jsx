import React from "react";
import { renderGPTText } from "../platform-logic/renderText.js";

const LLMFeedbackPane = ({
    status,
    feedback,
    problemID,
    variabilization,
    context,
}) => {
    if (status === "loading") {
        return (
            <div style={styles.container}>
                <p style={styles.loading}>⏳ Loading feedback...</p>
            </div>
        );
    }

    if (status === "error") {
        return (
            <div style={{ ...styles.container, borderColor: "#e74c3c" }}>
                <p style={styles.error}>
                    ❌ Error loading feedback. Please try again.
                </p>
            </div>
        );
    }

    if (status !== "success" || !feedback) {
        return (
            <div style={styles.container}>
                <p style={styles.empty}>No feedback available.</p>
            </div>
        );
    }

    const judgmentColor =
        feedback.evaluation === "correct" ? "#2ecc71" : "#e74c3c";

    return (
        <div
            style={{
                ...styles.container,
                borderColor: judgmentColor,
            }}
        >
            <p style={{ ...styles.evaluation, color: judgmentColor }}>
                {feedback.evaluation === "correct"
                    ? "✅ Correct"
                    : "❌ Incorrect"}
            </p>

            {/* Feedback only if incorrect */}
            {feedback.feedback && (
                <div style={styles.feedbackSection}>
                    {feedback.feedback.message && (
                        <p style={styles.text}>
                            <strong>💡 Explanation:</strong>{" "}
                            {renderGPTText(
                                feedback.feedback.message,
                                problemID,
                                variabilization,
                                context,
                            )}
                        </p>
                    )}
                    {feedback.feedback.hint && (
                        <p style={styles.text}>
                            <strong>📝 Hint:</strong>{" "}
                            {renderGPTText(
                                feedback.feedback.hint,
                                problemID,
                                variabilization,
                                context,
                            )}
                        </p>
                    )}
                    {Array.isArray(feedback.feedback.study_tips) &&
                        feedback.feedback.study_tips.length > 0 && (
                            <div style={styles.tipsSection}>
                                <strong>📚 Study Tips:</strong>
                                <ul style={styles.tipsList}>
                                    {feedback.feedback.study_tips.map(
                                        (tip, index) => (
                                            <li
                                                key={index}
                                                style={styles.tipItem}
                                            >
                                                <strong>
                                                    {renderGPTText(
                                                        tip.topic,
                                                        problemID,
                                                        variabilization,
                                                        context,
                                                    )}
                                                    :
                                                </strong>{" "}
                                                {renderGPTText(
                                                    tip.tip,
                                                    problemID,
                                                    variabilization,
                                                    context,
                                                )}
                                            </li>
                                        ),
                                    )}
                                </ul>
                            </div>
                        )}
                </div>
            )}
        </div>
    );
};

const styles = {
    container: {
        border: "2px solid #ccc",
        borderRadius: "8px",
        padding: "30px",
        marginTop: "55px",
        backgroundColor: "#f9f9f9",
        fontFamily: "Arial, sans-serif",
    },
    evaluation: {
        fontSize: "18px",
        fontWeight: "bold",
        marginBottom: "10px",
    },
    feedbackSection: {
        marginTop: "15px",
    },
    text: {
        margin: "8px 0",
        lineHeight: "1.4",
    },
    tipsSection: {
        marginTop: "12px",
    },
    tipsList: {
        marginTop: "6px",
        paddingLeft: "20px",
    },
    tipItem: {
        marginBottom: "6px",
    },
    loading: {
        color: "#2980b9",
        fontStyle: "italic",
    },
    error: {
        color: "#e74c3c",
        fontWeight: "bold",
    },
    empty: {
        color: "#7f8c8d",
        fontStyle: "italic",
    },
};

export default LLMFeedbackPane;
