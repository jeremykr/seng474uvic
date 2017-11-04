"use strict"

import * as puppeteer from 'puppeteer';
import * as fs from 'fs';

const remaxVicUrl = 'https://www.remax.ca/find-real-estate/#type=all&city=VICTORIA,+BC&neighbourhoodId=&postalCode=&queryText=VICTORIA,+BC&east=-123.02994161401368&west=-123.66474538598634&north=48.504678828646526&south=48.31780883885029&showSchools=false&schoolTypes=0,1,2&schoolLevels=0,1,2&schoolPrograms=0,1&schoolIds=&refreshPins=true&gallery.listingPageSize=20&coordinatesFor=VICTORIA,+BC&cityName=Victoria&province=BC&mode=CustomBox&alt=&isCommercial=false&zoom=12&listingtab.index=2';

(async () => {
  const time = Date.now();
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(remaxVicUrl, { waitUntil: 'networkidle' });
  const galleryTab = await page.$('.galleryTab');
  await galleryTab.tap();

  await page.waitForNavigation({ waitUntil: 'networkidle' });
  let urls = await scrapeUrls(page);

  let nextArrow : puppeteer.ElementHandle;
  while ((nextArrow = await page.$('.nextArrow')) !== null) {
    await nextArrow.tap();
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    urls = urls.concat(await scrapeUrls(page));
  }
  fs.writeFileSync('urlData.json', JSON.stringify(urls), 'utf8');
  await browser.close();
  console.log(`All URLs saved! Time taken: ${Date.now() - time}ms`);
})();

async function scrapeUrls(page: puppeteer.Page) {
  const elements = await page.$$('.teaserImage > a');
  return await Promise.all(elements.map(async x => (await x.getProperty('href')).jsonValue()));
}