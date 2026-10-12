export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (url.pathname === "/api/enquiry") {
      if (request.method !== "POST") {
        return Response.json(
          { ok: false, error: "Method not allowed" },
          {
            status: 405,
            headers: { Allow: "POST" }
          }
        );
      }

      return Response.json(
        {
          ok: false,
          error: "Enquiry service is not configured yet"
        },
        { status: 503 }
      );
    }

    return Response.json(
      { ok: false, error: "Not found" },
      { status: 404 }
    );
  }
};
