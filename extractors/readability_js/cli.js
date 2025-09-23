#!/usr/bin/env node
const { Readability } = require('@mozilla/readability')
const { JSDOM } = require('jsdom')
const { readFileSync } = require('node:fs')

const html = readFileSync(0, 'utf-8')

var doc = new JSDOM(html, { url: "https://fake-url.com" })

const reader = new Readability(doc.window.document)
const article = reader.parse()

console.log(article.textContent)
