<script lang="ts">
	interface Props {
		loading?: boolean;
		onclick?: () => void;
		label?: string;
	}

	let { loading = false, onclick, label = 'Run simulation' }: Props = $props();
</script>

<button class="run-btn" disabled={loading} {onclick}>
	{#if loading}
		<span class="spinner" aria-hidden="true"></span>
		Running…
	{:else}
		{label}
	{/if}
</button>

<style>
	.run-btn {
		display: inline-flex;
		align-items: center;
		gap: 0.5rem;
		padding: 0.6rem 1.4rem;
		background: var(--color-primary);
		color: #fff;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: background-color 0.15s;
		width: 100%;
		justify-content: center;
	}

	.run-btn:hover:not(:disabled) {
		background: #1549a8;
	}

	.run-btn:disabled {
		opacity: 0.65;
		cursor: not-allowed;
	}

	.spinner {
		display: inline-block;
		width: 1em;
		height: 1em;
		border: 2px solid rgba(255, 255, 255, 0.4);
		border-top-color: #fff;
		border-radius: 50%;
		animation: spin 0.7s linear infinite;
		flex-shrink: 0;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}
</style>
