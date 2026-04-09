<script lang="ts">
	import { resolve } from '$app/paths';
	import LanguageSwitcher from './LanguageSwitcher.svelte';
	import AudienceToggle from './AudienceToggle.svelte';
</script>

<header class="navbar">
	<a href={resolve('/')} class="navbar-brand">ComPhot</a>
	<div class="navbar-actions">
		<LanguageSwitcher />
		<AudienceToggle />
	</div>
</header>

<style>
	.navbar {
		position: sticky;
		top: 0;
		z-index: 100;
		height: var(--nav-height);
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 0 var(--space-6);
		background-color: var(--color-bg);
		border-bottom: 1px solid var(--color-border);
		box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
	}

	.navbar-brand {
		font-size: 1.2rem;
		font-weight: 700;
		color: var(--color-text);
		text-decoration: none;
		letter-spacing: -0.01em;
	}

	.navbar-brand:hover {
		color: var(--color-primary);
	}

	.navbar-actions {
		display: flex;
		align-items: center;
		gap: var(--space-4);
	}
</style>
