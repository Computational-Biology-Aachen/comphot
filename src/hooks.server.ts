import type { Handle } from "@sveltejs/kit/hooks";
import { getTextDirection } from "#lib/paraglide/runtime.js";
import { paraglideMiddleware } from "#lib/paraglide/server.js";

const handleParaglide: Handle = ({ event, resolve }) =>
  // event.request is readonly in SvelteKit 3; routing on the de-localized URL
  // is handled by the reroute hook in hooks.ts, so only the locale is needed here
  paraglideMiddleware(event.request, ({ locale }) => {
    return resolve(event, {
      transformPageChunk: ({ html }) =>
        html
          .replace("%paraglide.lang%", locale)
          .replace("%paraglide.dir%", getTextDirection(locale)),
    });
  });

export const handle: Handle = handleParaglide;
