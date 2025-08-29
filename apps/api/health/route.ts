export async function GET() {
  return new Response(JSON.stringify({ ok: true, service: "web" }), {
    headers: { "content-type": "application/json" },
  });
}

