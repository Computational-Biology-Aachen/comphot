<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion,
    H1,
    H2,
    InfoBox,
    Li,
    SectionMain as Main,
    PageNav,
    Text,
    Ol,
    Ul,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.pho_headline_photosynthesis_page()} | ComPhot</title>
</svelte:head>

<Main
  width="narrow"
  align="start"
>
  <H1>
    {@html marked.parseInline(m.pho_headline_photosynthesis_page())}
  </H1>

  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_pho_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_pho_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.math_pho_lo_3())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_pho_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_lo_3())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_lo_4())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <InfoBox header="What you need to know">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_pho_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.math_pho_prereq_2())}</Li>
        <Li>{@html marked.parseInline(m.math_pho_prereq_3())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_pho_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_prereq_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_prereq_3())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_prereq_4())}</Li>
        <Li>{@html marked.parseInline(m.bio_pho_prereq_5())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/", label: m.sde_pagenames_start() }}
    next={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
  />

  <H2>
    {@html marked.parseInline(m.pho_headline_climate())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_introduction_climate_change(),
        m.math_pho_introduction_climate_change(),
      ),
    )}
  </Text>

  {#if audienceStore.audience === "4math"}
    <img
      src="{base}/pictures/plants_basics.jpeg"
      alt="Plant basics"
      class="page-img"
    />
    <img
      src="{base}/pictures/plants_stress.jpeg"
      alt="Plants under stress"
      class="page-img"
    />
  {:else}
    <Ul>
      <Li>{m.bio_pho_point_1()}</Li>
      <Li>{m.bio_pho_point_2()}</Li>
      <Li>{m.bio_pho_point_3()}</Li>
    </Ul>
    <Text>{@html marked.parseInline(m.bio_pho_end_of_introduction())}</Text>
  {/if}

  <H2>
    {@html marked.parseInline(m.pho_headline_photosynthesis())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_photosynthesis_explanation_1(),
        m.math_pho_photosynthesis_explanation_1(),
      ),
    )}
    {@html marked.parseInline(
      ta(
        m.bio_pho_photosynthesis_explanation_2(),
        m.math_pho_photosynthesis_explanation_2(),
      ),
    )}
  </Text>

  <figure class="page-figure">
    <img
      src="{base}/pictures/Fotosynthese_eng.jpg"
      alt="Photosynthesis diagram"
      class="page-img centered"
    />
    <figcaption class="caption">
      {ta(
        m.bio_pho_caption_fotosynthese_picture(),
        m.math_pho_caption_fotosynthese_picture(),
      )}
    </figcaption>
  </figure>

  <H2>
    {@html marked.parseInline(m.pho_headline_photosynthesis_location())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_photosynthesis_location_explanation(),
        m.math_pho_photosynthesis_location_explanation(),
      ),
    )}
  </Text>

  <figure class="page-figure">
    <img
      src="{base}/pictures/phot_place_upper.PNG"
      alt="Leaf cross-section showing chloroplasts"
      class="page-img centered"
    />
    <figcaption class="caption">
      {ta(
        m.bio_pho_caption_fotosynthese_leaf_zoom(),
        m.math_pho_caption_fotosynthese_leaf_zoom(),
      )}
    </figcaption>
  </figure>

  <figure class="page-figure">
    <img
      src="{base}/pictures/NPQphotosynthesis.png"
      alt="NPQ photosynthesis apparatus"
      class="page-img centered"
    />
    <figcaption class="caption">
      {m.pho_caption_fotosynthese_apparat_picture()}
    </figcaption>
  </figure>

  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_photosynthesis_location_continue(),
        m.math_pho_photosynthesis_location_continue(),
      ),
    )}
  </Text>

  <YouTubeEmbed
    videoId="hMCA0bBVoxE"
    title="Journey into a leaf"
  />

  <!-- SECTION -->

  <H2>
    {@html marked.parseInline(m.pho_headline_npq())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(m.bio_pho_npq_explanation(), m.math_pho_npq_explanation()),
    )}
  </Text>

  <InfoBox header="Learning objectives">
    <Text>
      {@html marked.parseInline(m.pho_npq_explanation_detailed())}
    </Text>
  </InfoBox>

  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_npq_explanation_continued(),
        m.math_pho_npq_explanation_continued(),
      ),
    )}
  </Text>

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

  <!-- SECTION -->

  <H2>
    {@html marked.parseInline(m.pho_header_model_organismen())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_pho_model_organismen_explanation(),
        m.math_pho_model_organismen_explanation(),
      ),
    )}
  </Text>

  <Accordion title={m.pho_expander_model_organismen()}>
    <img
      src="{base}/pictures/Arabidopsis.jpg"
      alt="Arabidopsis thaliana"
      class="arabidopsis-img"
    />
    <p class="caption">{m.pho_caption_thaiana_picture()}</p>

    <Text>{@html m.pho_model_organism_intro()}</Text>
    <ol class="content-ol">
      <li>{@html m.pho_model_organism_item1()}</li>
      <li>{@html m.pho_model_organism_item2()}</li>
      <li>{@html m.pho_model_organism_item3()}</li>
      <li>{@html m.pho_model_organism_item4()}</li>
    </ol>
    <Text>{@html m.pho_model_organism_outro()}</Text>
  </Accordion>

  <Accordion title={m.literature()}>
    <Text>
      <p>{m.literature_onpage()}</p>
      <Ol>
        <Li>
          Cook, J., Oreskes, N., Doran, P. T., Anderegg, W. R. L., Verheggen,
          B., Maibach, E. W., Carlton, J. S., Lewandowsky, S., Skuce, A. G.,
          Green, S. A., Nuccitelli, D., Jacobs, P., Richardson, M., Winkler, B.,
          Painting, R., &amp; Rice, K. (2016). Consensus on consensus: A
          synthesis of consensus estimates on human-caused global warming.
          Environmental Research Letters, 11(4), 048002.
          <a href="https://doi.org/10.1088/1748-9326/11/4/048002">
            https://doi.org/10.1088/1748-9326/11/4/048002
          </a>
        </Li>
      </Ol>
    </Text>
  </Accordion>

  <PageNav
    base={base}
    prev={{ href: "/", label: m.sde_pagenames_start() }}
    next={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
  />
</Main>

<style>
  .content-ol {
    display: grid;
    gap: var(--space-1);
    padding-bottom: var(--space-4);
    padding-left: 2rem;
  }
</style>
