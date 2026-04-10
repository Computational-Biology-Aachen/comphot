<script lang="ts">
	import { base } from '$app/paths';

	interface NavLink {
		href: string;
		label: string;
	}

	interface Props {
		prev?: NavLink;
		next?: NavLink;
	}

	let { prev, next }: Props = $props();
</script>

<nav class="page-nav" aria-label="Page navigation">
	<div class="page-nav-prev">
		{#if prev}
			<a href="{base}{prev.href}" class="page-nav-btn">
				<span class="arrow" aria-hidden="true">←</span>
				{prev.label}
			</a>
		{/if}
	</div>
	<div class="page-nav-next">
		{#if next}
			<a href="{base}{next.href}" class="page-nav-btn">
				{next.label}
				<span class="arrow" aria-hidden="true">→</span>
			</a>
		{/if}
	</div>
</nav>

<style>
	.page-nav {
		display: flex;
		justify-content: space-between;
		margin-top: var(--space-12);
		padding-top: var(--space-6);
		border-top: 1px solid var(--color-border);
	}

	.page-nav-prev,
	.page-nav-next {
		display: flex;
	}

	.page-nav-btn {
		display: inline-flex;
		align-items: center;
		gap: var(--space-2);
		padding: var(--space-2) var(--space-4);
		font-size: 0.9rem;
		font-weight: 500;
		color: var(--color-primary);
		text-decoration: none;
		border: 1px solid var(--color-border);
		border-radius: 6px;
		transition:
			background-color 0.15s,
			border-color 0.15s;
	}

	.page-nav-btn:hover {
		background-color: var(--color-surface);
		border-color: var(--color-primary);
		color: var(--color-primary);
	}

	.arrow {
		font-size: 1rem;
	}
</style>
