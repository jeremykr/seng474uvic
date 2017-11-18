"use strict"

import * as fs from 'fs';
import * as puppeteer from 'puppeteer';
import * as request from 'request-promise';
import * as cheerio from 'cheerio';
import { mapLimit } from 'async';
import { cursorTo } from 'readline';
import { EventEmitter } from 'events';

const remaxVicUrl = 'https://www.remax.ca/find-real-estate/#type=all&city=VICTORIA,+BC&neighbourhoodId=&postalCode=&queryText=VICTORIA,+BC&east=-123.02994161401368&west=-123.66474538598634&north=48.504678828646526&south=48.31780883885029&showSchools=false&schoolTypes=0,1,2&schoolLevels=0,1,2&schoolPrograms=0,1&schoolIds=&refreshPins=true&gallery.listingPageSize=20&coordinatesFor=VICTORIA,+BC&cityName=Victoria&province=BC&mode=CustomBox&alt=&isCommercial=false&zoom=12&listingtab.index=2';
const remaxVanUrl = 'https://www.remax.ca/find-real-estate/#type=all&city=VANCOUVER,+BC&neighbourhoodId=&postalCode=&queryText=VANCOUVER,+BC&east=-121.47359832910155&west=-124.00457367089842&north=49.565284136938836&south=48.82944752718503&showSchools=false&schoolTypes=0,1,2&schoolLevels=0,1,2&schoolPrograms=0,1&schoolIds=&refreshPins=true&gallery.listingPageSize=20&coordinatesFor=VANCOUVER,+BC&cityName=Vancouver&province=BC&mode=CustomBox&alt=&isCommercial=false&zoom=10&listingtab.index=2';

const percentEmitter = new EventEmitter();

export async function writeAllUrls(path: string, url: string) {
  console.log('Beginning to parse urls');
  const time = Date.now();
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle' });
  const galleryTab = await page.$('.galleryTab');
  await galleryTab.tap();

  await page.waitForNavigation({ waitUntil: 'networkidle' });
  let urls = await scrapeUrls(page);

  let i = 1;

  let nextArrow : puppeteer.ElementHandle;
  while ((nextArrow = await page.$('.nextArrow')) !== null) {
    await nextArrow.tap();
    await page.waitForNavigation({ waitUntil: 'networkidle' });
    urls = urls.concat(await scrapeUrls(page));
    cursorTo(process.stdout, 0);
    process.stdout.write(`Pages read: ${++i}`);
  }
  fs.writeFileSync(path, JSON.stringify(urls), 'utf8');
  await browser.close();
  console.log(`\nAll URLs saved! Time taken: ${Date.now() - time}ms`);
  return urls;
}

async function scrapeUrls(page: puppeteer.Page) {
  const elements = await page.$$('.teaserImage > a');
  return await Promise.all(elements.map(async x => (await x.getProperty('href')).jsonValue()));
}

function mapLimitPromise(coll, limit, mapFunc) {
  return new Promise((resolve, reject) => {
    mapLimit(coll, limit, mapFunc, (err, results) => err ? reject(err) : resolve(results));
  });
}

export async function parseListings(path: string, urls: string[]) {
  console.log('Beginning to scrape data for list of urls');
  const time = Date.now();
  // Keep track of progress
  let completed = 0;
  percentEmitter.on('update', () => {
    cursorTo(process.stdout, 0);
    process.stdout.write(`${++completed}/${urls.length}`);
  });
  const dataset = await mapLimitPromise(urls, 8, parseListing);
  fs.writeFileSync(path, JSON.stringify(dataset), 'utf8');
  console.log(`\nFinished parsing all data! Time taken: ${Date.now() - time}ms`);
}

async function parseListing(url: string) {
  try {
    const $: CheerioStatic = await request(url, { transform: (body) => cheerio.load(body) });
    const dataField = $('.property-description');
    const addressField = dataField.find('.propertyDetailsAddress');
    const address = addressField.find('.propertyAddress').text().trim().split(/\n\s*\n*/);
    const listingID = addressField.find('.propertyLastDate > span').text().trim();
    const demographicField = $('#neighbourhood');
    const averageLocalPrice = demographicField.find('.value-item.currency > span').text().trim().replace(/[\s\n]+/g, '');
    const averageLocalAge = demographicField.find('.value-item.years > .value').text();

    const data = {
      success: true,
      url: url,
      id: listingID,
      address: {
        street: address[0],
        cityState: address[1],
        postal: address[2] ? address[2].replace(/\s+/g, '') : null
      },
      price: parseFloat(dataField.text().trim().replace(/[,\$]/g, '')),
      averageLocalPrice: averageLocalPrice,
      averageLocalAge: averageLocalAge,
      walkScore: parseInt($('a.walkscore-value').text()),
      transitScore: parseInt($('a.transitscore-value').text())
    };
    
    const componentsField = dataField.find('.propertyDetailsComponents');
    componentsField.find('li').toArray().forEach( elem => {
      let propertyName = $(elem).find('.propertyName').text().replace(/[\s+:]/g, '').trim();
      propertyName = propertyName.charAt(0).toLowerCase() + propertyName.slice(1);
      const propertyValue = $(elem).find('.propertyValue').text().trim();
      const number = parseFloat(propertyValue.replace(/[,\$]/g, ''));
      data[propertyName] = isNaN(number) ? propertyValue : number;
    });
    percentEmitter.emit('update');
    return data;
  } catch(e) {
    percentEmitter.emit('update');
    return { success: false, url: url, error: e.stack };
  }
}

