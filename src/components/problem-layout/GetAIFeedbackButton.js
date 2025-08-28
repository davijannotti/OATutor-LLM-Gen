import React from 'react';
import Button from '@material-ui/core/Button';

const GetAIFeedbackButton = ({ onClick }) => {
  return (
    <Button
      variant="contained"
      color="primary"
      onClick={onClick}
      style={{ marginTop: '10px' }}
    >
      Get AI Feedback
    </Button>
  );
};

export default GetAIFeedbackButton;
