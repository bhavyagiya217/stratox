import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "apex-dark": "#0a0f1e",
        "apex-panel": "#111827",
        "apex-border": "#1f2937",
        "apex-accent": "#6366f1",
        "apex-accent2": "#8b5cf6",
      },
      backgroundImage: {
        "apex-gradient": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
      },
    },
  },
  plugins: [],
};
export default config;
