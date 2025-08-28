import React from 'react';

const LLMFeedbackPane = ({ status, feedback }) => {
  if (status === 'loading') {
    return <div>Loading feedback...</div>;
  }

  if (status === 'error') {
    return <div style={{ color: 'red' }}>Error loading feedback.</div>;
  }

  if (status !== 'success' || !feedback) {
    return null;
  }

  const judgmentColor = feedback.evaluation === 'correto' ? 'green' : 'red';

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }}>
      <p>
        <span style={{ color: judgmentColor, fontWeight: 'bold' }}>
          {feedback.evaluation}
        </span>
      </p>
      {feedback.feedback && (
        <div>
          {feedback.feedback.message && <p><strong>Message:</strong> {feedback.feedback.message}</p>}
          {feedback.feedback.hint && <p><strong>Hint:</strong> {feedback.feedback.hint}</p>}
          {feedback.feedback.study_tips && feedback.feedback.study_tips.length > 0 && (
            <div>
              <strong>Study Tips:</strong>
              <ul>
                {feedback.feedback.study_tips.map((tip, index) => (
                  <li key={index}><strong>{tip.topic}:</strong> {tip.tip}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default LLMFeedbackPane;
