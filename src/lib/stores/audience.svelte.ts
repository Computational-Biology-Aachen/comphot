import { browser } from "$app/env";

export type Audience = "4bio" | "4math";

const STORAGE_KEY = "comphot-audience";

function readStored(): Audience {
  if (browser) {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored === "4bio" || stored === "4math") return stored;
    } catch {
      // Storage blocked (privacy mode, sandbox): fall back to the default.
    }
  }
  return "4bio";
}

class AudienceStore {
  audience = $state<Audience>(readStored());

  setAudience(v: Audience) {
    this.audience = v;
    if (browser) {
      try {
        localStorage.setItem(STORAGE_KEY, v);
      } catch {
        // Not persisted; the choice still applies for this visit.
      }
    }
  }
}

export const audienceStore = new AudienceStore();
