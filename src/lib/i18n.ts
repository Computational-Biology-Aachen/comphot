import * as m from '$lib/paraglide/messages';
import { audienceStore } from '$lib/stores/audience.svelte';

type MessageFn = () => string;
type MessageModule = typeof m;

function callMessage(mod: MessageModule, key: string): string | null {
	if (key in mod) {
		const fn = mod[key as keyof MessageModule];
		if (typeof fn === 'function') {
			return (fn as unknown as MessageFn)();
		}
	}
	return null;
}

/**
 * Resolves a message key with audience-aware fallback.
 *
 * If a `bio_<key>` or `math_<key>` variant exists for the current audience,
 * that variant is returned. Otherwise the plain unprefixed key is used.
 */
export function t(key: string): string {
	const audience = audienceStore.audience;
	// Try audience-prefixed variant first (e.g. "bio_fal_headline_experiments")
	const audienceResult = callMessage(m, `${audience}_${key}`);
	if (audienceResult !== null) return audienceResult;
	// Fall back to unprefixed key
	const baseResult = callMessage(m, key);
	if (baseResult !== null) return baseResult;
	// Last resort: return the key itself
	return key;
}
