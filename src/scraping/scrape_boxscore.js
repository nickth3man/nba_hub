const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  try {
    console.error('Navigating to page...');
    await page.goto('https://www.basketball-reference.com/boxscores/194611010TRH.html', { 
      waitUntil: 'domcontentloaded',
      timeout: 60000 
    });
    
    console.error('Waiting for stats tables...');
    try {
      await page.waitForSelector('table.stats_table', { timeout: 15000 });
    } catch (e) {
      const title = await page.title();
      if (title.includes('Just a moment')) {
        console.error('Blocked by Cloudflare. Title:', title);
        // Try to wait a bit longer or solve captcha if possible (not really possible here)
      } else {
        console.error('Table not found. Title:', title);
      }
      process.exit(1);
    }

    const data = await page.evaluate(() => {
      const extractBoxScore = (tableId) => {
        const table = document.getElementById(tableId);
        if (!table) return [];
        const rows = Array.from(table.querySelectorAll('tbody tr:not(.thead)'));
        return rows.map(row => {
          const player = row.querySelector('[data-stat="player"]')?.innerText || '';
          const mp = row.querySelector('[data-stat="mp"]')?.innerText || '';
          const fg = row.querySelector('[data-stat="fg"]')?.innerText || '';
          const fga = row.querySelector('[data-stat="fga"]')?.innerText || '';
          const ft = row.querySelector('[data-stat="ft"]')?.innerText || '';
          const fta = row.querySelector('[data-stat="fta"]')?.innerText || '';
          const reb = row.querySelector('[data-stat="trb"]')?.innerText || '';
          const ast = row.querySelector('[data-stat="ast"]')?.innerText || '';
          const pf = row.querySelector('[data-stat="pf"]')?.innerText || '';
          const pts = row.querySelector('[data-stat="pts"]')?.innerText || '';
          
          return {
            player,
            mp,
            fg,
            fga,
            ft,
            fta,
            reb,
            ast,
            pf,
            pts
          };
        }).filter(p => p.player && p.player !== 'Team Totals');
      };

      return {
        NYK: extractBoxScore('box-NYK-game-basic'),
        TRH: extractBoxScore('box-TRH-game-basic')
      };
    });

    console.log(JSON.stringify(data, null, 2));
  } catch (error) {
    console.error('Error:', error);
  } finally {
    await browser.close();
  }
})();
