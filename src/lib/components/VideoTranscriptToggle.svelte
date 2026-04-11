<script lang="ts">
	import * as m from '$lib/paraglide/messages';

	interface Props {
		transcript: string;
	}

	let { transcript }: Props = $props();

	let showTranscript = $state(false);
</script>

<div class="transcript-toggle">
	<button
		type="button"
		class="transcript-btn"
		onclick={() => (showTranscript = !showTranscript)}
		aria-expanded={showTranscript}
	>
		{showTranscript ? '▼' : '▶'}
		{m.expander_video_transcript()}
	</button>
	{#if showTranscript}
		<div class="transcript-content">
			{transcript}
		</div>
	{/if}
</div>

<style>
	.transcript-toggle {
		margin: var(--space-4) 0;
	}

	.transcript-btn {
		background: none;
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: var(--space-2) var(--space-4);
		cursor: pointer;
		font-size: 0.9rem;
		color: var(--color-text-muted);
		display: flex;
		align-items: center;
		gap: var(--space-2);
		transition:
			background-color 0.15s,
			color 0.15s;
	}

	.transcript-btn:hover {
		background-color: var(--color-surface);
		color: var(--color-text);
	}

	.transcript-content {
		margin-top: var(--space-3);
		padding: var(--space-4);
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		font-size: 0.9rem;
		line-height: var(--line-height-base);
		white-space: pre-wrap;
	}
</style>
