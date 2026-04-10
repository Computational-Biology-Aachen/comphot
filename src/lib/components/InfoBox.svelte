<script lang="ts">
	interface Props {
		children?: import('svelte').Snippet;
	}

	let { children }: Props = $props();
</script>

<div class="info-box" role="note">
	<span class="info-icon" aria-hidden="true">ℹ</span>
	<div class="info-content">
		{@render children?.()}
	</div>
</div>

<style>
	.info-box {
		display: flex;
		gap: var(--space-3);
		padding: var(--space-4);
		background: #eff6ff;
		border: 1px solid #bfdbfe;
		border-left: 4px solid var(--color-primary);
		border-radius: 6px;
		margin: var(--space-4) 0;
		color: var(--color-text);
	}

	.info-icon {
		font-size: 1.2rem;
		line-height: 1.4;
		flex-shrink: 0;
		color: var(--color-primary);
	}

	.info-content {
		flex: 1;
		line-height: var(--line-height-base);
	}
</style>
