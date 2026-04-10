<script lang="ts">
	interface Props {
		videoId: string;
		title?: string;
	}

	let { videoId, title = 'YouTube video' }: Props = $props();
</script>

<div class="youtube-container">
	<iframe
		src="https://www.youtube-nocookie.com/embed/{videoId}"
		{title}
		allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
		allowfullscreen
		loading="lazy"
	></iframe>
</div>

<style>
	.youtube-container {
		position: relative;
		width: 100%;
		padding-bottom: 56.25%; /* 16:9 aspect ratio */
		margin: var(--space-4) 0;
		border-radius: 6px;
		overflow: hidden;
		background: #000;
	}

	iframe {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		border: 0;
	}
</style>
