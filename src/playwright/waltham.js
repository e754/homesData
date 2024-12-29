const { firefox } = require('playwright');

const fs = require('fs');
const csv = require('csv-parser');
const path = require('path');

// Load CSV data
let data = [];
fs.createReadStream('walthamUsage.csv')
  .pipe(csv())
  .on('data', (row) => data.push(row))
  .on('end', async () => {
    const browser = await firefox.launch({
        proxy: {
            server: 'http://myproxy.com:3128',
            username: 'usr',
            password: 'pwd'
        },
        headless: false,
        args: [
            '--ignore-certificate-errors',
            '--disable-blink-features=AutomationControlled',
            '--enable-webgl',
            '--use-gl=swiftshader',
            '--enable-accelerated-2d-canvas'
        ],
        proxy: {
            server: 'brd.superproxy.io:33335',
            username: 'brd-customer-hl_ae195d4f-zone-residential_proxy1',
            password: '2a4szrjr662z'
        }

    });
    const context = await browser.newContext({
        ignoreHTTPSErrors: true,
        userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        viewport: { width: 1280, height: 720 },
        locale: 'en-US',
        timezoneId: 'America/New_York',
        deviceScaleFactor: 1,
        
    });
    const page = await browser.newPage();
    
    const baseWaitTime = 2;
    
    // Helper function to add random delay
    function humanDelay(minWait = 0.5, maxWait = 2.0) {
      return new Promise(resolve => setTimeout(resolve, Math.random() * (maxWait - minWait) + minWait));
    }

    for (let i = 10000; i < 15000; i++) {
      console.log("Row:", i);
      try {
        console.log(i, data[i]['Location']);
        
        // Go to the page
        await page.goto("https://web-server.city.waltham.ma.us/GovernEComponents/WebUserInterfaceUB");
        await humanDelay();

        // Click the first button to select Parcel ID
        await page.click('#objWP_reportparameterstyle_ESearchManager1_rdblStyles_1');
        await humanDelay();
        await page.click('#objWP_reportparameterstyle_ESearchManager1_cmdLoadStyleContent');
        await humanDelay();

        const id_value = data[i]['Parcel ID'];
        const ids = id_value.split(' ');

        // Enter Parcel ID parts in the input fields
        await page.fill('#objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_0', ids[0]);
        await page.fill('#objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_1', ids[1]);
        await page.fill('#objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_msk_GFD0_2', ids[2]);
        await humanDelay();

        // Click the "Go" button
        await page.click('#objWP_reportparameterstyle_ESearchManager1_Web_CO_SearchPanel1_btnGo');
        await humanDelay();
        await page.click('#objWP_reportparameterstyle_ESearchManager1_cmdFinish');
        await humanDelay();

        // Switch to iframe
        const frame = page.frame({ index: 0 });

        // Extract permit dates
        const pmdates1_elements = await frame.$$('#PMDATE1');
        let ret = '';
        for (let el of pmdates1_elements) {
          ret += await el.textContent();
        }
        data[i]['permit dates'] = ret;
        await humanDelay();

        // Click the Text5 button
        await page.click('#Text5');
        await humanDelay();

        // Extract usage information
        const usageElement = await frame.$('#CONSUMPTION1 table tbody tr td table tbody tr td span');
        const usageText = await usageElement.textContent();
        data[i]['usage'] = usageText;
        console.log(usageText);

        // Save data to CSV every 10 iterations
        if (i % 10 === 0) {
          console.log("Downloaded");
          fs.writeFileSync('walthamUsage.csv', data.map(row => Object.values(row).join(',')).join('\n'));
        }
      } catch (e) {
        console.error(e);
        console.trace();
        await humanDelay();
      }
    }

    // Close browser
    await browser.close();
  });
