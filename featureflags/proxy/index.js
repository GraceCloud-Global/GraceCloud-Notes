const { createApp } = require('@unleash/proxy');
const express = require('express');
const app = express();
const unleash = createApp({
  unleashUrl: process.env.UNLEASH_URL || 'http://localhost:4242/api/',
  unleashApiToken: process.env.UNLEASH_API_TOKEN || 'default:development.unleash-insecure-api-token',
  clientKeys: [process.env.UNLEASH_CLIENT_KEY || 'public-key'],
});

app.use('/proxy', unleash);
app.listen(4243, () => console.log('Unleash proxy on 4243'));
