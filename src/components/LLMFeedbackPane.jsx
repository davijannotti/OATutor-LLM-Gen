import React from 'react';

const LLMFeedbackPane = ({ status, feedback, hints }) => {
  if (status === 'loading') {
    return <div>Loading feedback...</div>;
  }

  if (status === 'error') {
    return <div style={{ color: 'red' }}>Error loading feedback.</div>;
  }

  if (status !== 'success') {
    return null;
  }

  const judgmentColor = feedback.judgment === 'correct' ? 'green' : 'red';

  return (
    <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '10px' }}>
      <p>
        <span style={{ color: judgmentColor, fontWeight: 'bold' }}>
          {feedback.judgment}
        </span>
        : {feedback.feedback}
      </p>
      {hints && hints.length > 0 && (
        <div>
          <strong>Hints:</strong>
          <ul>
            {hints.map((hint, index) => (
              <li key={index}>{hint}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default LLMFeedbackPane;
