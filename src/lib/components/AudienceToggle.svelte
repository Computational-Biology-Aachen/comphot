<script lang="ts">
	import { audienceStore } from '$lib/stores/audience.svelte';
</script>

<div class="audience-toggle" role="group" aria-label="Audience">
	<button
		class="toggle-btn"
		class:active={audienceStore.audience === '4bio'}
		onclick={() => audienceStore.setAudience('4bio')}
		aria-pressed={audienceStore.audience === '4bio'}
	>
		4bio
	</button>
	<button
		class="toggle-btn"
		class:active={audienceStore.audience === '4math'}
		onclick={() => audienceStore.setAudience('4math')}
		aria-pressed={audienceStore.audience === '4math'}
	>
		4math
	</button>
</div>

<style>
	.audience-toggle {
		display: flex;
		gap: 0;
		border: 1px solid var(--color-border);
		border-radius: 6px;
		overflow: hidden;
	}

	.toggle-btn {
		padding: var(--space-1) var(--space-3);
		font-size: 0.85rem;
		font-weight: 500;
		background: var(--color-bg);
		color: var(--color-text-muted);
		border: none;
		cursor: pointer;
		transition:
			background-color 0.15s,
			color 0.15s;
	}

	.toggle-btn:hover {
		background-color: var(--color-surface);
		color: var(--color-text);
	}

	.toggle-btn.active {
		background-color: var(--color-primary);
		color: #ffffff;
	}
</style>
