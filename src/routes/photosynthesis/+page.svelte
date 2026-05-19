<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion as Expander,
    H1,
    H2,
    InfoBox,
    Main,
    Narrow,
    PageNav,
    Text,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.pho_headline_photosynthesis_page()} | ComPhot</title>
</svelte:head>

<Main>
  <Narrow>
    <H1>
      {@html marked.parseInline(m.pho_headline_photosynthesis_page())}
    </H1>

    <InfoBox variant="info">
      <Text>
        {@html marked.parseInline(
          ta(m.bio_pho_learning_objectives(), m.math_pho_learning_objectives()),
        )}
      </Text>
    </InfoBox>

    <PageNav
      base={base}
      prev={{ href: "/", label: m.sde_pagenames_start() }}
      next={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    />

    <section>
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
        <Text>
          {@html marked.parseInline(m.bio_pho_point_1())}
          {@html marked.parseInline(m.bio_pho_point_2())}
          {@html marked.parseInline(m.bio_pho_point_3())}
          {@html marked.parseInline(m.bio_pho_end_of_introduction())}
        </Text>
      {/if}
    </section>

    <section>
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
    </section>

    <section>
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
    </section>

    <section>
      <YouTubeEmbed
        videoId="hMCA0bBVoxE"
        title="Journey into a leaf"
      />
    </section>

    <!-- SECTION -->
    <section>
      <H2>
        {@html marked.parseInline(m.pho_headline_npq())}
      </H2>
      <Text>
        {@html marked.parseInline(
          ta(m.bio_pho_npq_explanation(), m.math_pho_npq_explanation()),
        )}
      </Text>

      <InfoBox>
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
    </section>

    <!-- SECTION -->
    <section>
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

      <Expander title={m.pho_expander_model_organismen()}>
        <img
          src="{base}/pictures/Arabidopsis.jpg"
          alt="Arabidopsis thaliana"
          class="arabidopsis-img"
        />
        <p class="caption">{m.pho_caption_thaiana_picture()}</p>

        <Text>
          {@html ta(
            m.bio_pho_expander_model_organism_explanation(),
            m.math_pho_expander_model_organism_explanation(),
          )}
        </Text>
      </Expander>
    </section>

    <Expander title={m.literature()}>
      <Text>
        <p>{m.literature_onpage()}</p>
        <ul>
          <li>
            Cook, J., Oreskes, N., Doran, P. T., Anderegg, W. R. L., Verheggen,
            B., Maibach, E. W., Carlton, J. S., Lewandowsky, S., Skuce, A. G.,
            Green, S. A., Nuccitelli, D., Jacobs, P., Richardson, M., Winkler,
            B., Painting, R., &amp; Rice, K. (2016). Consensus on consensus: A
            synthesis of consensus estimates on human-caused global warming.
            Environmental Research Letters, 11(4), 048002.
            <a href="https://doi.org/10.1088/1748-9326/11/4/048002">
              https://doi.org/10.1088/1748-9326/11/4/048002
            </a>
          </li>
        </ul>
      </Text>
    </Expander>

    <PageNav
      base={base}
      prev={{ href: "/", label: m.sde_pagenames_start() }}
      next={{ href: "/method", label: m.sde_pagenames_measuringmethod() }}
    />
  </Narrow>
</Main>
