<script lang="ts">
	import { base } from '$app/paths';
	import Expander from '$lib/components/Expander.svelte';
	import InfoBox from '$lib/components/InfoBox.svelte';
	import PageNav from '$lib/components/PageNav.svelte';
	import VideoTranscriptToggle from '$lib/components/VideoTranscriptToggle.svelte';
	import YouTubeEmbed from '$lib/components/YouTubeEmbed.svelte';
	import { ta } from '$lib/i18n';
	import * as m from '$lib/paraglide/messages';
	import { audienceStore } from '$lib/stores/audience.svelte';
	import { marked } from 'marked';
</script>

<svelte:head>
	<title>{m.pho_headline_photosynthesis_page()} | ComPhot</title>
</svelte:head>

<article class="page-content">
	<div class="prose">
		{@html marked(m.pho_headline_photosynthesis_page())}
	</div>

	<InfoBox>
		<div class="prose">
			{@html marked(ta(m.bio_pho_learning_objectives(), m.math_pho_learning_objectives()))}
		</div>
	</InfoBox>

	<PageNav
		prev={{ href: '/', label: m.sde_pagenames_start() }}
		next={{ href: '/method', label: m.sde_pagenames_measuringmethod() }}
	/>

	<section>
		<div class="prose">
			{@html marked(m.pho_headline_climate())}
			{@html marked(
				ta(m.bio_pho_introduction_climate_change(), m.math_pho_introduction_climate_change())
			)}
		</div>

		{#if audienceStore.audience === '4math'}
			<div class="two-col-images">
				<img src="{base}/pictures/plants_basics.jpeg" alt="Plant basics" class="page-img" />
				<img src="{base}/pictures/plants_stress.jpeg" alt="Plants under stress" class="page-img" />
			</div>
		{:else}
			<div class="prose">
				{@html marked(m.bio_pho_point_1())}
				{@html marked(m.bio_pho_point_2())}
				{@html marked(m.bio_pho_point_3())}
				{@html marked(m.bio_pho_end_of_introduction())}
			</div>
		{/if}
	</section>

	<section>
		<div class="prose">
			{@html marked(m.pho_headline_photosynthesis())}
			{@html marked(
				ta(m.bio_pho_photosynthesis_explanation_1(), m.math_pho_photosynthesis_explanation_1())
			)}
			{@html marked(
				ta(m.bio_pho_photosynthesis_explanation_2(), m.math_pho_photosynthesis_explanation_2())
			)}
		</div>

		<figure class="page-figure">
			<img
				src="{base}/pictures/Fotosynthese_eng.jpg"
				alt="Photosynthesis diagram"
				class="page-img centered"
			/>
			<figcaption class="caption">
				{ta(m.bio_pho_caption_fotosynthese_picture(), m.math_pho_caption_fotosynthese_picture())}
			</figcaption>
		</figure>
	</section>

	<section>
		<div class="prose">
			{@html marked(m.pho_headline_photosynthesis_location())}
			{@html marked(
				ta(
					m.bio_pho_photosynthesis_location_explanation(),
					m.math_pho_photosynthesis_location_explanation()
				)
			)}
		</div>

		<figure class="page-figure">
			<img
				src="{base}/pictures/phot_place_upper.PNG"
				alt="Leaf cross-section showing chloroplasts"
				class="page-img centered"
			/>
			<figcaption class="caption">
				{ta(
					m.bio_pho_caption_fotosynthese_leaf_zoom(),
					m.math_pho_caption_fotosynthese_leaf_zoom()
				)}
			</figcaption>
		</figure>

		<figure class="page-figure">
			<img
				src="{base}/pictures/NPQphotosynthesis.png"
				alt="NPQ photosynthesis apparatus"
				class="page-img centered"
			/>
			<figcaption class="caption">{m.pho_caption_fotosynthese_apparat_picture()}</figcaption>
		</figure>

		<div class="prose">
			{@html marked(
				ta(
					m.bio_pho_photosynthesis_location_continue(),
					m.math_pho_photosynthesis_location_continue()
				)
			)}
		</div>
	</section>

	<section>
		<YouTubeEmbed videoId="hMCA0bBVoxE" title="Journey into a leaf" />
		<VideoTranscriptToggle
			transcript={ta(m.bio_pho_video_transcript_journey(), m.math_pho_video_transcript_journey())}
		/>
	</section>

	<section>
		<div class="prose">
			{@html marked(m.pho_headline_npq())}
			{@html marked(ta(m.bio_pho_npq_explanation(), m.math_pho_npq_explanation()))}
		</div>

		<InfoBox>
			<div class="prose">
				{@html marked(m.pho_npq_explanation_detailed())}
			</div>
		</InfoBox>

		<div class="prose">
			{@html marked(
				ta(m.bio_pho_npq_explanation_continued(), m.math_pho_npq_explanation_continued())
			)}
		</div>

		<figure class="page-figure">
			<img
				src="{base}/pictures/Violaxanthin Scheme-4.png"
				alt="Violaxanthin scheme - Xanthophyll cycle"
				class="page-img centered"
			/>
			<figcaption class="caption">
				{ta(m.bio_pho_caption_npq(), m.math_pho_caption_npq())}
			</figcaption>
		</figure>
	</section>

	<section>
		<div class="prose">
			{@html marked(m.pho_header_model_organismen())}
			{@html marked(
				ta(m.bio_pho_model_organismen_explanation(), m.math_pho_model_organismen_explanation())
			)}
		</div>

		<Expander title={m.pho_expander_model_organismen()}>
			<div class="arabidopsis-section">
				<img
					src="{base}/pictures/Arabidopsis.jpg"
					alt="Arabidopsis thaliana"
					class="arabidopsis-img"
				/>
				<p class="caption">{m.pho_caption_thaiana_picture()}</p>
			</div>
			<div class="prose">
				{@html ta(
					m.bio_pho_expander_model_organism_explanation(),
					m.math_pho_expander_model_organism_explanation()
				)}
			</div>
		</Expander>
	</section>

	{#if audienceStore.audience === '4bio'}
		<Expander title={m.literature()}>
			<div class="prose">
				<p>{m.literature_onpage()}</p>
				<ul>
					<li>
						Cook, J., Oreskes, N., Doran, P. T., Anderegg, W. R. L., Verheggen, B., Maibach, E. W.,
						Carlton, J. S., Lewandowsky, S., Skuce, A. G., Green, S. A., Nuccitelli, D., Jacobs, P.,
						Richardson, M., Winkler, B., Painting, R., &amp; Rice, K. (2016). Consensus on
						consensus: A synthesis of consensus estimates on human-caused global warming.
						Environmental Research Letters, 11(4), 048002.
						<a href="https://doi.org/10.1088/1748-9326/11/4/048002">
							https://doi.org/10.1088/1748-9326/11/4/048002
						</a>
					</li>
				</ul>
			</div>
		</Expander>
	{/if}

	<PageNav
		prev={{ href: '/', label: m.sde_pagenames_start() }}
		next={{ href: '/method', label: m.sde_pagenames_measuringmethod() }}
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

	.two-col-images {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: var(--space-4);
		margin: var(--space-4) 0;
	}

	@media (max-width: 600px) {
		.two-col-images {
			grid-template-columns: 1fr;
		}
	}

	.arabidopsis-section {
		text-align: center;
		margin-bottom: var(--space-4);
	}

	.arabidopsis-img {
		max-width: 300px;
		height: auto;
		border-radius: 4px;
	}
</style>
