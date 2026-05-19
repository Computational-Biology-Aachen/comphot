<script lang="ts">
	import { base } from '$app/paths';
	import { PageNav } from '@computational-biology-aachen/design';
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

	<PageNav {base}
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

	<PageNav {base}
		prev={{ href: '/plant-memory', label: m.sde_pagenames_plantlightmemory() }}
		next={{ href: '/contact', label: m.sde_pagenames_contact() }}
	/>
</article>

<style>
	.page-figure {
		margin: var(--space-6) 0;
	}

	.page-img.centered {
		max-width: 70%;
	}
</style>
