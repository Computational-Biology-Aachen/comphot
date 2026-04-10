<script lang="ts">
	import { marked } from 'marked';
	import { base } from '$app/paths';
	import { t } from '$lib/i18n';
	import PageNav from '$lib/components/PageNav.svelte';
	import Expander from '$lib/components/Expander.svelte';
	import YouTubeEmbed from '$lib/components/YouTubeEmbed.svelte';
	import InfoBox from '$lib/components/InfoBox.svelte';
	import VideoTranscriptToggle from '$lib/components/VideoTranscriptToggle.svelte';
</script>

<svelte:head>
	<title>{t('mth_headline_one')} | ComPhot</title>
</svelte:head>

<article class="page-content">
	<div class="prose">
		{@html marked(t('mth_headline_one'))}
	</div>

	<InfoBox>
		<div class="prose">
			{@html marked(t('mth_learning_objectives'))}
		</div>
	</InfoBox>

	<PageNav
		prev={{ href: '/photosynthesis', label: t('sde_pagenames_photosynthesis') }}
		next={{ href: '/model', label: t('sde_pagenames_computationalmodels') }}
	/>

	<section class="gif-section">
		<div class="gif-container">
			<img
				src="{base}/pictures/Kurzvideo-Messmethode.gif"
				alt="PAM measurement short video"
				class="gif-img"
			/>
		</div>
	</section>

	<div class="prose">
		{@html marked(t('mth_introduction_measurement'))}
	</div>

	<figure class="page-figure">
		<img
			src="{base}/pictures/Foto-Fluoreszierende_Pflanzen.jpg"
			alt="A plant fluorescing under UV light"
			class="page-img"
		/>
		<figcaption class="caption">{t('mth_caption_abb1')}</figcaption>
	</figure>

	<Expander title={t('mth_growing_plants_1')} open={true}>
		<div class="prose">
			{@html marked(t('mth_introduction_glowing'))}
			{@html marked(t('mth_plant_are_shining_red'))}
			{@html marked(t('mth_introduction_experiment'))}
		</div>
		<YouTubeEmbed videoId="g3uTNWsDEdo" title="Chlorophyll fluorescence experiment" />
		<div class="prose">
			{@html marked(t('mth_explanation_video'))}
		</div>
	</Expander>

	<Expander title={t('mth_measuring_fluoreszenz')} open={true}>
		<div class="prose">
			{@html marked(t('mth_explanation_measurement_1'))}
			{@html marked(t('mth_introduction_phi'))}
		</div>
		<YouTubeEmbed videoId="EwXkOlMBl3o" title="Measuring fluorescence with PAM" />
	</Expander>

	<VideoTranscriptToggle transcriptKey="mth_video_transcript_pam" />

	<div class="prose">
		{@html marked(t('mth_headline_pam_measurement'))}
		{@html marked(t('mth_introduction_pam_measurement'))}
	</div>

	<Expander title={t('mth_measuring_light_fluorescence')} open={true}>
		<div class="prose">
			{@html marked(t('mth_explanation_introduction_attempts'))}
		</div>
		<figure class="page-figure">
			<img
				src="{base}/pictures/PAMbasics.png"
				alt="PAM basics diagram"
				class="page-img centered"
			/>
			<figcaption class="caption">{t('mth_caption_abb2')}</figcaption>
		</figure>
	</Expander>

	<section>
		<div class="prose">
			{@html marked(t('mth_headline_illustration'))}
			{@html marked(t('mth_explanation_illustration_units'))}
			{@html marked(t('mth_explanation_illustration'))}
		</div>

		<figure class="page-figure">
			<img
				src="{base}/pictures/Beispielabbildung_en.png"
				alt="Example PAM measurement result"
				class="page-img"
			/>
			<figcaption class="caption">{t('mth_caption_abb2')}</figcaption>
		</figure>
	</section>

	<Expander title={t('literature')}>
		<div class="prose">
			{@html marked(t('mth_literature_declaration'))}
			<ul>
				<li>
					Brooks, M. D., &amp; Niyogi, K. K. (2011). Use of a pulse-amplitude modulated chlorophyll
					fluorometer to study the efficiency of photosynthesis in Arabidopsis plants. Chloroplast
					Research in Arabidopsis: Methods and Protocols, Volume II, 299–310.
					<a href="https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16">
						https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16
					</a>
				</li>
				<li>
					Nies, T., Niu, Y., Ebenhöh, O., Matsubara, S., &amp; Matuszyńska, A. (2021). Chlorophyll
					fluorescence: How the quality of information about PAM instrument parameters may affect our
					research. bioRxiv.
					<a href="https://doi.org/10.1101/2021.05.12.443801">
						https://doi.org/10.1101/2021.05.12.443801
					</a>
				</li>
			</ul>
		</div>
	</Expander>

	<PageNav
		prev={{ href: '/photosynthesis', label: t('sde_pagenames_photosynthesis') }}
		next={{ href: '/model', label: t('sde_pagenames_computationalmodels') }}
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

	section {
		margin: var(--space-8) 0;
	}

	.gif-section {
		display: flex;
		justify-content: center;
		margin: var(--space-6) 0;
	}

	.gif-container {
		max-width: 400px;
	}

	.gif-img {
		width: 100%;
		height: auto;
		border-radius: 4px;
	}

	.page-figure {
		margin: var(--space-4) 0;
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
		max-width: 80%;
	}

	.caption {
		font-size: 0.875rem;
		color: var(--color-text-muted);
		text-align: center;
		margin-top: var(--space-2);
	}
</style>
