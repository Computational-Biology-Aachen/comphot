<script lang="ts">
  import { base } from "$app/paths";
  import { ta } from "$lib/i18n";
  import * as m from "$lib/paraglide/messages";
  import { audienceStore } from "$lib/stores/audience.svelte";
  import {
    Accordion as Expander,
    InfoBox,
    Main,
    PageNav,
    VideoTranscriptToggle,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { marked } from "marked";
</script>

<Main>
  <div class="prose">
    {@html marked(m.str_headline_main())}
    {@html marked(m.str_intro())}
  </div>

  <section class="usage-section">
    <div class="prose">{@html marked(m.str_headline_usage())}</div>
    <div class="two-col">
      <div class="col-text prose">
        {@html marked(ta(m.bio_str_usage(), m.math_str_usage()))}
      </div>
      <div class="col-video">
        <YouTubeEmbed
          videoId="KvyjIWLD8rU"
          title="Introduction video"
        />
      </div>
    </div>
  </section>

  <VideoTranscriptToggle
    message={m.expander_video_transcript()}
    transcript={m.str_video_transcript_introduction()}
  />

  <div class="prose">
    {@html marked(ta(m.bio_str_specific_use(), m.math_str_specific_use()))}
  </div>

  <section class="learning-objectives">
    <div class="prose">
      {@html marked(
        ta(
          m.bio_str_learning_objectives_header(),
          m.math_str_learning_objectives_header(),
        ),
      )}
    </div>
    <InfoBox>
      <div class="prose">
        {@html marked(
          ta(m.bio_str_learning_objectives(), m.math_str_learning_objectives()),
        )}
      </div>
    </InfoBox>
  </section>

  <div class="prose">
    {@html marked(m.str_link_plants_and_python())}
  </div>

  <section class="chapters">
    <div class="prose">
      {@html marked(m.str_headline_pages())}
      {@html marked(
        ta(m.bio_str_introduction_pages(), m.math_str_introduction_pages()),
      )}
      {@html marked(
        ta(m.bio_str_photosynthesis(), m.math_str_photosynthesis()),
      )}
      {@html marked(ta(m.bio_str_method(), m.math_str_method()))}
      {@html marked(ta(m.bio_str_model(), m.math_str_model()))}
      {@html marked(ta(m.bio_str_experiment(), m.math_str_experiment()))}
      {@html marked(ta(m.bio_str_memory(), m.math_str_memory()))}
    </div>
  </section>

  {#if audienceStore.audience === "4math"}
    <hr />
    <div class="prose">
      {@html marked(m.str_drop_box_intro())}
    </div>
    <Expander title={m.str_expander_in()}>
      <div class="prose">
        {@html marked(m.str_explanation_in_vitro())}
        {@html marked(m.str_explanation_in_vivo())}
        {@html marked(m.str_explanation_in_silico())}
      </div>
    </Expander>
    <hr />
  {/if}

  <Expander title={m.str_expander_about()}>
    <div class="prose">
      {@html marked(m.str_explanation_about())}
      {@html marked(m.programs_used())}
    </div>
  </Expander>

  <Expander title={m.appearances()}>
    <div class="prose">
      {@html marked(m.appearance_explanation())}
      {@html marked(m.eps2_conference_title())}
      <div>{@html m.eps2_conference_1()}</div>
      <div>{@html m.eps2_conference_2()}</div>
      <div>{@html m.eps2_conference_3()}</div>
    </div>
    <div class="poster-row">
      <img
        src="{base}/pictures/Poster.png"
        alt="ComPhot Poster"
        class="poster-img"
      />
      <img
        src="{base}/pictures/Editable/Elouen_Poster.svg"
        alt="Elouen Poster"
        class="poster-img"
      />
    </div>
  </Expander>

  <Expander title={m.literature()}>
    <div class="prose">
      <p>{m.literature_onpage()}</p>
      <ul>
        <li>
          Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A
          mathematical model of non-photochemical quenching to study short-term
          light memory in plants. Biochimica et Biophysica Acta (BBA) -
          Bioenergetics, 1857(12), 1860-1869.
          <a href="https://doi.org/10.1016/j.bbabio.2016.09.003">
            https://doi.org/10.1016/j.bbabio.2016.09.003
          </a>
        </li>
      </ul>
      <p>{@html marked(m.literature_plants_and_python())}</p>
    </div>
  </Expander>

  <PageNav
    base={base}
    next={{ href: "/photosynthesis", label: m.sde_pagenames_photosynthesis() }}
  />
</Main>

<style>
  .usage-section {
    margin: var(--space-6) 0;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1.5fr;
    align-items: start;
    gap: var(--space-6);
    margin-top: var(--space-4);
  }

  @media (max-width: 600px) {
    .two-col {
      grid-template-columns: 1fr;
    }
  }

  .learning-objectives {
    margin: var(--space-6) 0;
  }

  .chapters {
    margin: var(--space-6) 0;
  }

  .poster-row {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-4);
    margin-top: var(--space-4);
  }

  .poster-img {
    border-radius: 4px;
    max-width: 45%;
    height: auto;
  }
</style>
