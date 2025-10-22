import { serve } from 'https://deno.land/std@0.208.0/http/server.ts';

serve((req) => {
  const { pathname } = new URL(req.url);
  if (pathname === '/log') {
    req.text().then(data => console.log('🧭 Edge Log:', data));
    return new Response('ok');
  }
  return new Response('Edge API active');
});
