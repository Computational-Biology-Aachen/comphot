<script lang="ts">
	interface Props {
		title: string;
		open?: boolean;
		children?: import('svelte').Snippet;
	}

	let { title, open = false, children }: Props = $props();
</script>

<details {open} class="expander">
	<summary class="expander-summary">{title}</summary>
	<div class="expander-content">
		{@render children?.()}
	</div>
</details>

<style>
	.expander {
		border: 1px solid var(--color-border);
		border-radius: 6px;
		margin: var(--space-4) 0;
		background: var(--color-surface);
	}

	.expander-summary {
		padding: var(--space-3) var(--space-4);
		cursor: pointer;
		font-weight: 500;
		list-style: none;
		user-select: none;
		display: flex;
		align-items: center;
		gap: var(--space-2);
	}

	.expander-summary::-webkit-details-marker {
		display: none;
	}

	.expander-summary::before {
		content: '▶';
		font-size: 0.7em;
		transition: transform 0.2s;
		display: inline-block;
	}

	details[open] .expander-summary::before {
		transform: rotate(90deg);
	}

	.expander-content {
		padding: var(--space-4);
		border-top: 1px solid var(--color-border);
		background: var(--color-bg);
		border-radius: 0 0 6px 6px;
	}
</style>
