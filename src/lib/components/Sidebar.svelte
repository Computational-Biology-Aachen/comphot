<script lang="ts">
	import { base } from '$app/paths';
	import { page } from '$app/state';

	const navLinks = [
		{ href: '/', label: 'Home' },
		{ href: '/photosynthesis', label: 'Photosynthesis' },
		{ href: '/method', label: 'Method' },
		{ href: '/model', label: 'Model' },
		{ href: '/experiments', label: 'Experiments' },
		{ href: '/plant-memory', label: 'Plant Memory' },
		{ href: '/conclusion', label: 'Conclusion' },
		{ href: '/contact', label: 'Contact' }
	];

	let menuOpen = $state(false);

	function toggleMenu() {
		menuOpen = !menuOpen;
	}
</script>

<aside class="sidebar" class:open={menuOpen}>
	<button class="hamburger" aria-label="Toggle navigation" onclick={toggleMenu}>
		<span></span>
		<span></span>
		<span></span>
	</button>
	<nav class="sidebar-nav" aria-label="Main navigation">
		{#each navLinks as link (link.href)}
			{@const href = `${base}${link.href}`}
			{@const isActive =
				page.url.pathname === href || (link.href !== '/' && page.url.pathname.startsWith(href))}
			<a
				{href}
				class="nav-link"
				class:active={isActive}
				aria-current={isActive ? 'page' : undefined}
				onclick={() => {
					menuOpen = false;
				}}
			>
				{link.label}
			</a>
		{/each}
	</nav>
</aside>

<style>
	.sidebar {
		width: var(--sidebar-width);
		min-height: calc(100vh - var(--nav-height));
		background-color: var(--color-surface);
		border-right: 1px solid var(--color-border);
		padding: var(--space-6) 0;
		flex-shrink: 0;
	}

	.hamburger {
		display: none;
		flex-direction: column;
		gap: 5px;
		padding: var(--space-3) var(--space-4);
		background: none;
		border: none;
		cursor: pointer;
	}

	.hamburger span {
		display: block;
		width: 22px;
		height: 2px;
		background-color: var(--color-text);
		border-radius: 2px;
	}

	.sidebar-nav {
		display: flex;
		flex-direction: column;
	}

	.nav-link {
		display: block;
		padding: var(--space-2) var(--space-6);
		text-decoration: none;
		color: var(--color-text-muted);
		font-size: 0.9rem;
		font-weight: 400;
		border-left: 3px solid transparent;
		transition:
			color 0.15s,
			border-color 0.15s,
			background-color 0.15s;
	}

	.nav-link:hover {
		color: var(--color-text);
		background-color: var(--color-border);
	}

	.nav-link.active {
		color: var(--color-primary);
		border-left-color: var(--color-primary);
		font-weight: 500;
		background-color: rgba(28, 91, 199, 0.07);
	}

	@media (max-width: 768px) {
		.sidebar {
			width: 100%;
			min-height: unset;
			border-right: none;
			border-bottom: 1px solid var(--color-border);
			padding: 0;
		}

		.hamburger {
			display: flex;
		}

		.sidebar-nav {
			display: none;
		}

		.sidebar.open .sidebar-nav {
			display: flex;
		}
	}
</style>
