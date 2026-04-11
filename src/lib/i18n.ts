import { audienceStore } from '$lib/stores/audience.svelte';

/**
 * Selects the bio or math message variant based on the current audience.
 * Use this when a key has both a `bio_` and `math_` variant.
 *
 * @example
 * ta(m.bio_fal_learning_objectives(), m.math_fal_learning_objectives())
 */
export function ta<T>(bio: T, math: T): T {
	return audienceStore.audience === '4math' ? math : bio;
}
