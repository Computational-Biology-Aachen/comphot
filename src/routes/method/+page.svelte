<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import VideoTranscriptToggle, {
    Accordion as Expander,
    InfoBox,
    PageNav,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<svelte:head>
  <title>{m.mth_headline_one()} | ComPhot</title>
</svelte:head>

<article class="page-content">
  <div class="prose">
    {@html marked(m.mth_headline_one())}
  </div>

  <InfoBox>
    <div class="prose">
      {@html marked(
        ta(m.bio_mth_learning_objectives(), m.math_mth_learning_objectives()),
      )}
    </div>
  </InfoBox>

  <PageNav
    base={base}
    prev={{ href: "/photosynthesis", label: m.sde_pagenames_photosynthesis() }}
    next={{ href: "/model", label: m.sde_pagenames_computationalmodels() }}
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
    {@html marked(
      ta(
        m.bio_mth_introduction_measurement(),
        m.math_mth_introduction_measurement(),
      ),
    )}
  </div>

  <figure class="page-figure">
    <img
      src="{base}/pictures/Foto-Fluoreszierende_Pflanzen.jpg"
      alt="A plant fluorescing under UV light"
      class="page-img"
    />
    <figcaption class="caption">{m.mth_caption_abb1()}</figcaption>
  </figure>

  <Expander
    title={ta(m.bio_mth_growing_plants_1(), m.math_mth_growing_plants_1())}
    open={true}
  >
    <div class="prose">
      {@html marked(
        ta(m.bio_mth_introduction_glowing(), m.math_mth_introduction_glowing()),
      )}
      {@html marked(
        ta(
          m.bio_mth_plant_are_shining_red(),
          m.math_mth_plant_are_shining_red(),
        ),
      )}
      {@html marked(
        ta(
          m.bio_mth_introduction_experiment(),
          m.math_mth_introduction_experiment(),
        ),
      )}
    </div>
    <YouTubeEmbed
      videoId="g3uTNWsDEdo"
      title="Chlorophyll fluorescence experiment"
    />
    <div class="prose">
      {@html marked(
        ta(m.bio_mth_explanation_video(), m.math_mth_explanation_video()),
      )}
    </div>
  </Expander>

  <Expander
    title={m.mth_measuring_fluoreszenz()}
    open={true}
  >
    <div class="prose">
      {@html marked(
        ta(
          m.bio_mth_explanation_measurement_1(),
          m.math_mth_explanation_measurement_1(),
        ),
      )}
      {@html marked(
        ta(m.bio_mth_introduction_phi(), m.math_mth_introduction_phi()),
      )}
    </div>
    <YouTubeEmbed
      videoId="EwXkOlMBl3o"
      title="Measuring fluorescence with PAM"
    />
  </Expander>

  <VideoTranscriptToggle
    message={m.expander_video_transcript()}
    transcript={m.mth_video_transcript_pam()}
  />

  <div class="prose">
    {@html marked(m.mth_headline_pam_measurement())}
    {@html marked(
      ta(
        m.bio_mth_introduction_pam_measurement(),
        m.math_mth_introduction_pam_measurement(),
      ),
    )}
  </div>

  <Expander
    title={m.mth_measuring_light_fluorescence()}
    open={true}
  >
    <div class="prose">
      {@html marked(
        ta(
          m.bio_mth_explanation_introduction_attempts(),
          m.math_mth_explanation_introduction_attempts(),
        ),
      )}
    </div>
    <figure class="page-figure">
      <img
        src="{base}/pictures/PAMbasics.png"
        alt="PAM basics diagram"
        class="page-img centered"
      />
      <figcaption class="caption">{m.mth_caption_abb2()}</figcaption>
    </figure>
  </Expander>

  <section>
    <div class="prose">
      {@html marked(m.mth_headline_illustration())}
      {@html marked(m.mth_explanation_illustration_units())}
      {@html marked(m.mth_explanation_illustration())}
    </div>

    <figure class="page-figure">
      <img
        src="{base}/pictures/Beispielabbildung_en.png"
        alt="Example PAM measurement result"
        class="page-img"
      />
      <figcaption class="caption">{m.mth_caption_abb2()}</figcaption>
    </figure>
  </section>

  <Expander title={m.literature()}>
    <div class="prose">
      {@html marked(m.mth_literature_declaration())}
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
    </div>
  </Expander>

  <PageNav
    base={base}
    prev={{ href: "/photosynthesis", label: m.sde_pagenames_photosynthesis() }}
    next={{ href: "/model", label: m.sde_pagenames_computationalmodels() }}
  />
</article>

<style>
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
    border-radius: 4px;
    width: 100%;
    height: auto;
  }
</style>
