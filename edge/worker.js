export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/api')) {
      const target = 'https://api.gracealoneaba.com' + url.pathname;
      return fetch(target, request);
    }
    return new Response('Grace Alone ABA Edge', { status: 200 });
  },
};
