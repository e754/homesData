// // @ts-check

// // npx playwright test


// const { test, expect } = require('@playwright/test');
// const { chromium } = require('playwright');



// (async () => {
//   // Launch the browser
//   const browser = await chromium.launch({ headless: false });
//   const context = await browser.newContext();
//   const page = await context.newPage();

//   // Navigate to the website
//   await page.goto('https://example.com');

//   // Find the link and click it
//   await page.click('text=More information'); // Selector for the link's text

//   // Wait for the navigation to complete
//   await page.waitForLoadState('load');

//   // Print the current URL after clicking
//   console.log('Current URL:', page.url());

//   // Close the browser
//   await browser.close();
// })();
// test('has title', async ({ page }) => {
//   await page.goto('https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB');
//   console.log("hi")
//   // Expect a title "to contain" a substring.
//   await expect(page).toHaveTitle(/Playwright/);
// });

// // test('get started link', async ({ page }) => {
// //   await page.goto('https://playwright.dev/');

// //   // Click the get started link.
// //   await page.getByRole('link', { name: 'Get started' }).click();

// //   // Expects page to have a heading with the name of Installation.
// //   await expect(page.getByRole('heading', { name: 'Installation' })).toBeVisible();
// // });
