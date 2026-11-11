// What a reader must always be able to open on the built site.
// Paths are stable ids (knowledge/<path>), so a renamed page fails here on purpose.
import { test, expect, type Page } from "@playwright/test";

const TITLE = "SOC Triage Handbook";

// One stable page per top-level folder of the record.
const PAGES: Array<[string, string]> = [
  ["/docs/orientation/glossary/", "Glossary"],
  ["/docs/windows-events/event-4624/", "4624"],
  ["/docs/mitre/t1110-brute-force/", "Brute Force"],
  ["/docs/playbooks/brute-force/", "brute"],
  ["/docs/enrichment/ip-reputation-policy/", "reputation"],
  ["/docs/rules-map/escalation-policy/", "scalation"],
  ["/docs/triage-note/note-template/", "template"],
  ["/docs/wazuh/architecture/", "rchitecture"],
  ["/docs/networking/osi-model/", "OSI"],
  ["/docs/sysmon/overview/", "Sysmon"],
  ["/docs/linux-auth/ssh-failed-password/", "SSH"],
  ["/docs/false-positives/service-accounts/", "ervice accounts"],
  ["/docs/sla/severity-response-matrix/", "SLA"],
  ["/docs/soc-fundamentals/common-attacks/", "ttacks"],
];

function watchConsole(page: Page): string[] {
  const errors: string[] = [];
  page.on("console", (m) => { if (m.type() === "error") errors.push(m.text()); });
  page.on("pageerror", (e) => errors.push(String(e)));
  return errors;
}

test("home page opens with the record title", async ({ page }) => {
  const errors = watchConsole(page);
  const res = await page.goto("/");
  expect(res?.status()).toBe(200);
  await expect(page).toHaveTitle(new RegExp(TITLE));
  expect(errors).toEqual([]);
});

for (const [path, word] of PAGES) {
  test(`page ${path} opens`, async ({ page }) => {
    const errors = watchConsole(page);
    const res = await page.goto(path);
    expect(res?.status()).toBe(200);
    await expect(page).toHaveTitle(new RegExp(TITLE));
    await expect(page.locator("h1").first()).toContainText(new RegExp(word, "i"));
    expect(errors).toEqual([]);
  });
}

test("flashcards and quiz render on a page that has them", async ({ page }) => {
  await page.goto("/docs/windows-events/event-4740/");
  await expect(page.getByLabel("Card 1 of 6")).toBeVisible();
  await expect(page.getByText("What does event 4740 record?").first()).toBeVisible();
  await expect(page.getByRole("region", { name: "Quiz" })).toBeVisible();
});

test("llms.txt is served and lists the record", async ({ request }) => {
  const res = await request.get("/llms.txt");
  expect(res.status()).toBe(200);
  const body = await res.text();
  expect(body).toContain(`# ${TITLE}`);
  expect(body).toContain("windows-events/event-4740");
});

test("markdown twin of a page is served", async ({ request }) => {
  const res = await request.get("/md/windows-events/event-4740.md");
  expect(res.status()).toBe(200);
  expect(await res.text()).toContain("4740");
});

test("quick triage lookup finds an event by its ID and opens it", async ({ page }) => {
  await page.goto("/");
  const box = page.getByRole("combobox");
  await page.keyboard.press("/");
  await expect(box).toBeFocused();
  await box.fill("4625");
  const first = page.getByRole("option").first();
  await expect(first).toContainText("4625");
  await box.press("Enter");
  await expect(page).toHaveURL(/event-4625/);
});

test("navy dark is the default theme", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("html")).toHaveClass(/dark/);
});

test("sign-in button shows and explains it is not connected yet", async ({ page }) => {
  await page.goto("/");
  const button = page.getByRole("button", { name: "Sign in" });
  await expect(button).toBeVisible();
  await button.click();
  await expect(page.getByText("Sign-in is not connected yet")).toBeVisible();
  await expect(page).toHaveURL(/\/$/); // no redirect to any provider
});
