# LLM Feedback Documentation

This document outlines the implementation of the LLM-powered feedback feature in OATutor.

## 1. Overview

The LLM feedback feature provides students with immediate, AI-generated feedback on their short text answers. This feature is designed to be a supportive tool that guides students toward the correct answer without giving it away directly.

## 2. Feature Activation

The feature is activated through a combination of a problem-level meta-tag and a global environment variable.

-   **Meta-tag**: A problem must have the `allowLLMFeedback` meta-tag set to `true` in the course content.
-   **Environment Variable**: The `REACT_APP_LLM_FEEDBACK_ENABLED` environment variable must be set to `true` in the frontend application.

This dual-control mechanism allows for granular control over which problems use the feature and enables it to be toggled on or off globally.

## 3. Frontend Implementation

The frontend is responsible for:

1.  Checking if the feature is enabled for the current problem.
2.  Making a request to the backend proxy with the problem details and the student's answer.
3.  Displaying the feedback to the student in a dedicated component.
4.  Caching responses to prevent redundant API calls.

### Key Components

-   **`src/components/LLMFeedbackPane.jsx`**: A new component created to display the feedback from the LLM. It handles different states: loading, success, and error.
-   **`src/components/problem-layout/Problem.js`**: This component was modified to include the logic for fetching and managing the LLM feedback. It now holds the feedback state and triggers the API call.
-   **`src/components/problem-layout/ProblemCard.js`**: This component was modified to pass the student's answer up to the `Problem` component.

### Data Flow

1.  A student submits an answer in the `ProblemInput` component.
2.  The answer is passed up through `ProblemCard` to the `answerMade` function in `Problem.js`.
3.  In `Problem.js`, if the feature is enabled, the `fetchLLMFeedback` function is called.
4.  This function sends a POST request to the `/api/llm/feedback` endpoint.
5.  The response is stored in the component's state, and the `LLMFeedbackPane` is re-rendered to display the feedback.

## 4. Backend Implementation

The backend is an Express.js proxy located in the `llm-middleware/` directory. It is responsible for securely calling the LLM API.

### Key Components

-   **`llm-middleware/index.js`**: The main file for the proxy server.
-   **`llm-middleware/package.json`**: Defines the dependencies for the proxy server, including `express` and `axios`.

### API Endpoint

-   **`POST /api/llm/feedback`**: This endpoint receives the `question_stem` and `student_answer` from the frontend.

### Logic

1.  The endpoint receives the request from the frontend.
2.  It constructs a prompt for the LLM using the received data.
3.  It makes a POST request to the LLM API, including the API key from the environment variables (`LLM_API_KEY`).
4.  It returns the LLM's response to the frontend.

### Environment Variables

The backend proxy requires the following environment variables to be set:

-   `LLM_API_KEY`: Your API key for the LLM service.
-   `LLM_BASE_URL`: The base URL for the LLM API.
-   `LLM_MODEL`: The specific model to be used.
-   `PORT`: The port on which the proxy server will run (defaults to 3001).
