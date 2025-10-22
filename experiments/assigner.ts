import express from 'express';
import crypto from 'crypto';
const app = express();

function assign(userId: string, exp: string) {
  const hash = crypto.createHash('sha1').update(userId + exp).digest('hex');
  const bucket = parseInt(hash.slice(0, 4), 16) % 100;
  return bucket < 50 ? 'A' : 'B';
}

app.get('/experiments/:exp/assign', (req, res) => {
  const user = req.query.user || 'anon';
  const variant = assign(String(user), req.params.exp);
  res.json({ experiment: req.params.exp, user, variant });
});

app.listen(4260, () => console.log('Experiments assignment on 4260'));
