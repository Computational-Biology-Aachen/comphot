<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import { locales, localizeHref } from '$lib/paraglide/runtime';

	// Use route ID (without base) so localizeHref works correctly
	function routePath() {
		return page.route.id ?? '/';
	}
</script>

<nav class="lang-switcher" aria-label="Language">
	{#each locales as locale (locale)}
		<a
			href="{base}{localizeHref(routePath(), { locale })}"
			class="lang-link"
			aria-label="Switch to {locale}"
		>
			{locale.toUpperCase()}
		</a>
	{/each}
</nav>

<style>
	.lang-switcher {
		display: flex;
		gap: var(--space-2);
		align-items: center;
	}

	.lang-link {
		font-size: 0.85rem;
		font-weight: 500;
		color: var(--color-text-muted);
		text-decoration: none;
		padding: var(--space-1) var(--space-2);
		border-radius: 4px;
		transition: color 0.15s, background-color 0.15s;
	}

	.lang-link:hover {
		color: var(--color-primary);
		background-color: var(--color-surface);
	}
</style>
