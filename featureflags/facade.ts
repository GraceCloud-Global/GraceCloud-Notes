import express from 'express';
import fetch from 'node-fetch';
const app = express();

const UNLEASH_PROXY = process.env.UNLEASH_PROXY || 'http://localhost:4243/proxy';

app.get('/flags/:name', async (req, res) => {
  try {
    const resp = await fetch(UNLEASH_PROXY + '/client/features', { headers: { 'x-api-key': req.headers['x-api-key'] || '' }});
    const data = await resp.json();
    const feature = data.features?.find((f: any) => f.name === req.params.name);
    res.json({ enabled: !!feature?.enabled });
  } catch (e) {
    res.json({ enabled: false });
  }
});

app.listen(4250, () => console.log('Flags facade on 4250'));
