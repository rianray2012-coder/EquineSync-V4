import { reactRootErrorHandler } from "@/monitoring";
import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";

const rootOptions = reactRootErrorHandler
  ? {
      onUncaughtError: reactRootErrorHandler,
      onCaughtError: reactRootErrorHandler,
      onRecoverableError: reactRootErrorHandler,
    }
  : undefined;

const root = ReactDOM.createRoot(document.getElementById("root"), rootOptions);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
