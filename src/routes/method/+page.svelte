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
    Ul,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.mth_headline_one()} | ComPhot</title>
</svelte:head>

<Main
  width="narrow"
  align="start"
>
  <H1>
    {@html marked.parseInline(m.mth_headline_one())}
  </H1>

  <InfoBox header="Learning objectives">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mth_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.math_mth_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.math_mth_lo_3())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mth_lo_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mth_lo_2())}</Li>
        <Li>{@html marked.parseInline(m.bio_mth_lo_3())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <InfoBox header="What you need to know">
    {#if audienceStore.audience === "4math"}
      <Ul>
        <Li>{@html marked.parseInline(m.math_mth_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.math_mth_prereq_2())}</Li>
      </Ul>
    {:else}
      <Ul>
        <Li>{@html marked.parseInline(m.bio_mth_prereq_1())}</Li>
        <Li>{@html marked.parseInline(m.bio_mth_prereq_2())}</Li>
      </Ul>
    {/if}
  </InfoBox>

  <PageNav
    base={base}
    prev={{
      href: "/photosynthesis",
      label: m.sde_pagenames_photosynthesis(),
    }}
    next={{ href: "/model", label: m.sde_pagenames_computationalmodels() }}
  />

  <img
    src="{base}/pictures/Kurzvideo-Messmethode.gif"
    alt="PAM measurement short video"
    class="gif-img"
  />

  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_mth_introduction_measurement(),
        m.math_mth_introduction_measurement(),
      ),
    )}
  </Text>

  <figure class="page-figure">
    <img
      src="{base}/pictures/Foto-Fluoreszierende_Pflanzen.jpg"
      alt="A plant fluorescing under UV light"
      class="page-img"
    />
    <figcaption class="caption">{m.mth_caption_abb1()}</figcaption>
  </figure>

  <Accordion
    title={ta(m.bio_mth_growing_plants_1(), m.math_mth_growing_plants_1())}
    open={false}
  >
    <Text>
      {@html marked.parseInline(
        ta(m.bio_mth_introduction_glowing(), m.math_mth_introduction_glowing()),
      )}
      {@html marked.parseInline(
        ta(
          m.bio_mth_plant_are_shining_red(),
          m.math_mth_plant_are_shining_red(),
        ),
      )}
      {@html marked.parseInline(
        ta(
          m.bio_mth_introduction_experiment(),
          m.math_mth_introduction_experiment(),
        ),
      )}
    </Text>
    <YouTubeEmbed
      videoId="g3uTNWsDEdo"
      title="Chlorophyll fluorescence experiment"
    />
    <Text>
      {@html marked.parseInline(
        ta(m.bio_mth_explanation_video(), m.math_mth_explanation_video()),
      )}
    </Text>
  </Accordion>

  <Accordion
    title={m.mth_measuring_fluoreszenz()}
    open={false}
  >
    <Text>
      {@html marked.parseInline(
        ta(
          m.bio_mth_explanation_measurement_1(),
          m.math_mth_explanation_measurement_1(),
        ),
      )}
      {@html marked.parseInline(
        ta(m.bio_mth_introduction_phi(), m.math_mth_introduction_phi()),
      )}
    </Text>
    <YouTubeEmbed
      videoId="EwXkOlMBl3o"
      title="Measuring fluorescence with PAM"
    />
  </Accordion>

  <H2>
    {@html marked.parseInline(m.mth_headline_pam_measurement())}
  </H2>
  <Text>
    {@html marked.parseInline(
      ta(
        m.bio_mth_introduction_pam_measurement(),
        m.math_mth_introduction_pam_measurement(),
      ),
    )}
  </Text>

  <Accordion
    title={m.mth_measuring_light_fluorescence()}
    open={false}
  >
    <Text>
      {@html marked.parseInline(
        ta(
          m.bio_mth_explanation_introduction_attempts(),
          m.math_mth_explanation_introduction_attempts(),
        ),
      )}
    </Text>
    <figure class="page-figure">
      <img
        src="{base}/pictures/PAMbasics.png"
        alt="PAM basics diagram"
        class="page-img centered"
      />
      <figcaption class="caption">{m.mth_caption_abb2()}</figcaption>
    </figure>
  </Accordion>

  <H2>
    {@html marked.parseInline(m.mth_headline_illustration())}
  </H2>
  <Text>
    {@html marked.parseInline(m.mth_explanation_illustration_units())}
    {@html marked.parseInline(m.mth_explanation_illustration())}
  </Text>

  <figure class="page-figure">
    <img
      src="{base}/pictures/Beispielabbildung_en.png"
      alt="Example PAM measurement result"
      class="page-img"
    />
    <figcaption class="caption">{m.mth_caption_abb2()}</figcaption>
  </figure>

  <Accordion title={m.literature()}>
    <Text>
      {@html marked.parseInline(m.mth_literature_declaration())}
      <ul>
        <li>
          Brooks, M. D., &amp; Niyogi, K. K. (2011). Use of a pulse-amplitude
          modulated chlorophyll fluorometer to study the efficiency of
          photosynthesis in Arabidopsis plants. Chloroplast Research in
          Arabidopsis: Methods and Protocols, Volume II, 299-310.
          <a
            href="https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16"
          >
            https://link.springer.com/protocol/10.1007/978-1-61779-237-3_16
          </a>
        </li>
        <li>
          Nies, T., Niu, Y., Ebenhöh, O., Matsubara, S., &amp; Matuszyńska, A.
          (2021). Chlorophyll fluorescence: How the quality of information about
          PAM instrument parameters may affect our research. bioRxiv.
          <a href="https://doi.org/10.1101/2021.05.12.443801">
            https://doi.org/10.1101/2021.05.12.443801
          </a>
        </li>
      </ul>
    </Text>
  </Accordion>

  <PageNav
    base={base}
    prev={{
      href: "/photosynthesis",
      label: m.sde_pagenames_photosynthesis(),
    }}
    next={{ href: "/model", label: m.sde_pagenames_computationalmodels() }}
  />
</Main>
