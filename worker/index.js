const HTML_PATHS = new Set([
  "/",
  "/privacy",
  "/privacy/",
  "/terms",
  "/terms/",
  "/sms-opt-in-proof",
  "/sms-opt-in-proof/",
]);

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const response = await env.ASSETS.fetch(request);

    if (!HTML_PATHS.has(url.pathname)) {
      return response;
    }

    const headers = new Headers(response.headers);
    headers.set("Cache-Control", "no-store, max-age=0");
    headers.set("X-EquineSync-Compliance-Site", "twilio-a2p-review");
    return new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers,
    });
  },
};
