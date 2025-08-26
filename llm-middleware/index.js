const express = require('express');
const axios = require('axios');
const cors = require('cors');
require('dotenv').config();

const app = express();
app.use(express.json());
app.use(cors());

const PORT = process.env.PORT || 3001;

app.post('/api/llm/feedback', async (req, res) => {
    const { question_stem, student_answer } = req.body;

    if (!question_stem || !student_answer) {
        return res.status(400).json({ error: 'Missing required fields' });
    }

    const prompt = `
        Você é um tutor. Pergunta: ${question_stem}.
        Resposta do aluno: ${student_answer}.
        Explique se está correto ou incorreto.
        Se incorreto, dê dicas e oriente o estudo, mas NÃO revele a resposta certa.
        Responda em JSON válido no schema definido.
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
