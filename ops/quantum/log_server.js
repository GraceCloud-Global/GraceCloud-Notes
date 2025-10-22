import fs from 'fs';
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ port: 7071 });
wss.on('connection', ws => {
  ws.on('message', msg => {
    const log = { time: new Date().toISOString(), msg: msg.toString() };
    fs.appendFileSync('ops/quantum/logs.txt', JSON.stringify(log) + '\n');
  });
});

console.log('🔭 Quantum Log Collector @7071');
