# flatZ Frontend

flatZ is a community event and activity recommendation platform. This frontend is built with React, Vite, and Tailwind CSS, providing a fast, modern user interface for personalized recommendations and explanations.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [API Integration](#api-integration)
- [How to Extend](#how-to-extend)
- [Development & Testing](#development--testing)
- [License](#license)
- [Contact](#contact)

---

## Project Overview

The frontend consumes REST APIs from the flatZ backend to:
- Display personalized home feed recommendations
- Show explanations for recommendations
- Collect user feedback

---

## Architecture

```
frontend/
├── public/                # Static assets
│   └── vite.svg
├── src/                   # Source code
│   ├── api/               # API utilities
│   │   └── api.js
│   ├── assets/            # Images and icons
│   │   └── react.svg
│   ├── components/        # React components
│   │   ├── Explanations.jsx
│   │   └── HomeFeed.jsx
│   ├── App.jsx            # Main app component
│   ├── index.css          # Global styles (Tailwind)
│   └── main.jsx           # Entry point
├── index.html             # HTML template
├── package.json           # Project metadata and dependencies
├── postcss.config.js      # PostCSS configuration
├── tailwind.config.js     # Tailwind CSS configuration
├── vite.config.js         # Vite configuration
├── eslint.config.js       # ESLint configuration
├── .gitignore             # Git ignore file
└── README.md              # This file
```

---

## Tech Stack

- **React**: UI library for building interactive interfaces
- **Vite**: Fast development server and build tool
- **Tailwind CSS**: Utility-first CSS framework
- **ESLint**: Linting and code quality
- **PostCSS**: CSS processing
- **Axios/Fetch**: For API requests (see `src/api/api.js`)

---

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone [<repo-url>](https://github.com/gargdivyansh1/assignment)
   cd flatZ/frontend
   ```

2. **Install dependencies:**
   ```sh
   npm install
   ```

3. **Start the development server:**
   ```sh
   npm run dev
   ```
   - The app will be available at [http://localhost:5173](http://localhost:5173) by default.

4. **Build for production:**
   ```sh
   npm run build
   ```

---

## Project Structure

- **`src/App.jsx`**: Main application component, sets up routing and layout.
- **`src/main.jsx`**: Entry point, renders the app.
- **`src/api/api.js`**: Contains functions to interact with backend APIs (`/v1/reco/homefeed`, `/v1/reco/explanations`, `/v1/reco/feedback`).
- **`src/components/HomeFeed.jsx`**: Displays personalized recommendations.
- **`src/components/Explanations.jsx`**: Shows explanations for recommendations.
- **`src/assets/`**: Static images and icons.
- **`index.css`**: Global styles using Tailwind CSS.

---

## API Integration

The frontend communicates with the backend via REST APIs:

| Endpoint                  | Purpose                                    |
|---------------------------|--------------------------------------------|
| `/v1/reco/homefeed`       | Fetch personalized recommendations         |
| `/v1/reco/explanations`   | Fetch explanations for recommendations     |
| `/v1/reco/feedback`       | Submit user feedback                       |

- API calls are managed in `src/api/api.js`.
- Update the base URL in `api.js` if your backend runs on a different host/port.

---

## How to Extend

- **Add new UI features:** Create new components in `src/components/`.
- **Add new API calls:** Extend `src/api/api.js` and use in components.
- **Customize styles:** Edit `index.css` or Tailwind config.
- **Integrate with backend:** Ensure endpoints match backend API.

---

## Development & Testing

- Use VS Code for development.
- Lint code with:
  ```sh
  npm run lint
  ```
- Preview and debug UI in the browser.
- Write tests (if needed) using your preferred React testing library.

---

## Contact

For questions or contributions, open an issue or pull request on GitHub.
