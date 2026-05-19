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
    Link,
    Main,
    Narrow,
    PageNav,
    Section,
    Text,
    YouTubeEmbed,
  } from "@computational-biology-aachen/design";
  import { faGithub } from "@fortawesome/free-brands-svg-icons";
  import { marked } from "marked";
  import Fa from "svelte-fa";
</script>

<Main>
  <Narrow>
    <H1>
      {@html marked(m.str_headline_main())}
    </H1>
    <Text>
      {@html marked(m.str_intro())}
    </Text>

    <section class="usage-section">
      <H2>{@html marked(m.str_headline_usage())}</H2>
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

    <Text>
      {@html marked(ta(m.bio_str_specific_use(), m.math_str_specific_use()))}
    </Text>

    <section class="learning-objectives">
      <H2>
        {@html marked(
          ta(
            m.bio_str_learning_objectives_header(),
            m.math_str_learning_objectives_header(),
          ),
        )}
      </H2>
      <InfoBox>
        <Text>
          {@html marked(
            ta(
              m.bio_str_learning_objectives(),
              m.math_str_learning_objectives(),
            ),
          )}
        </Text>
      </InfoBox>
    </section>

    <Text>
      {@html marked(m.str_link_plants_and_python())}
    </Text>

    <section class="chapters">
      <H2>{@html marked(m.str_headline_pages())}</H2>
      <Text>
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
      </Text>
    </section>

    {#if audienceStore.audience === "4math"}
      <hr />
      <Text>
        {@html marked(m.str_drop_box_intro())}
      </Text>
      <Expander title={m.str_expander_in()}>
        <Text>
          {@html marked(m.str_explanation_in_vitro())}
          {@html marked(m.str_explanation_in_vivo())}
          {@html marked(m.str_explanation_in_silico())}
        </Text>
      </Expander>
      <hr />
    {/if}

    <Expander title={m.str_expander_about()}>
      <Text>
        {@html marked(m.str_explanation_about())}
      </Text>
    </Expander>

    <Expander title={m.appearances()}>
      <Text>
        {@html marked(m.appearance_explanation())}
        {@html marked(m.eps2_conference_title())}
        <div>{@html m.eps2_conference_1()}</div>
        <div>{@html m.eps2_conference_2()}</div>
        <div>{@html m.eps2_conference_3()}</div>
      </Text>
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
      <Text>
        <p>{m.literature_onpage()}</p>
        <ul>
          <li>
            Matuszyńska, A., Heidari, S., Jahns, P., &amp; Ebenhöh, O. (2016). A
            mathematical model of non-photochemical quenching to study
            short-term light memory in plants. Biochimica et Biophysica Acta
            (BBA) - Bioenergetics, 1857(12), 1860-1869.
            <a href="https://doi.org/10.1016/j.bbabio.2016.09.003">
              https://doi.org/10.1016/j.bbabio.2016.09.003
            </a>
          </li>
        </ul>
        <p>{@html marked(m.literature_plants_and_python())}</p>
      </Text>
    </Expander>

    <PageNav
      base={base}
      next={{
        href: "/photosynthesis",
        label: m.sde_pagenames_photosynthesis(),
      }}
    />
  </Narrow>
</Main>

<Section variant="dark">
  <Narrow>
    <h2 id="imprint">Imprint</h2>
    <Text color="light">
      Anbieter i.S.d. TDG/MDStV: Prof. Dr. Anna B. Matuszyńska <br />
      Worringerweg 1 52074 Aachen <br />
      Sammelbau Biologie, Bauteil 42 C, Erdgeschoss, Raum 041 <br />
      Work Phone: +49 241 80 25817 <br />

      Verantwortlich i.S.d. § 6 Abs. 2 MDStV: <br />
      Prof. Dr. Anna B. Matuszyńska <br />
      Design und Umsetzung Dr. Marvin van Aalst <Link
        color="light"
        href="https://github.com/Computational-Biology-Aachen/mxl-web"
        ><Fa icon={faGithub} /></Link
      ><br />
      (c) 2025 Prof. Dr. Anna B. Matuszyńska, Alle Rechte vorbehalten.
    </Text>
  </Narrow>
</Section>
