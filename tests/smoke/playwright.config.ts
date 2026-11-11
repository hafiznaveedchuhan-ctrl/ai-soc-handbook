// Browser smoke test for the BUILT static site (system/site/out).
// Run `npm run build` first; this config serves the export with `npm run preview`
// on port 4173 so it never collides with a running `npm run dev` on 3000.
import { defineConfig, devices } from "@playwright/test";

const PORT = 4173;

export default defineConfig({
  testDir: ".",
  timeout: 30_000,
  retries: process.env.CI ? 1 : 0,
  reporter: process.env.CI ? [["list"], ["html", { open: "never", outputFolder: "../../playwright-report" }]] : "list",
  use: { baseURL: `http://127.0.0.1:${PORT}` },
  projects: [{ name: "chromium", use: { ...devices["Desktop Chrome"] } }],
  webServer: {
    command: "node system/site/preview.mjs",
    cwd: "../..",
    env: { PORT: String(PORT) },
    url: `http://127.0.0.1:${PORT}/`,
    reuseExistingServer: false,
    timeout: 30_000,
  },
});
