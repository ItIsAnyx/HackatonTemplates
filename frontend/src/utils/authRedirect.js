export function getAuthDestination(from) {
    const pathname = from?.pathname;
    if (typeof pathname !== "string" ||
        !pathname.startsWith("/") ||
        pathname.startsWith("//") ||
        /^\/(login|register)\/?$/.test(pathname)) {
        return "/";
    }

    return {
        pathname,
        search: typeof from.search === "string" ? from.search : "",
        hash: typeof from.hash === "string" ? from.hash : "",
    };
}
