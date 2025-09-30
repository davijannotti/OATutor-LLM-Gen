const express = require("express");
const axios = require("axios");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.LLM_PORT || 3001;

app.post("/api/llm/feedback", async (req, res) => {
    const { question_stem, student_answer, knowledge_components } = req.body;

    if (!question_stem || !student_answer) {
        return res.status(400).json({ error: "Missing required fields" });
    }

    // Strict prompt in English
    const messages = [
        {
            role: "system",
            content:
                "You are a general tutor. Provide pedagogical feedback strictly in JSON format without revealing the correct answer.",
        },
        {
            role: "user",
            content: `
            Question: ${question_stem}.
            Student answer: ${student_answer}.
            Knowledge components: ${knowledge_components.join(", ")}.

            Return a strict JSON object in this format:
            {
              "evaluation": "correct" | "incorrect",
              "feedback": {
                "message": "An explanation message for the student.",
                "hint": "A hint to help the student reach the correct answer.",
                "study_tips": [
                  {
                    "topic": "The study topic related to the mistake.",
                    "tip": "A practical study tip for the topic."
                  }
                ]
              }
            }

            Rules:
            - If the answer is correct, set "feedback" to null.
            - Do NOT reveal the full solution.
            - When writing math expressions, ALWAYS wrap inline LaTeX in single dollar signs.
              Example: $x = 4$, evaluate $x^2$.
            - Never use double dollar signs ($$...$$).
            - Keep the JSON valid and strictly follow the schema above.
            - Do not add extra keys or text outside the JSON.
            `,
        },
    ];

    try {
        const response = await axios.post(
            `${process.env.LLM_BASE_URL}/chat/completions`,
            {
                model: process.env.LLM_MODEL,
                messages,
                temperature: 0.7,
                max_tokens: 300,
                response_format: { type: "json_object" },
            },
            {
                headers: {
                    Authorization: `Bearer ${process.env.LLM_API_KEY}`,
                    "Content-Type": "application/json",
                },
            },
        );

        const content = response.data.choices[0].message.content;

        let feedback;
        try {
            feedback = JSON.parse(content);
        } catch (err) {
            console.error("Error parsing JSON from LLM:", err);
            return res
                .status(500)
                .json({ error: "Invalid JSON response from LLM" });
        }

        // Strict schema validation
        if (
            !feedback.evaluation ||
            (feedback.evaluation !== "correct" &&
                feedback.evaluation !== "incorrect")
        ) {
            return res
                .status(400)
                .json({ error: "Invalid evaluation field in response" });
        }

        if (feedback.evaluation === "incorrect") {
            if (
                !feedback.feedback ||
                typeof feedback.feedback.message !== "string" ||
                typeof feedback.feedback.hint !== "string" ||
                !Array.isArray(feedback.feedback.study_tips)
            ) {
                return res
                    .status(400)
                    .json({ error: "Invalid feedback structure in response" });
            }

            for (const tip of feedback.feedback.study_tips) {
                if (
                    typeof tip.topic !== "string" ||
                    typeof tip.tip !== "string"
                ) {
                    return res.status(400).json({
                        error: "Invalid study_tips format in response",
                    });
                }
            }
        } else if (
            feedback.evaluation === "correct" &&
            feedback.feedback !== null
        ) {
            return res.status(400).json({
                error: "Feedback must be null when evaluation is correct",
            });
        }

        res.json(feedback);
    } catch (error) {
        console.error(
            "Error calling LLM API:",
            error.response?.data || error.message,
        );
        res.status(500).json({ error: "Internal Server Error" });
    }
});

app.listen(PORT, () => {
    console.log(`LLM middleware server running on port ${PORT}`);
});
