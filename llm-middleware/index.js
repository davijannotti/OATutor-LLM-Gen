const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.PORT || 3001;

app.post('/api/llm/feedback', async (req, res) => {
    console.log('Request body:', req.body);
    const { question_stem, student_answer, knowledge_components } = req.body;

    if (!question_stem || !student_answer) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const prompt = `
        Você é um tutor de matemática.
        A pergunta é: ${question_stem}.
        A resposta do aluno é: ${student_answer}.
        Os componentes de conhecimento para esta pergunta são: ${knowledge_components.join(', ')}.

        Avalie a resposta do aluno e forneça um feedback em formato JSON.
        O JSON deve ter a seguinte estrutura:
        {
          "evaluation": "correto" | "incorreto",
          "feedback": {
            "message": "Uma mensagem para o aluno explicando o erro.",
            "hint": "Uma dica para ajudar o aluno a chegar na resposta correta.",
            "study_tips": [
              {
                "topic": "O tópico de estudo relacionado ao erro.",
                "tip": "Uma dica de estudo para o tópico."
              }
            ]
          }
        }

        Se a resposta estiver correta, o campo "feedback" pode ser nulo.
        Não revele a resposta correta.
    `;

    try {
        const response = await axios.post(process.env.LLM_BASE_URL, {
            model: process.env.LLM_MODEL,
            prompt: prompt,
            stream: false,
            temperature: 0.7,
            max_tokens: 150,
            top_p: 1,
            frequency_penalty: 0,
            presence_penalty: 0,
            stop: ["\n\n"],
            response_format: { type: "json_object" },
        }, {
            headers: {
                'Authorization': `Bearer ${process.env.LLM_API_KEY}`,
                'Content-Type': 'application/json'
            }
        });

        res.json(response.data);
    } catch (error) {
        console.error('Error calling LLM API:', error);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

app.listen(PORT, () => {
    console.log(`LLM middleware server running on port ${PORT}`);
});
