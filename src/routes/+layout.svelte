<script lang="ts">
	import '../app.css';
	import { locales, localizeHref } from '$lib/paraglide/runtime';
	import { base } from '$app/paths';
	import { page } from '$app/state';
	import favicon from '$lib/assets/favicon.svg';
	import Navbar from '$lib/components/Navbar.svelte';
	import Sidebar from '$lib/components/Sidebar.svelte';

	let { children } = $props();

	// Get the route path without base prefix for localizeHref
	function routePath() {
		const routeId = page.route.id ?? '/';
		return routeId;
	}
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<!-- Alternate locale links for crawlers -->
	{#each locales as locale (locale)}
		<link rel="alternate" hreflang={locale} href="{base}{localizeHref(routePath(), { locale })}" />
	{/each}
</svelte:head>

<Navbar />

<div class="app-body">
	<Sidebar />
	<main class="content">
		{@render children()}
	</main>
</div>

<!-- Hidden locale links for Paraglide's prerender crawler -->
<div style="display:none">
	{#each locales as locale (locale)}
		<a href="{base}{localizeHref(routePath(), { locale })}">{locale}</a>
	{/each}
</div>

<style>
	.app-body {
		display: flex;
		min-height: calc(100vh - var(--nav-height));
	}

	.content {
		flex: 1;
		padding: var(--space-8);
		max-width: var(--content-max-width);
		min-width: 0;
	}
</style>
