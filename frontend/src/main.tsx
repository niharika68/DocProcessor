import React from "react";
import ReactDOM from "react-dom/client";
import { Provider } from "jotai";
import App from "./App";
import PasswordGate from "./components/PasswordGate";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <PasswordGate>
      <Provider>
        <App />
      </Provider>
    </PasswordGate>
  </React.StrictMode>
);
