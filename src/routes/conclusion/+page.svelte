<script lang="ts">
	import { base } from '$app/paths';
	import PageNav from '$lib/components/PageNav.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { marked } from 'marked';
</script>

<svelte:head>
	<title>{m.con_headline_conclusion()} | ComPhot</title>
</svelte:head>

<article class="page-content">
	<div class="prose">
		{@html marked(m.con_headline_conclusion())}
	</div>

	<PageNav
		prev={{ href: '/plant-memory', label: m.sde_pagenames_plantlightmemory() }}
		next={{ href: '/contact', label: m.sde_pagenames_contact() }}
	/>

	<div class="prose">
		{@html marked(ta(m.bio_con_conclusion_text_one(), m.math_con_conclusion_text_one()))}
	</div>

	<figure class="page-figure">
		<img
			src="{base}/pictures/photosynthesis_productivity.gif"
			alt="Photosynthesis productivity animation"
			class="page-img centered"
		/>
	</figure>

	<div class="prose">
		{@html marked(m.con_conclusion_text_two())}
	</div>

	<PageNav
		prev={{ href: '/plant-memory', label: m.sde_pagenames_plantlightmemory() }}
		next={{ href: '/contact', label: m.sde_pagenames_contact() }}
	/>
</article>

<style>
	.page-content {
		max-width: var(--content-max-width);
	}

	.prose :global(h1),
	.prose :global(h2),
	.prose :global(h3) {
		margin-top: var(--space-6);
		margin-bottom: var(--space-3);
		line-height: 1.3;
	}

	.prose :global(p) {
		margin-bottom: var(--space-4);
	}

	.prose :global(ul),
	.prose :global(ol) {
		padding-left: var(--space-6);
		margin-bottom: var(--space-4);
	}

	.prose :global(a) {
		color: var(--color-primary);
	}

	.page-figure {
		margin: var(--space-6) 0;
		text-align: center;
	}

	.page-img {
		max-width: 100%;
		height: auto;
		border-radius: 4px;
	}

	.page-img.centered {
		display: block;
		margin: 0 auto;
		max-width: 70%;
	}
</style>
