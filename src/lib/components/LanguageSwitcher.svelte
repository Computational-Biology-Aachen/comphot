<script lang="ts">
	import { setLocale, getLocale } from '$lib/paraglide/runtime';

	const LOCALES = [
		{ code: 'en', label: 'EN' },
		{ code: 'de', label: 'DE' },
		{ code: 'fr', label: 'FR' }
	] as const;

	let currentLocale = $state(getLocale());

	function switchLocale(code: (typeof LOCALES)[number]['code']) {
		setLocale(code);
		currentLocale = getLocale();
	}
</script>

<div class="lang-switcher">
	{#each LOCALES as { code, label }}
		<button
			class="lang-btn"
			class:active={currentLocale === code}
			onclick={() => switchLocale(code)}
		>
			{label}
		</button>
	{/each}
</div>

<style>
	.lang-switcher {
		display: flex;
		gap: 2px;
	}

	.lang-btn {
		padding: 3px 8px;
		border: 1px solid var(--color-border);
		border-radius: 4px;
		background: transparent;
		color: var(--color-text-muted);
		font-size: 0.8rem;
		font-weight: 500;
		cursor: pointer;
		line-height: 1;
		transition:
			color 0.15s,
			background 0.15s,
			border-color 0.15s;
	}

	.lang-btn:hover {
		color: var(--color-text);
		border-color: var(--color-text-muted);
	}

	.lang-btn.active {
		background: var(--color-primary);
		border-color: var(--color-primary);
		color: #fff;
	}
</style>
